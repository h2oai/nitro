import { Calendar, Checkbox, ChoiceGroup, ColorPicker, ComboBox, CommandBar, CompoundButton, ContextualMenu, ContextualMenuItemType, cssColor, DatePicker, DateRangeType, DefaultButton, Dropdown, DropdownMenuItemType, IButtonStyles, IChoiceGroupOption, IColor, IColorCellProps, IComboBox, IComboBoxOption, IContextualMenuItem, IContextualMenuProps, IDropdownOption, IRGB, ISliderProps, ISpinButtonStyles, IStackItemStyles, IStackTokens, ITag, ITextFieldProps, Label, MaskedTextField, Position, PrimaryButton, Rating, Slider, SpinButton, Stack, SwatchColorPicker, TagPicker, TextField, Toggle } from '@fluentui/react';
import { GlobalNavButtonActiveIcon, GlobalNavButtonIcon, RocketIcon } from '@fluentui/react-icons-mdl2';
import React from 'react';
import styled from 'styled-components';
import { B, box, Dict, gensym, isN, isPair, isS, N, S, U, V, xid } from './core';
import { Markdown } from './markdown';
import { Conf, Input, MsgType, Option, Stackable, Stacking, Widget, WidgetT } from './protocol';
import { Send } from './socket';
import { make } from './ui';

const newCaptureContext = (send: Send, data: Array<V | V[]>) => {
  const capture = <T extends V | V[]>(index: any, value: T) => {
    if (index >= 0) data[index] = value
  }
  const submit = () => send({ t: MsgType.Input, d: data })
  return { capture, submit }
}

type Context = ReturnType<typeof newCaptureContext>

type InputProps = { context: Context, input: Input }

const unum = (x: any): N | undefined => isN(x) ? x : undefined
const ustr = (x: any): S | undefined => isS(x) ? x : undefined
const udate = (x: any): Date | undefined => isS(x) ? new Date(x) : undefined
const snakeToCamelCase = (s: S): S => s.replace(/(_\w)/g, m => m[1].toUpperCase())
const getDefaultValue = (value: any, min: any, max: any, step: any): N | undefined => {
  if (isN(value)) return value
  if (isN(min)) return Math.max(0, min)
  if (isN(max)) return Math.min(0, max)
  if (isN(step)) return 0
  return undefined
}

const WithLabel = ({ label, children }: { label?: S, children: JSX.Element }) => (
  label
    ? (
      <Stack>
        <Stack.Item>
          <Label>{label}</Label>
        </Stack.Item>
        <Stack.Item>{children}</Stack.Item>
      </Stack>
    ) : (
      children
    )
)

const XTextField = make(({ context, input }: InputProps) => {
  const
    { index, text, value, placeholder, icon, mask, prefix, suffix, error, lines, required, password } = input,
    onChange = ({ target }: React.FormEvent<HTMLInputElement | HTMLTextAreaElement>, v?: S) => {
      v = v ?? (target as HTMLInputElement).value ?? value ?? ''
      // TODO live?
      context.capture(index, v)
    },
    render = () => {
      const
        field: Partial<ITextFieldProps> = {
          label: text,
          defaultValue: isS(value) ? value : isN(value) ? String(value) : undefined,
          placeholder: placeholder ?? (text ? undefined : 'Enter some text...'),
          errorMessage: error,
          required: required === true,
          onChange,
        }
      return password === true
        ? <TextField {...field} type='password' canRevealPassword revealPasswordAriaLabel='Show password' />
        : mask
          ? <MaskedTextField {...field} mask={mask} />
          : lines && (lines >= 1)
            ? <TextField {...field} multiline resizable autoAdjustHeight rows={lines} />
            : <TextField {...field} iconProps={icon ? { iconName: icon } : undefined} prefix={prefix} suffix={suffix} />
    }

  context.capture(index, (value as any) ?? '')
  return { render }
})


