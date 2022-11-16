# Copyright 2022 H2O.ai, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import asyncio
import collections
import traceback
import urllib.parse
from collections import OrderedDict
from enum import IntEnum
from types import FunctionType
from typing import Callable, Optional, Sequence, Set, Tuple, List, Dict, Union, Iterable

from .version import __version__

# noinspection PyBroadException
try:
    import msgpack


    def _marshal(d: dict):
        return msgpack.packb(d)


    def _unmarshal(b) -> dict:
        return msgpack.unpackb(b)

except:
    import json


    def _marshal(d: dict):
        return json.dumps(d)


    def _unmarshal(b) -> dict:
        return json.loads(b)

__xid = 0


def _xid() -> str:
    global __xid
    __xid += 1
    return f'p{__xid}'


def _qual_name_of(f: FunctionType) -> str:
    return f'{f.__module__}.{f.__qualname__}'


class _MsgType(IntEnum):
    Error = 1
    Join = 2
    Switch = 3
    Input = 4
    Output = 5
    Set = 6


_primitive = (bool, int, float, str)
Primitive = Union[bool, int, float, str]


class RemoteError(Exception):
    pass


class ContextSwitchError(Exception):
    def __init__(self, method: str, params: dict = None):
        super().__init__('Context switched')
        self.method = method
        self.params = params


class ProtocolError(Exception):
    def __init__(self, code: int, text: str):
        super().__init__(f'{text} (code {code})')
        self.code = code
        self.text = text


class InterruptError(Exception):
    def __init__(self):
        super().__init__('Interrupted')


def _dump(x):  # recursive
    if isinstance(x, OrderedDict):
        return _dump([(k, v) for k, v in x.items()])
    if isinstance(x, (tuple, list, set)):
        return [_dump(e) for e in x]
    if callable(getattr(x, 'dump', None)):
        return x.dump()
    return x


def _clean(d: dict) -> dict:
    return {k: v for k, v in d.items() if v is not None}


N = Union[int, float]
V = Union[N, str]
P = Union[str, int, float, bool]
Data = Union[
    Dict[str, Union[P, 'Data']],
    Sequence[Union[P, 'Data']],
]
Locale = Union[str, Sequence[str]]
Length = Union[str, int, float]

Sizing = Union[
    Length,
    Tuple[Length],
    Tuple[Length, Length],
    Tuple[Length, Length, Length],
]


class Header:
    def __init__(
            self,
            text: str,
            mode: Optional[str] = None,
            style: Optional[str] = None,
            icon: Optional[str] = None,
    ):
        self.text = text
        self.mode = mode
        self.style = style
        self.icon = icon

    def dump(self) -> dict:
        return _clean(dict(
            text=self.text,
            mode=self.mode,
            style=self.style,
            icon=self.icon,
        ))


header = Header

Headers = Union[
    Tuple[Header, ...],
    List[Header],
    Set[Header],
]

Delegate = Union[V, Callable]


def _address_of(delegate: Delegate) -> str:
    return f'#!{urllib.parse.quote(_qual_name_of(delegate))}' if isinstance(delegate, FunctionType) else str(delegate)


def link(delegate: Delegate, **kwargs) -> str:
    method = _address_of(delegate)
    if len(kwargs) == 0:
        return method
    params = '&'.join([f'{k}={urllib.parse.quote(str(v))}' for k, v in kwargs.items()])
    return f'{method}?{params}'


class Option:
    def __init__(
            self,
            value: Delegate,
            text: Optional[str] = None,
            name: Optional[str] = None,
            icon: Optional[str] = None,
            caption: Optional[str] = None,
            hotkey: Optional[str] = None,
            selected: Optional[bool] = None,
            disabled: Optional[bool] = None,
            options: Optional['Options'] = None,
    ):
        self.value = value
        self.text = text
        self.name = name
        self.icon = icon
        self.caption = caption
        self.hotkey = hotkey
        self.selected = selected
        self.disabled = disabled
        self.options = options

    def dump(self) -> dict:
        return _clean(dict(
            value=self.value,
            text=self.text,
            name=self.name,
            icon=self.icon,
            caption=self.caption,
            hotkey=self.hotkey,
            selected=self.selected,
            disabled=self.disabled,
            options=_dump(self.options),
        ))


