import { BaseSlots, createTheme, getColorFromString, IColor, isDark, ThemeGenerator, themeRulesStandardCreator } from '@fluentui/react';
import { Dict, S } from './core';

export type Scheme = {
  primaryFont: S
  monospaceFont: S
  primaryColor: S
  foregroundColor: S
  backgroundColor: S
}

export const generateTheme = (scheme: Scheme) => {
  //
  // Adapted from https://github.com/microsoft/fluentui/blob/master/apps/theming-designer/src/components/ThemingDesigner.tsx
  //
  const
    foregroundColor = getColorFromString(scheme.foregroundColor)!,
    backgroundColor = getColorFromString(scheme.backgroundColor)!,
    primaryColor = getColorFromString(scheme.primaryColor)!,
    slots: [BaseSlots, IColor][] = [
      [BaseSlots.primaryColor, primaryColor],
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
      ...{ palette },
      isInverted: isDark(rules[BaseSlots[BaseSlots.backgroundColor]].color!),
    })

  return theme
}