const XSpinButton = make(({ context, input }: InputProps) => {
  const
    { index, min, max, step, value } = input,

    defaultValue = getDefaultValue(value, min, max, step) ?? 0,
    onChange = (event: React.SyntheticEvent<HTMLElement>, value?: string): void => {
      let v = isS(value) ? parseFloat(value) : defaultValue
      if (isNaN(v)) v = defaultValue
      context.capture(index, v)
    },
    render = () => {
      const
        { text, value, min, max, step, precision } = input

      return (
        <SpinButton
          label={text}
          labelPosition={Position.top}
          defaultValue={isS(value) ? value : isN(value) ? String(value) : undefined}
          min={unum(min)}
          max={unum(max)}
          step={step}
          precision={precision}
          styles={{ labelWrapper: { marginBottom: -4 } }} // Make textbox top match textfield
          onChange={onChange}
        />
      )
    }

  context.capture(index, defaultValue)

  return { render }
})

const XSlider = make(({ context, input }: InputProps) => {
  const
    { index, text, value, min, max, step } = input,
    originFromZero = isN(min) && min < 0 && isN(max) && max > 0,
    ranged = isPair(value) && isN(value[0]) && isN(value[1]),
    defaultValue = ranged ? 0 : getDefaultValue(value, min, max, step),
    defaultValueMin = ranged ? getDefaultValue(value[0], min, max, step) : 0,
    defaultValueMax = ranged ? getDefaultValue(value[1], min, max, step) : 0,
    onChange = (v: U, range?: [U, U]) => {
      context.capture(index, range ? range : v)
    },
    render = () => {
      const
        props: Partial<ISliderProps> = {
          label: text,
          min: unum(min),
          max: unum(max),
          step,
          originFromZero,
          ranged,
          onChange,
        }

      return ranged
        ? (
          <Slider
            {...props}
            defaultLowerValue={defaultValueMin}
            defaultValue={defaultValueMax}
          />
        ) : (
          <Slider
            {...props}
            defaultValue={defaultValue}
          />
        )
    }

  if (ranged) {
    if (defaultValueMin !== undefined && defaultValueMax !== undefined) {
      context.capture(index, [defaultValueMin, defaultValueMax])
    }
  } else {
    if (defaultValue !== undefined) {
      context.capture(index, defaultValue)
    }
  }

  return { render }
})

const XRating = make(({ context, input }: InputProps) => {
  const
    { index, text, min, max, value } = input,
    allowZeroStars = isN(min) && min <= 0,
    defaultRating = unum(value) ?? (allowZeroStars ? 0 : 1),
    onChange = (event: React.FormEvent<HTMLElement>, rating?: number) => {
      if (rating === undefined) return
      context.capture(index, rating)
    },
    render = () => {
      return (
        <WithLabel label={text}>
          <Rating
            defaultRating={defaultRating}
            allowZeroStars={allowZeroStars}
            max={unum(max)}
            onChange={onChange}
          />
        </WithLabel>
      )
    }

  context.capture(index, defaultRating)

  return { render }
})

const leftPad = (c: S, n: U) => {
  let pad = ''
  for (let i = 0; i < n; i++) pad += c
  return (s: S) => {
    if (s.length >= n) return s
    s = pad + s
    return s.substring(s.length - n)
  }
}

const lpad2 = leftPad('0', 2)

type Clock = {
  hh: U, mm: U, ss: U,
  pm: B, c24: B,
}
const
  parseClock = (t: S): Clock => {
    const
      am = t.endsWith('am'),
      pm = !am && t.endsWith('pm'),
      c24 = !(am || pm),
      hhmmss = c24 ? t : t.substring(0, t.length - 2),
      [hh, mm, ss] = hhmmss.split(':').map(t => parseInt(t, 10))
    return { hh, mm, ss, pm, c24 }
  },
  clockToString = ({ hh, mm, ss, pm, c24 }: Clock) => {
    const parts: S[] = []
    if (!isNaN(hh)) parts.push(lpad2(String(hh)))
    if (!isNaN(mm)) parts.push(lpad2(String(mm)))
    if (!isNaN(ss)) parts.push(lpad2(String(ss)))
    const s = parts.join(':')
    return c24 ? s : s + (pm ? 'PM' : 'AM')
  }

