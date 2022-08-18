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

import { BaseSlots, createTheme, getColorFromString, IColor, isDark, loadTheme, ThemeGenerator, themeRulesStandardCreator } from '@fluentui/react';
import { fromSpectrum, grays, isColor, rgbToHex, RGBTriplet, shades, spectrum } from './color';
import { B, Dict, S, words, zip } from './core';
import { Theme as ProtocolTheme } from './protocol';

export type Scheme = {
  sansFont: S
  monospaceFont: S
  foregroundColor: S
  backgroundColor: S
  accentColor: S
}

const
  generateTheme = (scheme: Scheme) => {
    //
    // Adapted from https://github.com/microsoft/fluentui/blob/master/apps/theming-designer/src/components/ThemingDesigner.tsx
    //
    const
      foregroundColor = getColorFromString(scheme.foregroundColor)!,
      backgroundColor = getColorFromString(scheme.backgroundColor)!,
      accentColor = getColorFromString(scheme.accentColor)!,
      slots: [BaseSlots, IColor][] = [
        [BaseSlots.primaryColor, accentColor],
        [BaseSlots.foregroundColor, foregroundColor],
        [BaseSlots.backgroundColor, backgroundColor]
      ],
      rules = themeRulesStandardCreator(),
      isInverted = isDark(backgroundColor)

    ThemeGenerator.insureSlots(rules, isInverted)
    for (const [slot, color] of slots) {
      ThemeGenerator.setSlot(rules[BaseSlots[slot]], color, isInverted, true, true)
    }

    const
      palette: Dict<S> = ThemeGenerator.getThemeAsJson(rules),
      theme = createTheme({
        defaultFontStyle: {
          fontFamily: 'inherit',
        },
        palette,
        isInverted,
      })
    return theme
  },
  exportVars = (vars: [S, S][]) => {
    const
      root = document.querySelector(':root') as HTMLElement,
      style = root.style
    for (const [k, v] of vars) style.setProperty(k, v)
  },
  exportTheme = (prose: S, dark: B) => {
    const root = document.querySelector('html') as HTMLElement
    if (root) {
      const add: S[] = [], remove: S[] = []
      for (const shade of grays) {
        const klass = 'prose-' + shade
        if (shade === prose) add.push(klass); else remove.push(klass)
      }
      if (dark) add.push('dark'); else remove.push('dark')
      if (add.length) root.classList.add(...add)
      if (remove.length) root.classList.remove(...remove)
    }
  }

export const applyTheme = ({ mode, accent }: ProtocolTheme) => {
  let prose = 'gray'

  if (!mode) mode = 'light'
  if (!accent || !isColor(accent)) accent = 'indigo'

  const
    modes = new Set(words(mode)),
    isDarkMode = modes.has('dark')

  for (const shade of grays) if (modes.has(shade)) prose = shade

  const
    foreground = fromSpectrum(prose, isDarkMode ? '300' : '700') ?? [0, 0, 0],// Mimic Tailwind prose.
    background: RGBTriplet = isDarkMode ? (fromSpectrum(prose, '900') ?? [0, 0, 0]) : [255, 255, 255],
    foregroundColor = rgbToHex(foreground),
    backgroundColor = rgbToHex(background),
    accentColor = rgbToHex(fromSpectrum(accent, isDarkMode ? '400' : '600') ?? [99, 102, 241]),
    scheme: Scheme = {
      sansFont: 'inherit',
      monospaceFont: 'inherit',
      backgroundColor,
      foregroundColor,
      accentColor,
    },
    theme = generateTheme(scheme),
    vars: [S, S][] = zip(spectrum[accent], shades, (c, s) => ([`--ui-accent-${s}`, c.join(' ')]))

  vars.push(['--ui-foreground', foreground.join(' ')])
  vars.push(['--ui-background', background.join(' ')])

  exportVars(vars)
  exportTheme(prose, theme.isInverted)
  loadTheme(theme)
}
