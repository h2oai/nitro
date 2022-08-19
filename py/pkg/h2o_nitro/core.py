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
from typing import Callable, Optional, Sequence, Set, Tuple, List, Dict, Union, Iterable
from types import FunctionType
import random
import asyncio
import collections
from collections import OrderedDict
from enum import IntEnum
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
Locale = Dict[str, str]
Locales = Dict[str, Locale]


class RemoteError(Exception):
    pass


class ContextSwitchError(Exception):
    def __init__(self, method: str):
        super().__init__('Context switched')
        self.method = method


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


class Option:
    def __init__(
            self,
            value: Union[V, Callable],
            text: Optional[str] = None,
            name: Optional[str] = None,
            icon: Optional[str] = None,
            caption: Optional[str] = None,
            selected: Optional[bool] = None,
            options: Optional['Options'] = None,
    ):
        # If value is a function, use it as the delegate.
        self.delegate = value if isinstance(value, FunctionType) else None
        # If value was a function, use one of these as the value:
        # - option's name, if available.
        # - function's name ("module_name.function_name")
        self.value = value if self.delegate is None else name if name is not None else _qual_name_of(self.delegate)
        self.text = text
        self.name = name
        self.icon = icon
        self.caption = caption
        self.selected = selected
        self.options = options

    def dump(self) -> dict:
        return _clean(dict(
            value=self.value,
            text=self.text,
            name=self.name,
            icon=self.icon,
            caption=self.caption,
            selected=self.selected,
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
            data: Optional[dict] = None,
            halt: Optional[bool] = None,
            title: Optional[str] = None,
            caption: Optional[str] = None,
            hint: Optional[str] = None,
            help: Optional[str] = None,
            popup: Optional[bool] = None,
            style: Optional[str] = None,
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
            path: Optional[str] = None,
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
        self.popup = popup
        self.style = style
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
        self.path = path
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
            data: Optional[dict] = None,
            halt: Optional[bool] = None,
            title: Optional[str] = None,
            caption: Optional[str] = None,
            hint: Optional[str] = None,
            help: Optional[str] = None,
            popup: Optional[bool] = None,
            style: Optional[str] = None,
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
            path: Optional[str] = None,
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
            popup=self.popup if popup is None else popup,
            style=self.style if style is None else f'{self.style} {style}',  # Additive!
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
            path=self.path if path is None else path,
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
            popup=self.popup,
            style=self.style,
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
            path=self.path,
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
            popup=self.popup,
            style=self.style,
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
            path=self.path,
            error=self.error,
            lines=self.lines,
            ignore=self.ignore,
        ))


box = Box


def row(
        *items: Item,
        name: Optional[str] = None,
        style: Optional[str] = None,
        image: Optional[str] = None,
        path: Optional[str] = None,
) -> Box:
    return Box(
        *items,
        mode='row',
        name=name,
        style=style,
        image=image,
        path=path,
    )


def col(
        *items: Item,
        name: Optional[str] = None,
        style: Optional[str] = None,
        image: Optional[str] = None,
        path: Optional[str] = None,
) -> Box:
    return Box(
        *items,
        mode='col',
        name=name,
        style=style,
        image=image,
        path=path,
    )


def _collect_delegates(d: Dict[str, FunctionType], options: Optional[Sequence[Option]] = None):
    if options is None:
        return
    for opt in options:
        if opt.delegate:
            d[opt.value] = opt.delegate
        if opt.options:
            _collect_delegates(d, opt.options)


def _interpret(msg, expected_type: int):
    if isinstance(msg, dict):
        t = msg.get('t')

        if t == _MsgType.Error:
            code = msg.get('code')
            text = msg.get('text')
            raise RemoteError(f'{text} (code {code})')

        if t == _MsgType.Switch:
            method = msg.get('method')
            raise ContextSwitchError(method)

        if (expected_type > -1) and t != expected_type:
            raise ProtocolError(400, f'unexpected message: want {expected_type}, got {t}')

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


def _marshal_error(code: int, text: str):
    return _marshal(dict(t=_MsgType.Error, code=code, text=text))


def _marshal_set(
        title: str = None,
        caption: str = None,
        menu: Optional[Sequence[Option]] = None,
        nav: Optional[Sequence[Option]] = None,
        theme: Optional[Theme] = None,
        plugins: Optional[Iterable[Plugin]] = None,
        locale: Optional[Locale] = None,
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
            plugins=_dump(plugins),
            locale=locale,
            mode=mode,
        ))))


def _marshal_switch(method: Union[V, Callable], params: Optional[dict]):
    return _marshal(_clean(dict(
        t=_MsgType.Switch,
        method='#!' + _qual_name_of(method) if isinstance(method, FunctionType) else str(method),
        params=_clean(params),
    )))