option = Option

OptionPair = Tuple[V, str]
Options = Union[
    str,
    Tuple[Primitive, ...],
    List[Primitive],
    Set[Primitive],
    Dict[Primitive, V],
    Tuple[Option, ...],
    List[Option],
    Set[Option],
    Tuple[OptionPair, ...],
    List[OptionPair],
    Set[OptionPair],
]

Item = Union[str, 'Box', Options]
Items = Union[List[Item], Tuple[Item, ...]]
Range = Union[
    Tuple[V, V],
    Tuple[N, N],
    Tuple[N, N, N],
    Tuple[N, N, N, int],
    List[V],
]
Value = Union[
    bool,
    V,
    Tuple[V, V],
    List[V],
]


class Theme:
    def __init__(
            self,
            mode: Optional[str] = None,
            accent: Optional[str] = None,
    ):
        self.mode = mode
        self.accent = accent

    def dump(self) -> dict:
        return dict(
            mode=self.mode,
            accent=self.accent,
        )


class Script:
    # noinspection PyShadowingBuiltins
    def __init__(
            self,
            source: str,
            type: Optional[str] = None,
            asynchronous: Optional[bool] = None,
            cross_origin: Optional[str] = None,
            referrer_policy: Optional[str] = None,
            integrity: Optional[str] = None
    ):
        self.source = source
        self.type = type
        self.asynchronous = asynchronous
        self.cross_origin = cross_origin
        self.referrer_policy = referrer_policy
        self.integrity = integrity

    def dump(self) -> dict:
        return _clean(dict(
            source=self.source,
            type=self.type,
            asynchronous=self.asynchronous,
            cross_origin=self.cross_origin,
            referrer_policy=self.referrer_policy,
            integrity=self.integrity
        ))


class Translation:
    def __init__(self, locale: str, strings: Dict[str, str]):
        self.locale = locale
        self.strings = strings

    def dump(self) -> dict:
        return dict(
            locale=self.locale,
            strings=self.strings,
        )


class Resources:
    def __init__(self, locale: str, translations: Sequence[Translation]):
        self.locale = locale
        self.translations = translations

    def dump(self) -> dict:
        return dict(
            locale=self.locale,
            translations=_dump(self.translations),
        )


class Plugin:
    def __init__(self, name: str, scripts: Optional[Iterable[Script]] = None):
        self.name = name
        self.scripts = scripts

    def dump(self) -> dict:
        return dict(
            name=self.name,
            scripts=_dump(self.scripts),
        )