const XTimePicker = make(({ context, input }: InputProps) => {
  const
    { index, text, value } = input,
    clock = parseClock(String(value).toLowerCase()),
    capture = () => context.capture(index, clockToString(clock)),
    hide: IStackItemStyles = { root: { display: 'none' } },
    narrow: Partial<ISpinButtonStyles> = { labelWrapper: { marginBottom: -4 }, spinButtonWrapper: { width: 50 } },
    onHoursChange = (_: React.SyntheticEvent<HTMLElement>, value?: S): void => {
      if (value) clock.hh = parseInt(value)
      capture()
    },
    onMinutesChange = (_: React.SyntheticEvent<HTMLElement>, value?: S): void => {
      if (value) clock.mm = parseInt(value)
      capture()
    },
    onSecondsChange = (_: React.SyntheticEvent<HTMLElement>, value?: S): void => {
      if (value) clock.ss = parseInt(value)
      capture()
    },
    onToggleChange = (_: React.SyntheticEvent<HTMLElement>, checked?: B): void => {
      if (checked !== undefined) clock.pm = checked
      capture()
    },
    render = () => {
      return (
        <WithLabel label={text}>
          <Stack horizontal horizontalAlign='start' tokens={gap5}>
            <Stack.Item styles={isNaN(clock.hh) ? hide : undefined}>
              <SpinButton
                label='Hours'
                labelPosition={Position.top}
                defaultValue={String(clock.hh)}
                min={clock.c24 ? 0 : 1}
                max={clock.c24 ? 23 : 12}
                styles={narrow}
                onChange={onHoursChange}
              />
            </Stack.Item>
            <Stack.Item styles={isNaN(clock.mm) ? hide : undefined}>
              <SpinButton
                label='Minutes'
                labelPosition={Position.top}
                defaultValue={String(clock.mm)}
                min={0}
                max={59}
                styles={narrow}
                onChange={onMinutesChange}
              />
            </Stack.Item>
            <Stack.Item styles={isNaN(clock.ss) ? hide : undefined}>
              <SpinButton
                label='Seconds'
                labelPosition={Position.top}
                defaultValue={String(clock.ss)}
                min={0}
                max={59}
                styles={narrow}
                onChange={onSecondsChange}
              />
            </Stack.Item>
            <Stack.Item styles={clock.c24 ? hide : undefined} align='end'>
              <Toggle
                offText='AM'
                onText='PM'
                defaultChecked={clock.pm}
                onChange={onToggleChange}
              />
            </Stack.Item>
          </Stack>
        </WithLabel>
      )
    }

  capture()

  return { render }
})

const dateToString = (d: Date) => d.toISOString().substring(0, 10)

const XDatePicker = make(({ context, input }: InputProps) => {
  const
    { index, value } = input,
    defaultDate = udate(value) ?? new Date(),
    defaultValue = dateToString(defaultDate),
    onSelectDate = (d?: Date | null) => {
      console.log('in select', d)
      context.capture(index, dateToString(d ?? defaultDate))
    },
    render = () => {
      const
        { text, placeholder, value, min, max, required } = input,
        date = udate(value),
        minDate = udate(min),
        maxDate = udate(max)

      // TODO firstDayOfWeek, firstWeekOfYear customization
      // TODO pass strings for localization
      return (
        <DatePicker
          label={text}
          value={date}
          minDate={minDate}
          maxDate={maxDate}
          placeholder={placeholder}
          onSelectDate={onSelectDate}
          isRequired={required}
          highlightSelectedMonth
          showGoToToday
        />
      )
    }

  context.capture(index, defaultValue)

  return { render }
})

const XCalendar = make(({ context, input }: InputProps) => {
  const
    { index, value } = input,
    defaultDate = udate(value) ?? new Date(),
    defaultValue = dateToString(defaultDate),
    onSelectDate = (d?: Date) => {
      context.capture(index, dateToString(d ?? new Date()))
    },
    render = () => {
      // TODO format string; aria-label
      const
        { text, mode, value, min, max } = input,
        date = udate(value),
        minDate = udate(min),
        maxDate = udate(max),
        dateRangeType = mode === 'week'
          ? DateRangeType.Week
          : mode === 'month'
            ? DateRangeType.Month
            : DateRangeType.Day
      // TODO firstDayOfWeek, firstWeekOfYear customization
      // TODO pass strings for localization
      return (
        <WithLabel label={text}>
          <Calendar
            dateRangeType={dateRangeType}
            value={date}
            minDate={minDate}
            maxDate={maxDate}
            isDayPickerVisible={mode !== 'month'}
            onSelectDate={onSelectDate}
            highlightSelectedMonth
            showGoToToday
          />
        </WithLabel>
      )
    }

  context.capture(index, defaultValue)

  return { render }
})