def _get_locale(locales: Optional[Locales], locale: Optional[str], fallback: str) -> Optional[Locale]:
    if locales is None or locale is None:
        return None
    return locales.get(locale) or locales.get(fallback)


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
            plugins: Optional[Iterable[Plugin]] = None,
            locales: Optional[Locales] = None,
            default_locale: Optional[str] = None,
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
        self._plugins = plugins
        self._locales = locales
        self._default_locale = default_locale or 'en-US'

        self._delegates: Dict[str, FunctionType] = dict()
        _collect_delegates(self._delegates, self._menu)
        _collect_delegates(self._delegates, self._nav)
        _collect_delegates(self._delegates, self._routes)

    def _ack(self, mode: Optional[str] = None, locale: Optional[str] = None):
        return _marshal_set(
            title=self._title,
            caption=self._caption,
            menu=self._menu,
            nav=self._nav,
            theme=self._theme,
            plugins=self._plugins,
            locale=_get_locale(self._locales, locale, self._default_locale),
            mode=mode,
        )

    def __getitem__(self, key):
        return self.context.get(key)

    def __setitem__(self, key, value):
        self.context[key] = value

    def _delegate_for(self, key: str):
        d = self._delegates.get(key)
        if d is None:
            raise ProtocolError(404, f'Delegate not found: "{key}"')
        return d


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
            plugins: Optional[Iterable[Plugin]] = None,
            locales: Optional[Locales] = None,
            default_locale: Optional[str] = None,
    ):
        super().__init__(delegate, context, send, recv, title, caption, menu, nav, routes, theme, plugins, locales,
                         default_locale)

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
            plugins=self._plugins,
            locales=self._locales,
            default_locale=self._default_locale
        )._run()

    def _run(self):
        # Handshake
        method, mode, locale = self._read(_MsgType.Join)
        self._send(self._ack(mode, locale))

        # Event loop
        while True:
            try:
                (self._delegate_for(method) if method else self._delegate)(self)
            except ContextSwitchError as cse:
                method = cse.method
            except ProtocolError as pe:
                self._send(_marshal_error(pe.code, pe.text))
            except InterruptError:
                return

    def _write(self, read: bool, b: Box, edit: Edit):
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
        self._send(_marshal_set(
            title=title,
            caption=caption,
            menu=menu,
            nav=nav,
            theme=theme,
        ))

    def jump(
            self,
            method: Union[V, Callable],
            target: Optional[str] = None,
            popup: Optional[bool] = None,
            width: Optional[int] = None,
            height: Optional[int] = None,
            left: Optional[int] = None,
            top: Optional[int] = None,
    ):
        self._send(_marshal_switch(method, dict(
            target=target,
            popup=popup,
            width=width,
            height=height,
            left=left,
            top=top,
        )))
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
            plugins: Optional[Iterable[Plugin]] = None,
            locales: Optional[Locales] = None,
            default_locale: Optional[str] = None,
    ):
        super().__init__(delegate, context, send, recv, title, caption, menu, nav, routes, theme, plugins, locales,
                         default_locale)

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
            plugins=self._plugins,
            locales=self._locales,
            default_locale=self._default_locale,
        )._run()

    async def _run(self):
        # Handshake
        method, mode, locale = await self._read(_MsgType.Join)
        await self._send(self._ack(mode, locale))

        # Event loop
        while True:
            try:
                await (self._delegate_for(method) if method else self._delegate)(self)
            except ContextSwitchError as cse:
                method = cse.method
            except ProtocolError as pe:
                await self._send(_marshal_error(pe.code, pe.text))
            except InterruptError:
                return

    async def _read(self, expected: int):
        m = await self._recv()
        if m:
            return _interpret(_unmarshal(m), expected)
        raise InterruptError()

    async def _write(self, read: bool, b: Box, edit: Edit):
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
        await self._send(_marshal_set(
            title=title,
            caption=caption,
            menu=menu,
            nav=nav,
            theme=theme,
        ))

    async def jump(
            self,
            method: Union[V, Callable],
            target: Optional[str] = None,
            popup: Optional[bool] = None,
            width: Optional[int] = None,
            height: Optional[int] = None,
            left: Optional[int] = None,
            top: Optional[int] = None,
    ):
        await self._send(_marshal_switch(method, dict(
            target=target,
            popup=popup,
            width=width,
            height=height,
            left=left,
            top=top,
        )))
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


# noinspection SpellCheckingInspection
_lorem = '''
lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna 
aliqua ut enim ad minim veniam quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat 
duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur 
excepteur sint occaecat cupidatat non proident sunt in culpa qui officia deserunt mollit anim id est laborum
'''

# noinspection SpellCheckingInspection
_lorems = set([w.strip() for w in _lorem.split(' ')])
_long_lorems = set([w for w in _lorems if len(w) > 4])


# noinspection PyShadowingBuiltins
def _sentence(min: int, max: int):
    return ' '.join(random.sample(_lorems, random.randint(min, max))).capitalize() + '.'


def lorem(sentences: Optional[int] = None, words: Optional[int] = None):
    if words is not None:
        return ' '.join(random.sample(_long_lorems, words)).title()
    if sentences is None:
        return _sentence(4, 5)
    lines = [_sentence(5, 9) for _ in range(sentences)]
    return ' '.join(lines)