class Box:
    # noinspection PyShadowingBuiltins
    def __init__(
            self,
            *items,
            name: Optional[str] = None,
            mode: Optional[str] = None,
            value: Optional[Value] = None,
            options: Optional[Options] = None,
            headers: Optional[Headers] = None,
            data: Optional[Data] = None,
            halt: Optional[bool] = None,
            title: Optional[str] = None,
            caption: Optional[str] = None,
            hint: Optional[str] = None,
            help: Optional[str] = None,
            locale: Optional[Locale] = None,
            hotkey: Optional[str] = None,
            popup: Optional[bool] = None,
            style: Optional[str] = None,
            disabled: Optional[bool] = None,
            image: Optional[str] = None,
            icon: Optional[str] = None,
            min: Optional[V] = None,
            max: Optional[V] = None,
            step: Optional[N] = None,
            precision: Optional[int] = None,
            range: Optional[Range] = None,
            mask: Optional[str] = None,
            prefix: Optional[str] = None,
            suffix: Optional[str] = None,
            placeholder: Optional[str] = None,
            link: Optional[Delegate] = None,
            error: Optional[str] = None,
            lines: Optional[int] = None,
            ignore: Optional[bool] = None,
    ):
        self.xid = _xid()
        self.name = name
        self.mode = mode
        self.value = value
        self.options = options
        self.headers = headers
        self.items = items
        self.data = data
        self.halt = halt
        self.title = title
        self.caption = caption
        self.hint = hint
        self.help = help
        self.locale = locale
        self.hotkey = hotkey
        self.popup = popup
        self.style = style
        self.disabled = disabled
        self.image = image
        self.icon = icon
        self.min = min
        self.max = max
        self.step = step
        self.precision = precision
        self.range = range
        self.mask = mask
        self.prefix = prefix
        self.suffix = suffix
        self.placeholder = placeholder
        self.link = link
        self.error = error
        self.lines = lines
        self.ignore = ignore

    def __call__(
            self,
            *items,
            name: Optional[str] = None,
            mode: Optional[str] = None,
            value: Optional[Value] = None,
            options: Optional[Options] = None,
            headers: Optional[Headers] = None,
            data: Optional[Data] = None,
            halt: Optional[bool] = None,
            title: Optional[str] = None,
            caption: Optional[str] = None,
            hint: Optional[str] = None,
            help: Optional[str] = None,
            locale: Optional[Locale] = None,
            hotkey: Optional[str] = None,
            popup: Optional[bool] = None,
            style: Optional[str] = None,
            disabled: Optional[bool] = None,
            image: Optional[str] = None,
            icon: Optional[str] = None,
            min: Optional[V] = None,
            max: Optional[V] = None,
            step: Optional[N] = None,
            precision: Optional[int] = None,
            range: Optional[Range] = None,
            mask: Optional[str] = None,
            prefix: Optional[str] = None,
            suffix: Optional[str] = None,
            placeholder: Optional[str] = None,
            link: Optional[str] = None,
            error: Optional[str] = None,
            lines: Optional[int] = None,
            ignore: Optional[bool] = None,
    ):
        return box(
            *items,
            name=self.name if name is None else name,
            mode=self.mode if mode is None else mode,
            value=self.value if value is None else value,
            options=self.options if options is None else options,
            headers=self.headers if headers is None else headers,
            data=self.data if data is None else data,
            halt=self.halt if halt is None else halt,
            title=self.title if title is None else title,
            caption=self.caption if caption is None else caption,
            hint=self.hint if hint is None else hint,
            help=self.help if help is None else help,
            locale=self.locale if locale is None else locale,
            hotkey=self.hotkey if hotkey is None else hotkey,
            popup=self.popup if popup is None else popup,
            style=self.style if style is None else f'{self.style} {style}',  # Additive!
            disabled=self.disabled if disabled is None else disabled,
            image=self.image if image is None else image,
            icon=self.icon if icon is None else icon,
            min=self.min if min is None else min,
            max=self.max if max is None else max,
            step=self.step if step is None else step,
            precision=self.precision if precision is None else precision,
            range=self.range if range is None else range,
            mask=self.mask if mask is None else mask,
            prefix=self.prefix if prefix is None else prefix,
            suffix=self.suffix if suffix is None else suffix,
            placeholder=self.placeholder if placeholder is None else placeholder,
            link=self.link if link is None else link,
            error=self.error if error is None else error,
            lines=self.lines if lines is None else lines,
            ignore=self.ignore if ignore is None else ignore,
        )

    def clone(self):
        return Box(
            *self.items,
            name=self.name,
            mode=self.mode,
            value=self.value,
            options=self.options,
            headers=self.headers,
            data=self.data,
            halt=self.halt,
            title=self.title,
            caption=self.caption,
            hint=self.hint,
            help=self.help,
            locale=self.locale,
            hotkey=self.hotkey,
            popup=self.popup,
            style=self.style,
            disabled=self.disabled,
            image=self.image,
            icon=self.icon,
            min=self.min,
            max=self.max,
            step=self.step,
            precision=self.precision,
            range=self.range,
            mask=self.mask,
            prefix=self.prefix,
            suffix=self.suffix,
            placeholder=self.placeholder,
            link=self.link,
            error=self.error,
            lines=self.lines,
            ignore=self.ignore,
        )

    def __truediv__(self, style: str):
        b = self.clone()
        b.style = style if b.style is None else f'{b.style} {style}'
        return b

    def dump(self) -> dict:
        return _clean(dict(
            xid=self.xid,
            name=self.name,
            mode=self.mode,
            value=self.value,
            options=_dump(self.options),
            headers=_dump(self.headers),
            items=_dump(self.items),
            data=_dump(self.data),
            halt=self.halt,
            title=self.title,
            caption=self.caption,
            hint=self.hint,
            help=self.help,
            locale=self.locale,
            hotkey=self.hotkey,
            popup=self.popup,
            style=self.style,
            disabled=self.disabled,
            image=self.image,
            icon=self.icon,
            min=self.min,
            max=self.max,
            step=self.step,
            precision=self.precision,
            range=self.range,
            mask=self.mask,
            prefix=self.prefix,
            suffix=self.suffix,
            placeholder=self.placeholder,
            link=self.link,
            error=self.error,
            lines=self.lines,
            ignore=self.ignore,
        ))