const XColorPicker = make(({ context, input }: InputProps) => {
  const
    { index, text, value } = input,
    colorValue = value ? String(value) : '#000',
    defaultColor = cssColor(colorValue),
    colorToTuple = ({ r, g, b, a }: IRGB) => [r, g, b, a ?? 100],
    capture = (color: IRGB) => context.capture(index, colorToTuple(color)),
    onChange = (_: React.SyntheticEvent<HTMLElement>, color: IColor) => capture(color),
    render = () => {
      return (
        <WithLabel label={text}>
          <ColorPicker
            color={colorValue}
            alphaType='alpha'
            onChange={onChange}
            showPreview
          />
        </WithLabel>
      )
    }

  if (defaultColor) capture(defaultColor)

  return { render }
})

const CheckboxContainer = styled.div`
  margin: 0.5rem 0;
`
const XCheckList = make(({ context, input }: InputProps) => {
  const
    { index, text, options } = input,
    selecteds = selectedsOf(input),
    selection = new Set<S>(selecteds.map(s => String(s.value))),
    capture = () => context.capture(index, Array.from(selection)),
    onChecked = (value?: V, checked?: B) => {
      if (checked) {
        selection.add(String(value))
      } else {
        selection.delete(String(value))
      }
      capture()
    },
    render = () => {
      const
        checkboxes = options.map(c => (
          <CheckboxContainer key={c.value}>
            <Checkbox
              label={c.text}
              defaultChecked={selection.has(String(c.value))}
              onChange={(_, checked) => onChecked(c.value, checked)}
            />
          </CheckboxContainer>
        ))

      return (
        <WithLabel label={text}><div>{checkboxes}</div></WithLabel>
      )
    }

  capture()

  return { render }
})

// TODO support icons on items. See "Customized Dropdown" Fluent example.
const XDropdown = make(({ context, input }: InputProps) => {
  const
    { index, text, placeholder, error, required, options } = input,
    selected = selectedOf(input),
    hasGroups = options.some(c => c.options?.length ? true : false),
    items: IDropdownOption[] = hasGroups ? toGroupedDropdownOptions(options) : options.map(toDropdownOption),
    selectedKey = selected ? selected.value : undefined,
    onChange = (_?: React.FormEvent<HTMLElement>, option?: IDropdownOption) => {
      if (option) context.capture(index, option.key)
    },
    render = () => {
      return (
        <Dropdown
          label={text}
          placeholder={placeholder}
          options={items}
          selectedKey={selectedKey}
          errorMessage={error}
          required={required ? true : false}
          onChange={onChange}
        />
      )
    }

  if (selected) context.capture(index, selected.value)

  return { render }
})

const XMultiSelectDropdown = make(({ context, input }: InputProps) => {
  const
    { index, text, placeholder, error, required, options } = input,
    selecteds = selectedsOf(input),
    selection = new Set<S>(selecteds.map(s => String(s.value))),
    items: IDropdownOption[] = options.map(c => ({ key: c.value, text: String(c.text) })),
    selectedKeys = selecteds.map(c => String(c.value)),
    capture = () => context.capture(index, Array.from(selection)),
    onChange = (_?: React.FormEvent<HTMLElement>, option?: IDropdownOption) => {
      if (option) {
        const key = String(option.key)
        if (option.selected) {
          selection.add(key)
        } else {
          selection.delete(key)
        }
        capture()
      }
    },
    render = () => {
      return (
        <Dropdown
          multiSelect
          label={text}
          placeholder={placeholder}
          options={items}
          defaultSelectedKeys={selectedKeys}
          errorMessage={error}
          required={required ? true : false}
          onChange={onChange}
        />
      )
    }

  capture()

  return { render }
})


