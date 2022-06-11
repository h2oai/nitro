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

type Go = (error: S | null) => void

type Module = {
  plugin: Plugin
  imports: Script[]
  sources: Source[]
  exports: any
}

type Source = {
  ctor: S
  code: S
}

function sequence<X, Y>(xs: X[], f: (x: X, go: Go) => void, go: Go) {
  const
    q = xs.slice().reverse(),
    next = () => {
      const x = q.pop()
      if (x) {
        f(x, e => {
          if (e) {
            go(e)
          } else {
            next()
          }
        })
      } else {
        go(null)
      }
    }
  next()
}

const
  modules: Dict<Module> = {},
  installScript = (script: Script, go: Go) => {
    const { source, type, asynchronous, cross_origin, referrer_policy, integrity } = script
    const e = document.createElement('script')
    e.type = 'text/javascript'
    e.src = source
    if (type) e.type = type
    if (asynchronous) e.async = true
    if (cross_origin) e.crossOrigin = cross_origin
    if (referrer_policy) e.referrerPolicy = referrer_policy
    if (integrity) e.integrity = integrity
    e.addEventListener('load', () => go(null))
    document.body.appendChild(e)
  },
  installSource = ({ ctor, code }: Source, go: Go) => {
    const e = document.createElement('script')
    e.type = 'text/javascript'
    // HTML5 specifies that a <script> tag inserted with innerHTML should not execute.
    // See https://developer.mozilla.org/en-US/docs/Web/API/Element/innerHTML#security_considerations
    // See https://www.w3.org/TR/2008/WD-html5-20080610/dom.html#innerhtml0
    e.appendChild(document.createTextNode(`function ${ctor}(exports){${code}}`))
    document.body.appendChild(e)
    go(null)
  },
  installModule = (module: Module, go: Go) => {
    const
      { plugin, imports, sources, exports } = module,
      nextCtor = gensym(plugin.name + '_')

    for (const script of plugin.scripts) {
      if (script.type === 'inline') {
        sources.push({ ctor: nextCtor(), code: script.source })
      } else {
        imports.push(script)
      }
    }
    // imported scripts first, in order
    sequence(imports, installScript, e => {
      if (e) {
        go(e)
        return
      }
      // local scripts next, in order
      sequence(sources, installSource, e => {
        if (e) {
          go(e)
          return
        }
        for (const { ctor } of sources) {
          const f = (window as any)[ctor]
          if (f) f(exports)
        }
        go(null)
      })
    })
  },
  execPlugin = (name: S, method: S, context: Context, element: Element, data?: any) => {
    loadModule(name, module => {
      const f = module.exports[method]
      if (f) {
        f(context, element, data)
      } else {
        console.error(`No exported function named "${method}" in plugin "${name}".`)
      }
    })
  },
  waitFor = (timeout: U, interval: U, test: () => B, pass: () => void, fail: () => void) => {
    let elapsed = 0
    const timer = setInterval(() => {
      if (test()) {
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
  loadModule = (name: S, onLoad: (m: Module) => void) => {
    const module = modules[name]
    if (module) {
      onLoad(module)
      return
    }
    waitFor(
      10000, 10,
      () => modules[name] ? true : false,
      () => onLoad(modules[name]),
      () => console.error(`Timed out waiting for plugin "${name}" to load.`),
    )
  }

export const
  installPlugins = (plugins: Plugin[]) => {
    plugins.forEach(plugin => { // parallel
      const module: Module = {
        plugin,
        imports: [],
        sources: [],
        exports: {},
      }
      installModule(module, e => {
        if (e) {
          console.error(e)
          return
        }
        modules[plugin.name] = module
      })
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