box = Box


def row(
        *items: Item,
        name: Optional[str] = None,
        mode: Optional[str] = None,
        style: Optional[str] = None,
        image: Optional[str] = None,
        link: Optional[str] = None,
) -> Box:
    return Box(
        *items,
        mode=f'row {mode}' if mode else 'row',
        name=name,
        style=style,
        image=image,
        link=link,
    )


def col(
        *items: Item,
        name: Optional[str] = None,
        mode: Optional[str] = None,
        style: Optional[str] = None,
        image: Optional[str] = None,
        link: Optional[str] = None,
) -> Box:
    return Box(
        *items,
        mode=f'col {mode}' if mode else 'col',
        name=name,
        style=style,
        image=image,
        link=link,
    )


def _interpret(msg, expected_type: int):
    if isinstance(msg, dict):
        t = msg.get('t')

        if t == _MsgType.Error:
            code = msg.get('code')
            text = msg.get('text')
            raise RemoteError(f'{text} (code {code})')

        if t == _MsgType.Switch:
            method = msg.get('method')
            params = msg.get('params')
            raise ContextSwitchError(method, params)

        if (expected_type > -1) and t != expected_type:
            raise ProtocolError(409, f'unexpected message: want {expected_type}, got {t}')

        if t == _MsgType.Input:
            inputs = msg.get('inputs')

            n = len(inputs)
            if n == 0:
                return
            elif n == 1:
                return _unwrap_input(inputs[0])
            else:
                # Convert list to tuple
                return tuple([_unwrap_input(e) for e in inputs])

        if t == _MsgType.Join:
            client = msg.get('client')
            locale = client.get('locale') if client else None
            method = msg.get('method')
            params = msg.get('params')
            mode = params.get('mode') if params else None
            return method, mode, locale

        raise ProtocolError(400, f'unknown message type {t}')
    raise ProtocolError(400, f'unknown message format: want dict, got {type(msg)}')


def _unwrap_input(x):
    return None if x is None else x[1]


def _marshal_error(code: int, text: str, trace: Optional[str] = None):
    return _marshal(_clean(dict(t=_MsgType.Error, code=code, text=text, trace=trace)))


def _marshal_set(
        title: str = None,
        caption: str = None,
        menu: Optional[Sequence[Option]] = None,
        nav: Optional[Sequence[Option]] = None,
        theme: Optional[Theme] = None,
        layout: Optional[Box] = None,
        plugins: Optional[Iterable[Plugin]] = None,
        help: Optional[Dict[str, str]] = None,
        resources: Optional[Resources] = None,
        mode: Optional[str] = None,
):
    return _marshal(dict(
        t=_MsgType.Set,
        settings=_clean(dict(
            title=title,
            caption=caption,
            menu=_dump(menu),
            nav=_dump(nav),
            theme=_dump(theme),
            layout=_dump(layout),
            plugins=_dump(plugins),
            help=_dump(help),
            resources=_dump(resources),
            mode=mode,
        ))))


def _marshal_switch(method: str, params: Optional[dict]):
    return _marshal(_clean(dict(
        t=_MsgType.Switch,
        method=method,
        params=_clean(params),
    )))


def _lookup_resources(
        lookup: Optional[Dict[str, Dict[str, str]]],
        *locales: Optional[str],
) -> Optional[Translation]:
    if lookup:
        for locale in locales:
            r = lookup.get(locale)
            if r:
                return Translation(locale, r)
    return None