const XComboBox = make(({ context, input }: InputProps) => {
  const
    { index, value, text, placeholder, required, error, options } = input,
    items: IComboBoxOption[] = options.map(c => ({ key: String(c.value), text: c.text ?? '' })),
    selected = selectedOf(input),
    selectedKey = selected ? String(selected.value) : undefined,
    // Double-test because value may not be an available option.
    initialValue = selected ? String(selected.value) : value ? String(value) : undefined,
    onChange = (_: React.FormEvent<IComboBox>, option?: IComboBoxOption, _index?: N, value?: S) => {
      const v = option ? option.text : value
      if (v) context.capture(index, v)
    },
    render = () => {
      return (
        <ComboBox
          label={text}
          text={initialValue}
          placeholder={placeholder}
          options={items}
          defaultSelectedKey={selectedKey}
          required={required}
          errorMessage={error}
          onChange={onChange}
          allowFreeform
          autoComplete='on'
        />
      )
    }
  if (initialValue) context.capture(index, initialValue)
  return { render }
})

const toContextualMenuItem = ({ value, text, caption, icon, options }: Option, capture: (v: V) => void): IContextualMenuItem => {
  return text
    ? {
      key: String(value),
      text,
      title: caption,
      iconProps: icon ? { iconName: icon } : undefined,
      subMenuProps: options ? toContextualMenuProps(options, capture) : undefined,
      onClick: () => capture(value),
    } : {
      key: xid(),
      itemType: ContextualMenuItemType.Divider,
    }
}
const toContextualMenuProps = (cs: Option[], capture: (v: V) => void): IContextualMenuProps => ({ items: cs.map(c => toContextualMenuItem(c, capture)) })

const continueAction: Option = { t: WidgetT.Option, value: 'continue', text: 'Continue', selected: true }
const continueWidget: Widget = { t: WidgetT.Input, xid: xid(), mode: 'button', index: -1 /* don't capture */, options: [continueAction] }

const ButtonsContainer = styled.div`
  margin: 1rem 0 2rem;
`
const XButtons = make(({ context, input }: InputProps) => {
  const
    { value } = input,
    selection = new Set<V>(Array.isArray(value) ? value : value ? [value] : []),
    render = () => {
      const
        { text, value, index, row, options } = input,
        horizontal = row !== false,
        styles: IButtonStyles = horizontal ? {} : { root: { width: '100%' } },
        compoundStyles: IButtonStyles = horizontal ? {} : { root: { width: '100%', maxWidth: 'auto' } },
        capture = (value: V) => {
          context.capture(index, value)
          context.submit()
        },
        buttons = options.map(c => {
          const
            text = c.text,
            onClick = () => capture(c.value),
            button = c.selected || selection.has(c.value)
              ? c.options
                ? c.value === ''
                  ? <PrimaryButton text={text ?? 'Choose an action'} menuProps={toContextualMenuProps(c.options, capture)} />
                  : <PrimaryButton split text={text} styles={styles} menuProps={toContextualMenuProps(c.options, capture)} onClick={onClick} />
                : c.caption
                  ? <CompoundButton primary text={text} secondaryText={c.caption} styles={compoundStyles} onClick={onClick} />
                  : <PrimaryButton text={text} styles={styles} onClick={onClick} />
              : c.options
                ? c.value === ''
                  ? <DefaultButton text={text ?? 'Choose an action'} menuProps={toContextualMenuProps(c.options, capture)} />
                  : <DefaultButton split text={text} styles={styles} menuProps={toContextualMenuProps(c.options, capture)} onClick={onClick} />
                : c.caption
                  ? <CompoundButton text={text} secondaryText={c.caption} styles={compoundStyles} onClick={onClick} />
                  : <DefaultButton text={text} styles={styles} onClick={onClick} />
          return <Stack.Item key={c.value}>{button}</Stack.Item>
        })
      return (
        <ButtonsContainer>
          <WithLabel label={text}>
            <Stack horizontal={horizontal} tokens={gap5}>{buttons}</Stack>
          </WithLabel>
        </ButtonsContainer>
      )
    }
  return { render }
})


const toDropdownOption = (c: Option): IDropdownOption => ({ key: c.value, text: String(c.text) })
const toGroupedDropdownOptions = (options: Option[]): IDropdownOption[] => {
  const
    items: IDropdownOption[] = [],
    sepSym = gensym('s'),
    groupSym = gensym('g')
  for (const g of options) {
    if (g.options?.length) {
      if (options.length) items.push({ key: sepSym(), text: '-', itemType: DropdownMenuItemType.Divider })
      items.push({ key: groupSym(), text: String(g.text), itemType: DropdownMenuItemType.Header })
      for (const c of g.options) {
        items.push(toDropdownOption(c))
      }
    } else {
      items.push(toDropdownOption(g))
    }
  }
  return items
}

