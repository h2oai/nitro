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

import { BaseSlots, createTheme, getColorFromString, IColor, isDark, loadTheme, Theme, ThemeGenerator, themeRulesStandardCreator } from '@fluentui/react';
import { B, Dict, S } from './core';

export type Scheme = {
  sansFont: S
  monospaceFont: S
  foregroundColor: S
  backgroundColor: S
  accentColor: S
}

export const defaultScheme: Scheme = {
  sansFont: 'inherit',
  monospaceFont: 'inherit',
  foregroundColor: '#3f3f46', // zinc-700
  backgroundColor: '#ffffff',
  accentColor: '#6366f1', // indigo-500
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
      currentIsDark = isDark(rules[BaseSlots[BaseSlots.backgroundColor]].color!)

    ThemeGenerator.insureSlots(rules, currentIsDark)
    for (const [slot, color] of slots) {
      ThemeGenerator.setSlot(rules[BaseSlots[slot]], color, currentIsDark, true, true)
    }

    const
      palette: Dict<S> = ThemeGenerator.getThemeAsJson(rules),
      theme = createTheme({
        defaultFontStyle: {
          fontFamily: 'inherit',
        },
        palette,
        isInverted: isDark(rules[BaseSlots[BaseSlots.backgroundColor]].color!),
      })
    return theme
  },
  exportSwatches = (swatches: [S, S][]) => {
    const
      root = document.querySelector(':root') as HTMLElement,
      s = root.style
    for (const [name, color] of swatches) {
      s.setProperty(`--${name}`, `${color}`)
    }
  },
  hyphenCase = (s: S) => s.replace(/[A-Z]/g, x => '-' + x.toLowerCase()),
  dict2Swatches = (colors: Dict<S>, prefix: S) => {
    const swatches: [S, S][] = []
    for (const k in colors) {
      swatches.push([prefix + hyphenCase(k), colors[k]])
    }
    return swatches
  },
  extractSwatches = (theme: Theme) => {
    const
      {
        black,
        white,
        accent,

        themeDarker,
        themeDark,
        themeDarkAlt,
        themePrimary,
        themeSecondary,
        themeTertiary,
        themeLight,
        themeLighter,
        themeLighterAlt,

        neutralDark,
        neutralPrimary,
        neutralPrimaryAlt,
        neutralSecondary,
        neutralSecondaryAlt,
        neutralTertiary,
        neutralTertiaryAlt,
        neutralQuaternary,
        neutralQuaternaryAlt,
        neutralLight,
        neutralLighter,
        neutralLighterAlt,

      } = theme.palette,

      colors: Dict<S> = {
        'foreground': black,
        'background': white,
        accent,

        'accentDarker': themeDarker,
        'accentDark': themeDark,
        'accentDarkAlt': themeDarkAlt,
        'accentPrimary': themePrimary,
        'accentSecondary': themeSecondary,
        'accentTertiary': themeTertiary,
        'accentLight': themeLight,
        'accentLighter': themeLighter,
        'accentLighterAlt': themeLighterAlt,

        neutralDark,
        neutralPrimary,
        neutralPrimaryAlt,
        neutralSecondary,
        neutralSecondaryAlt,
        neutralTertiary,
        neutralTertiaryAlt,
        neutralQuaternary,
        neutralQuaternaryAlt,
        neutralLight,
        neutralLighter,
        neutralLighterAlt,
      }

    return dict2Swatches(colors, '')
  },
  exportDarkMode = (enable: B) => {
    const root = document.querySelector('html') as HTMLElement
    if (root) {
      if (enable) {
        root.classList.add('dark')
      } else {
        root.classList.remove('dark')
      }
    }
  }

export const loadScheme = (scheme: Scheme) => {
  const theme = generateTheme(scheme)
  exportSwatches(extractSwatches(theme))
  exportDarkMode(theme.isInverted)
  loadTheme(theme)
}
