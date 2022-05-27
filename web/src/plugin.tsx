// Copyright 2022 H2O.ai, Inc.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import React from 'react';
import { B, Dict, gensym, S, U, xid } from "./core";
import { Plugin, Script } from './protocol';
import { BoxProps, Context, make } from './ui';

enum ScriptState { NotInstalled, Installing, Installed }

type Module = {
  id: S
  ctors: S[]
  exports: any
  ready: B
}

const
  nextPluginID = gensym('nitroplug_'),
  installedModules: Dict<Module> = {}, // global
  installedScripts: Dict<ScriptState> = {}, // global
  installScript = ({ source, type, asynchronous, cross_origin, referrer_policy, integrity }: Script) => {
    const status = installedScripts[source]
    if (status === ScriptState.Installed || status === ScriptState.Installing) return
    installedScripts[source] = ScriptState.Installing
    const e = document.createElement('script')
    e.type = 'text/javascript'
    e.src = source
    if (type) e.type = type
    if (asynchronous) e.async = true
    if (cross_origin) e.crossOrigin = cross_origin
    if (referrer_policy) e.referrerPolicy = referrer_policy
    if (integrity) e.integrity = integrity
    e.addEventListener('load', () => {
      installedScripts[source] = ScriptState.Installed
    })
    document.body.appendChild(e)
  },
  wrapSource = (name: S, source: S) => `function ${name}(exports){${source}}`,
  inlineScript = (name: S, { source }: Script) => {
    const e = document.createElement('script')
    e.type = 'text/javascript'
    // HTML5 specifies that a <script> tag inserted with innerHTML should not execute.
    // See https://developer.mozilla.org/en-US/docs/Web/API/Element/innerHTML#security_considerations
    // See https://www.w3.org/TR/2008/WD-html5-20080610/dom.html#innerhtml0
    e.appendChild(document.createTextNode(wrapSource(name, source)))
    document.body.appendChild(e)
  },
  installScripts = (plugin: Module, scripts: Script[]) => {
    const nextScriptID = gensym(plugin.id + '_')
    for (const script of scripts) {
      if (script.type === 'inline') {
        const ctor = nextScriptID()
        inlineScript(ctor, script)
        plugin.ctors.push(ctor)
      } else {
        installScript(script)
      }
    }
  },
  installPlugin = ({ name, scripts }: Plugin) => {
    const plugin = installedModules[name] = {
      id: nextPluginID(),
      ctors: [],
      exports: {},
      ready: false,
    }
    installScripts(plugin, scripts)
  },
  waitFor = (timeout: U, interval: U, ok: () => B, pass: () => void, fail: () => void) => {
    let elapsed = 0
    const timer = setInterval(() => {
      if (ok()) {
        clearInterval(timer)
        pass()
      } else {
        elapsed += interval // approx
        if (elapsed > timeout) {
          clearInterval(timer)
          fail()
        }
      }
    }, interval)
  },
  areScriptsInstalled = () => Object.values(installedScripts).every(state => state === ScriptState.Installed),
  waitForScriptInstallation = (pass: () => void) => {
    waitFor(10000, 10, areScriptsInstalled, pass, () => console.error('One or more scripts failed to load.'))
  },
  loadModule = (name: S, onload: (m: Module) => void) => {
    const module = installedModules[name]
    if (!module) {
      console.error(`Plugin module "${name}" not found.`)
      return
    }
    if (module.ready) {
      onload(module)
      return
    }
    waitFor(10000, 10, () => module.ready, () => onload(module), () => console.error(`Timed out waiting for plugin "${name}" to load.`))
  }

export const
  installPlugins = (plugins: Plugin[]) => {
    plugins.forEach(installPlugin)
    waitForScriptInstallation(() => {
      Object.values(installedModules).forEach(module => {
        module.ctors.forEach(ctor => {
          const f = (window as any)[ctor]
          if (f) f(module.exports)
        })
        module.ready = true
      })
    })
  },
  execPlugin = (name: S, method: S, context: Context, element: Element, data?: any) => {
    loadModule(name, module => {
      const f = module.exports[method]
      if (f) {
        if (element) {
          f(context, element, data)
        } else {
          f(context, data)
        }
      } else {
        console.error(`No exported function named "${method}" in plugin "${name}".`)
      }
    })
  },
  PluginBox = make(({ context, box }: BoxProps) => {
    const
      sig = (box.mode ?? ':.').split(':')[1],
      [plugin, method] = sig.split('.'),
      id = xid(),
      ref = React.createRef<HTMLDivElement>(),
      init = () => {
        if (ref.current) execPlugin(plugin, method, context, ref.current, box.data)
      },
      render = () => (<div id={id} ref={ref} />)

    return { init, render }
  })