const XTagPicker = make(({ context, input }: InputProps) => {
  const
    { index, text, options } = input,
    selectedOptions = selectedsOf(input),
    selectedKeys = selectedOptions.map(o => String(o.value)),
    tags: ITag[] = options.map(o => ({ key: o.value, name: String(o.text) })),
    selectedTags = tags.filter(tag => selectedKeys.includes(tag.key as S)),
    capture = (tags: ITag[]) => context.capture(index, tags.map(tag => tag.key)),
    listContainsTagList = (tag: ITag, tagList?: ITag[]) => (!tagList || !tagList.length || tagList.length === 0)
      ? false
      : tagList.some(compareTag => compareTag.key === tag.key),
    suggest = (filterText: string, tagList?: ITag[]): ITag[] =>
      filterText
        ? tags.filter(tag => tag.name.toLowerCase().includes(filterText.toLowerCase()) && !listContainsTagList(tag, tagList))
        : [],
    resolve = (item: ITag) => item.name,
    whenEmpty = () => tags,
    onChange = (tags?: ITag[]) => {
      if (tags) capture(tags)
    },
    render = () => {
      return (
        <WithLabel label={text}>
          <TagPicker
            pickerSuggestionsProps={{
              suggestionsHeaderText: 'Suggestions',
              noResultsFoundText: 'No matches found',
            }}
            onResolveSuggestions={suggest}
            getTextFromItem={resolve}
            onEmptyResolveSuggestions={whenEmpty}
            defaultSelectedItems={selectedTags}
            onChange={onChange}
          />
        </WithLabel>
      )
    }

  capture(selectedTags)

  return { render }
})

const swatchCellSize = 25
const XSwatchPicker = make(({ context, input }: InputProps) => {
  const
    { index, text, options } = input,
    selected = selectedOf(input),
    cells: IColorCellProps[] = options.map(c => ({
      id: String(c.value),
      label: String(c.text),
      color: String(c.value),
    })),
    onChange = (_e: React.FormEvent<HTMLElement>, _id?: S, color?: S) => {
      if (color) context.capture(index, color)
    },
    render = () => {
      return (
        <WithLabel label={text}>
          <SwatchColorPicker
            columnCount={10}
            colorCells={cells}
            cellWidth={swatchCellSize}
            cellHeight={swatchCellSize}
            defaultSelectedId={selected ? String(selected.value) : undefined}
            onChange={onChange}
          />
        </WithLabel>
      )
    }

  if (selected) context.capture(index, selected.value)

  return { render }
})

const selectedOf = ({ value, options }: Input): Option | undefined => value
  ? options.find(c => c.value === value)
  : options.find(c => c.selected)

const selectedsOf = ({ value, options }: Input): Option[] => Array.isArray(value)
  ? options.filter(c => value.includes(c.value))
  : options.filter(c => c.selected)

const XChoiceGroup = make(({ context, input }: InputProps) => {
  const
    { index, text, placeholder, required, options } = input,
    selected = selectedOf(input),
    items: IChoiceGroupOption[] = options.map(({ value, text, icon: iconName }) => ({
      key: String(value),
      text: String(text),
      iconProps: iconName ? { iconName } : undefined,
    })),
    selectedKey = selected ? selected.value : undefined,
    onChange = (_?: React.FormEvent<HTMLElement>, option?: IChoiceGroupOption) => {
      if (option) context.capture(index, option?.key)
    },
    render = () => {
      return (
        <ChoiceGroup
          label={text}
          placeholder={placeholder}
          options={items}
          defaultSelectedKey={selectedKey}
          required={required ? true : false}
          onChange={onChange}
        />
      )
    }

  if (selected) context.capture(index, selected.value)

  return { render }
})


const XMarkdown = make(({ context, input }: InputProps) => {
  const
    ref = React.createRef<HTMLDivElement>(),
    update = () => {
      const { index } = input
      if (index < 0) return

      const el = ref.current
      if (!el) return

      el.querySelectorAll<HTMLAnchorElement>('a[data-jump]').forEach(link => {
        const value = link.getAttribute('data-jump')
        if (value) {
          link.onclick = e => {
            context.capture(index, value)
            context.submit()
            e.preventDefault()
          }
        }
      })
    },
    render = () => {
      return <Markdown ref={ref} dangerouslySetInnerHTML={{ __html: input.text ?? '' }} />
    }
  return { init: update, update, render }
})