def _to_resources(locale: str, lookup: Optional[Dict[str, Dict[str, str]]]):
    translations = [Translation(l, r) for l, r in lookup.items()] if lookup else None
    return Resources(locale, translations)


TranslateLocale = Callable[[str], str]
LocaleOrTranslate = Union[str, TranslateLocale]


def _translate_locale(translate: LocaleOrTranslate, locale: str) -> str:
    if translate:
        if isinstance(translate, str):
            return translate
        return translate(locale)
    return locale or 'en-US'


class Delegator:
    def __init__(self):
        self._delegates: Dict[str, FunctionType] = dict()

    def _add(self, f: FunctionType) -> str:
        a = _address_of(f)
        self._delegates[a[2:]] = f
        return a

    def scan(self, b: Box):
        if isinstance(b, Box):
            if isinstance(b.link, FunctionType):
                b.link = self._add(b.link)
            if b.items:
                for c in b.items:
                    self.scan(c)
            self.scan_opts(b.options)

    def scan_opts(self, options: Optional[Sequence[Option]] = None):
        if options:
            for o in options:
                if isinstance(o, Option):
                    if isinstance(o.value, FunctionType):
                        o.value = self._add(o.value)
                    self.scan_opts(o.options)

    def lookup(self, key: str):
        d = self._delegates.get(key)
        if d is None:
            raise ProtocolError(404, f'Delegate not found: "{key}"')
        return d


class _View:
    def __init__(
            self,
            delegate: Callable,
            context: any = None,
            send: Optional[Callable] = None,
            recv: Optional[Callable] = None,
            title: str = 'H2O Nitro',
            caption: str = f'v{__version__}',
            menu: Optional[Sequence[Option]] = None,
            nav: Optional[Sequence[Option]] = None,
            routes: Optional[Sequence[Option]] = None,
            theme: Optional[Theme] = None,
            layout: Optional[Box] = None,
            plugins: Optional[Iterable[Plugin]] = None,
            help: Optional[Dict[str, str]] = None,
            resources: Optional[Dict[str, Dict[str, str]]] = None,
            locale: Optional[LocaleOrTranslate] = None,
            delegator: Optional[Delegator] = None,
    ):
        self._delegate = delegate
        self.context = context or {}
        self._send = send
        self._recv = recv
        self._title = title
        self._caption = caption
        self._menu = menu
        self._nav = nav
        self._routes = routes
        self._theme = theme
        self._layout = layout
        self._plugins = plugins
        self._help = help
        self._resources = resources
        self._locale = locale
        # TODO clone instead? (to account for view-local closures)
        self._delegator = delegator or Delegator()

        for options in [self._menu, self._nav, self._routes]:
            self._delegator.scan_opts(options)

    def _ack(self, mode: Optional[str] = None, locale: Optional[str] = None):
        resources = _to_resources(locale, self._resources)
        return _marshal_set(
            title=self._title,
            caption=self._caption,
            menu=self._menu,
            nav=self._nav,
            theme=self._theme,
            layout=self._layout,
            plugins=self._plugins,
            help=self._help,
            resources=resources,
            mode=mode,
        )

    def __getitem__(self, key):
        return self.context.get(key)

    def __setitem__(self, key, value):
        self.context[key] = value


class EditType(IntEnum):
    Insert = 1
    Update = 2
    Remove = 3


class Edit:
    # noinspection PyShadowingBuiltins
    def __init__(self, type: EditType, selector: Optional[str] = None):
        self.t = type
        self.s = selector

    def dump(self) -> dict:
        return _clean(dict(t=self.t, s=self.s))


class View(_View):
    def __init__(
            self,
            delegate: Callable,
            context: any = None,
            send: Optional[Callable] = None,
            recv: Optional[Callable] = None,
            title: str = None,
            caption: str = None,
            menu: Optional[Sequence[Option]] = None,
            nav: Optional[Sequence[Option]] = None,
            routes: Optional[Sequence[Option]] = None,
            theme: Optional[Theme] = None,
            layout: Optional[Box] = None,
            plugins: Optional[Iterable[Plugin]] = None,
            help: Optional[Dict[str, str]] = None,
            resources: Optional[Dict[str, Dict[str, str]]] = None,
            locale: Optional[LocaleOrTranslate] = None,
            delegator: Optional[Delegator] = None,
    ):
        super().__init__(delegate, context, send, recv, title, caption, menu, nav, routes, theme, layout, plugins,
                         help, resources, locale, delegator)

    def serve(self, send: Callable, recv: Callable, context: any = None):
        View(
            delegate=self._delegate,
            context=context,
            send=send,
            recv=recv,
            title=self._title,
            caption=self._caption,
            menu=self._menu,
            nav=self._nav,
            routes=self._routes,
            theme=self._theme,
            layout=self._layout,
            plugins=self._plugins,
            help=self._help,
            resources=self._resources,
            locale=self._locale,
            delegator=self._delegator,
        )._run()

    def _run(self):
        # Handshake
        method, mode, locale = self._read(_MsgType.Join)
        self._send(self._ack(mode, _translate_locale(self._locale, locale)))

        # Event loop
        params = None
        while True:
            try:
                if method:
                    delegate = self._delegator.lookup(method)
                    if params:
                        delegate(self, **params)
                    else:
                        delegate(self)
                else:
                    self._delegate(self)
            except ContextSwitchError as cse:
                method, params = cse.method, cse.params
            except InterruptError:
                return
            except Exception as e:
                self._send(_marshal_error(0, str(e), traceback.format_exc()))
                return

    def _write(self, read: bool, b: Box, edit: Edit):
        self._delegator.scan(b)
        self._send(_marshal(_clean(dict(t=_MsgType.Output, box=b.dump(), edit=edit.dump() if edit else None))))
        if read:
            return self._read(_MsgType.Input)

    def _read(self, expected: int):
        m = self._recv()
        if m:
            return _interpret(_unmarshal(m), expected)
        raise InterruptError()

    def set(
            self,
            title: str = None,
            caption: str = None,
            menu: Optional[Sequence[Option]] = None,
            nav: Optional[Sequence[Option]] = None,
            theme: Optional[Theme] = None,
    ):
        for options in [menu, nav]:
            self._delegator.scan_opts(options)

        self._send(_marshal_set(
            title=title,
            caption=caption,
            menu=menu,
            nav=nav,
            theme=theme,
        ))

    def jump(
            self,
            method: Delegate,
            target: Optional[str] = None,
            popup: Optional[bool] = None,
            width: Optional[int] = None,
            height: Optional[int] = None,
            left: Optional[int] = None,
            top: Optional[int] = None,
    ):
        method = _address_of(method)
        self._send(_marshal_switch(method, dict(
            target=target,
            popup=popup,
            width=width,
            height=height,
            left=left,
            top=top,
        )))
        # Don't wait for ack if redirect
        if target is None and method.startswith('#'):
            self._read(_MsgType.Switch)

    def __call__(
            self,
            *items: Item,
            read=True,
            at: Optional[str] = None,
            halt: Optional[bool] = None,
            title: Optional[str] = None,
            popup: Optional[bool] = None,
            style: Optional[str] = None,
    ):
        b = Box(*items, mode='col', halt=halt, title=title, popup=popup, style=style)
        return self._write(read, b, Edit(EditType.Update, at) if at else None)

    def add(self, *items: Item, read=True, at: Optional[str] = None):
        return self._write(read, Box(*items, mode='col'), Edit(EditType.Insert, at))

    def clear(self, read=True, at: Optional[str] = None):
        return self._write(read, Box(mode='col'), Edit(EditType.Remove, at))