const applyBoxStyles = (css: React.CSSProperties, { width, height, margin, padding, grow, shrink, basis }: Stackable) => {
  if (width) {
    if (Array.isArray(width)) {
      switch (width.length) {
        case 1:
          {
            const [min] = width
            if (min) css.minWidth = min
          }
          break
        case 2:
          {
            const [min, max] = width
            if (min) css.minWidth = min
            if (max) css.maxWidth = max
          }
          break
        case 3:
          {
            const [min, max, initial] = width
            if (min) css.minWidth = min
            if (max) css.maxWidth = max
            if (initial) css.width = initial
          }
          break
      }
    } else {
      css.width = width
    }
  }
  if (height) {
    if (Array.isArray(height)) {
      switch (height.length) {
        case 1:
          {
            const [min] = height
            if (min) css.minHeight = min
          }
          break
        case 2:
          {
            const [min, max] = height
            if (min) css.minHeight = min
            if (max) css.maxHeight = max
          }
          break
        case 3:
          {
            const [min, max, initial] = height
            if (min) css.minHeight = min
            if (max) css.maxHeight = max
            if (initial) css.height = initial
          }
          break
      }
    } else {
      css.height = height
    }
  }
  if (margin) css.margin = margin
  if (padding) css.padding = padding
  if (grow) css.flexGrow = grow
  if (shrink) css.flexShrink = shrink
  if (basis) css.flexBasis = basis

  return css
}

const ZoneItemContainer = styled.div`
  box-sizing: border-box;
`

const XZoneItem = ({ stackable, children }: { stackable: Stackable, children: JSX.Element }) => (
  <ZoneItemContainer style={applyBoxStyles({}, stackable)}>
    {children}
  </ZoneItemContainer>
)

const flexStyles: Dict<S> = {
  start: 'flex-start',
  end: 'flex-end',
  between: 'flex-between',
  around: 'flex-around',
  evenly: 'flex-evenly',
}

const toFlexStyle = (s: S): S => flexStyles[s] ?? s

const ZoneContainer = styled.div`
  display: flex;
  box-sizing: border-box;
`

const XZone = ({ context, widgets, stack }: { context: Context, widgets: Widget[], stack: Stacking & Stackable }) => {
  const
    children = widgets.map(widget => {
      const child = (widget.t === WidgetT.Stack)
        ? <XZone context={context} widgets={widget.items} stack={widget} />
        : (widget.t === WidgetT.Input)
          ? <XInput key={widget.xid} context={context} input={widget} />
          : <div>Unknown widget</div>
      return <XZoneItem key={xid()} stackable={widget}>{child}</XZoneItem>
    }),
    { row, justify, align, wrap, gap } = stack,
    css: React.CSSProperties = {
      flexDirection: row ? 'row' : 'column',
      flexWrap: wrap ? 'wrap' : 'nowrap',
      gap: gap ?? 5,
      justifyItems: justify ? toFlexStyle(justify) : undefined,
      alignItems: align ? toFlexStyle(align) : undefined,
      alignContent: wrap ? toFlexStyle(wrap) : undefined,
    }

  return (
    <ZoneContainer style={applyBoxStyles(css, stack)}>
      {children}
    </ZoneContainer>
  )
}

const gap5: IStackTokens = { childrenGap: 5 }

const widgetsHaveActions = (widgets: Widget[]): B => { // recursive
  for (const w of widgets) {
    switch (w.t) {
      case WidgetT.Stack:
        if (widgetsHaveActions(w.items)) return true
        break
      case WidgetT.Input:
        {
          const { mode } = w
          if (mode === 'button' && w.options.length) return true
          if (mode === 'md' && w.index >= 0) return true
        }
        break
    }
  }
  return false
}

const XInput = ({ context, input }: InputProps) => { // recursive 
  const { mode, options, editable, multiple } = input
  switch (mode) {
    case 'md':
      return <XMarkdown context={context} input={input} />
    case 'button':
      return <XButtons context={context} input={input} />
    case 'check':
      return <XCheckList context={context} input={input} />
    case 'color':
      return options.length
        ? <XSwatchPicker context={context} input={input} />
        : <XColorPicker context={context} input={input} />
    case 'date':
      return <XDatePicker context={context} input={input} />
    case 'day':
    case 'month':
    case 'week':
      return <XCalendar context={context} input={input} />
    case 'menu':
      return editable
        ? <XComboBox context={context} input={input} />
        : multiple
          ? <XMultiSelectDropdown context={context} input={input} />
          : <XDropdown context={context} input={input} />
    case 'number':
      return <XSpinButton context={context} input={input} />
    case 'radio':
      return <XChoiceGroup context={context} input={input} />
    case 'range':
      return <XSlider context={context} input={input} />
    case 'rating':
      return <XRating context={context} input={input} />
    case 'tag':
      return <XTagPicker context={context} input={input} />
    case 'text':
      return <XTextField context={context} input={input} />
    case 'time':
      return <XTimePicker context={context} input={input} />
    default:
      return <div>Unknown input</div>
  }
}

const XCommandBar = make(({ send, options }: { send: Send, options: Option[] }) => {
  const
    switchTo = (v: V) => {
      send({ t: MsgType.Switch, d: v })
    },
    items = options.map(o => toContextualMenuItem(o, switchTo)),
    render = () => (
      <CommandBar items={items} />
    )
  return { render }
})

const MenuContainer = styled.div`
  cursor: pointer;
  width: 22px;
  height: 22px;
  display: flex;
  align-items: center;
`
const XMenu = make(({ send, options }: { send: Send, options: Option[] }) => {
  const
    hasMenu = options.length > 0,
    switchTo = (v: V) => {
      send({ t: MsgType.Switch, d: v })
    },
    items = options.map(o => toContextualMenuItem(o, switchTo)),
    containerRef = React.createRef<HTMLDivElement>(),
    showMenuB = box(false),
    showMenu = () => showMenuB(true),
    hideMenu = () => showMenuB(false),
    render = () => {
      const isMenuVisible = showMenuB()
      return (
        <MenuContainer ref={containerRef} onClick={showMenu}>
          {
            hasMenu
              ? isMenuVisible
                ? <GlobalNavButtonActiveIcon />
                : <GlobalNavButtonIcon />
              : <RocketIcon />
          }
          <ContextualMenu
            items={items}
            hidden={!isMenuVisible}
            target={containerRef}
            onItemClick={hideMenu}
            onDismiss={hideMenu}
          />
        </MenuContainer>
      )
    }
  return { render, showMenuB }
})

export const AppContainer = styled.div`
  max-width: 720px;
  background-color: #fff;
  margin: 1rem auto 2rem;
`
const HeaderContainer = styled.div`
  display: flex;
  align-items: center;
  padding: 1rem 2rem;
`
const HeaderTitle = styled.div` 
  font-weight: 700;
  text-transform: uppercase;
  font-size: 1rem;
  color: #555;
  margin-left: 0.5rem;
`
const HeaderSubtitle = styled.div`
  font-weight: 400;
  color: #999;
  margin-left: 0.5rem;
`
const WidgetsContainer = styled.div`
  padding: 1rem 2rem 2rem;
`
const NavBar = styled.div`
  display: flex;
  flex-grow: 1;
  justify-content: flex-end;
`
export const Header = make(({ send, conf }: { send: Send, conf: Conf }) => {
  const
    render = () => {
      return (
        <HeaderContainer>
          <XMenu send={send} options={conf.menu ?? []} />
          <HeaderTitle>{conf.title}</HeaderTitle>
          <HeaderSubtitle>{conf.caption}</HeaderSubtitle>
          <NavBar>
            <XCommandBar send={send} options={conf.nav ?? []} />
          </NavBar>
        </HeaderContainer>
      )
    }
  return { render }
})

export const XWidgets = (props: { send: Send, widgets: Widget[] }) => {
  const
    original = props.widgets,
    hasActions = widgetsHaveActions(original),
    widgets: Widget[] = hasActions ? original : [...original, continueWidget],
    context = newCaptureContext(props.send, [])
  return (
    <WidgetsContainer>
      <XZone context={context} widgets={widgets} stack={{}} />
    </WidgetsContainer>
  )
}