class AsyncView(_View):
    def __init__(
            self,
            delegate: Callable,
            context: any = None,
            send: Optional[Callable] = None,
            recv: Optional[Callable] = None,
            title: str = None,
            caption: str = None,
            menu: Optional[Sequence[Option]] = None,
            nav: Optional[Sequence[Option]] = None,
            routes: Optional[Sequence[Option]] = None,
            theme: Optional[Theme] = None,
            layout: Optional[Box] = None,
            plugins: Optional[Iterable[Plugin]] = None,
            help: Optional[Dict[str, str]] = None,
            resources: Optional[Dict[str, Dict[str, str]]] = None,
            locale: Optional[LocaleOrTranslate] = None,
            delegator: Optional[Delegator] = None,
    ):
        super().__init__(delegate, context, send, recv, title, caption, menu, nav, routes, theme, layout, plugins,
                         help, resources, locale, delegator)

    async def serve(self, send: Callable, recv: Callable, context: any = None):
        await AsyncView(
            delegate=self._delegate,
            context=context,
            send=send,
            recv=recv,
            title=self._title,
            caption=self._caption,
            menu=self._menu,
            nav=self._nav,
            routes=self._routes,
            theme=self._theme,
            layout=self._layout,
            plugins=self._plugins,
            help=self._help,
            resources=self._resources,
            locale=self._locale,
            delegator=self._delegator,
        )._run()

    async def _run(self):
        # Handshake
        method, mode, locale = await self._read(_MsgType.Join)
        await self._send(self._ack(mode, _translate_locale(self._locale, locale)))

        # Event loop
        params = None
        while True:
            try:
                if method:
                    delegate = self._delegator.lookup(method)
                    if params:
                        await delegate(self, **params)
                    else:
                        await delegate(self)
                else:
                    await self._delegate(self)
            except ContextSwitchError as cse:
                method, params = cse.method, cse.params
            except InterruptError:
                return
            except Exception as e:
                await self._send(_marshal_error(0, str(e), traceback.format_exc()))
                return

    async def _read(self, expected: int):
        m = await self._recv()
        if m:
            return _interpret(_unmarshal(m), expected)
        raise InterruptError()

    async def _write(self, read: bool, b: Box, edit: Edit):
        self._delegator.scan(b)
        await self._send(_marshal(_clean(dict(t=_MsgType.Output, box=b.dump(), edit=edit.dump() if edit else None))))
        if read:
            return await self._read(_MsgType.Input)

    async def set(
            self,
            title: str = None,
            caption: str = None,
            menu: Optional[Sequence[Option]] = None,
            nav: Optional[Sequence[Option]] = None,
            theme: Optional[Theme] = None,
    ):
        for options in [menu, nav]:
            self._delegator.scan_opts(options)

        await self._send(_marshal_set(
            title=title,
            caption=caption,
            menu=menu,
            nav=nav,
            theme=theme,
        ))

    async def jump(
            self,
            method: Delegate,
            target: Optional[str] = None,
            popup: Optional[bool] = None,
            width: Optional[int] = None,
            height: Optional[int] = None,
            left: Optional[int] = None,
            top: Optional[int] = None,
    ):
        method = _address_of(method)
        await self._send(_marshal_switch(method, dict(
            target=target,
            popup=popup,
            width=width,
            height=height,
            left=left,
            top=top,
        )))
        # Don't wait for ack if redirect
        if target is None and method.startswith('#'):
            await self._read(_MsgType.Switch)

    async def __call__(
            self,
            *items: Item,
            read=True,
            at: Optional[str] = None,
            halt: Optional[bool] = None,
            title: Optional[str] = None,
            popup: Optional[bool] = None,
            style: Optional[str] = None,
    ):
        b = Box(*items, mode='col', halt=halt, title=title, popup=popup, style=style)
        return await self._write(read, b, Edit(EditType.Update, at) if at else None)

    async def add(self, *items: Item, read=True, at: Optional[str] = None):
        return await self._write(read, Box(*items, mode='col'), Edit(EditType.Insert, at))

    async def clear(self, read=True, at: Optional[str] = None):
        return await self._write(read, Box(mode='col'), Edit(EditType.Remove, at))


class Duplex:
    def __init__(self):
        self._input = collections.deque()
        self._output = collections.deque()

    async def send(self, x):
        self._output.append(x)

    async def recv(self):
        while True:
            if len(self._input):
                return self._input.popleft()
            await asyncio.sleep(0.1)

    def write(self, x):
        self._input.append(x)

    def read(self):
        return self._output.popleft() if len(self._output) else None
