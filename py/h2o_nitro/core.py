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

import random
from pathlib import Path
from typing import Optional, Sequence, Set, Tuple, List, Dict, Union, Callable
from collections import OrderedDict
import msgpack
from enum import Enum, IntEnum

web_directory = str(Path(__file__).parent / 'www')

__xid = 0


def _xid() -> str:
    global __xid
    __xid += 1
    return f'p{__xid}'


class _MsgType(IntEnum):
    Error = 1
    Join = 2
    Switch = 3
    Input = 4
    Set = 5
    Insert = 6
    Update = 7
    Remove = 8


_primitive = (bool, int, float, str)
Primitive = Union[bool, int, float, str]


class RemoteError(Exception):
    pass


class ContextSwitchError(Exception):
    def __init__(self, target: str):
        super().__init__('Context switched')
        self.target = target


class InterruptError(Exception):
    def __init__(self):
        super().__init__('Interrupted')


class ProtocolError(Exception):
    pass


def _marshal(d: dict):
    return msgpack.packb(d)


def _unmarshal(b) -> dict:
    return msgpack.unpackb(b)


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
        self.delegate = value if callable(value) else None
        self.value = value if self.delegate is None else _xid()
        self.text = text
        self.name = name
        self.icon = icon
        self.caption = caption
        self.selected = selected
        self.options = options

    def dump(self) -> dict:
        d = dict(
            value=self.value,
            text=self.text,
            name=self.name,
            icon=self.icon,
            caption=self.caption,
            selected=self.selected,
            options=_dump(self.options),
        )
        return _clean(d)


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

Item = Union[str, 'Box']
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

Length = Union[str, int]

Sizing = Union[
    Length,
    Tuple[Length],
    Tuple[Length, Length],
    Tuple[Length, Length, Length],
]


class Theme:
    def __init__(
            self,
            background_color: str,
            foreground_color: str,
            accent_color: str,
            accent_color_name: str,
    ):
        self.background_color = background_color
        self.foreground_color = foreground_color
        self.accent_color = accent_color
        self.accent_color_name = accent_color_name

    def dump(self) -> dict:
        return dict(
            background_color=self.background_color,
            foreground_color=self.foreground_color,
            accent_color=self.accent_color,
            accent_color_name=self.accent_color_name,
        )


class Box:
    def __init__(
            self,
            text: Optional[Union[str, Options]] = None,
            name: Optional[str] = None,
            mode: Optional[str] = None,
            value: Optional[Value] = None,
            options: Optional[Options] = None,
            items: Optional[Items] = None,
            row: Optional[bool] = None,
            tile: Optional[str] = None,
            cross_tile: Optional[str] = None,
            wrap: Optional[str] = None,
            gap: Optional[Length] = None,
            grow: Optional[int] = None,
            shrink: Optional[int] = None,
            basis: Optional[Length] = None,
            align: Optional[str] = None,
            width: Optional[Sizing] = None,
            height: Optional[Sizing] = None,
            margin: Optional[Sizing] = None,
            padding: Optional[Sizing] = None,
            color: Optional[str] = None,
            background: Optional[str] = None,
            border: Optional[str] = None,
            image: Optional[str] = None,
            fit: Optional[str] = None,
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
            error: Optional[str] = None,
            lines: Optional[int] = None,
            multiple: Optional[bool] = None,
            required: Optional[bool] = None,
            password: Optional[bool] = None,
            editable: Optional[bool] = None,
    ):
        if isinstance(text, (tuple, set, list, dict, OrderedDict)):
            if options is not None:
                raise ValueError('options= must not be set if first argument is a collection.')
            label = None
            opts = text
            mode = 'button'
        else:
            label = text
            opts = options

        self.text = label
        self.name = name
        self.mode = mode
        self.value = value
        self.options = opts
        self.items = items
        self.row = row
        self.tile = tile
        self.cross_tile = cross_tile
        self.wrap = wrap
        self.gap = gap
        self.grow = grow
        self.shrink = shrink
        self.basis = basis
        self.align = align
        self.width = width
        self.height = height
        self.margin = margin
        self.padding = padding
        self.color = color
        self.background = background
        self.border = border
        self.image = image
        self.fit = fit
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
        self.error = error
        self.lines = lines
        self.multiple = multiple
        self.required = required
        self.password = password
        self.editable = editable

    def dump(self) -> dict:
        return _clean(dict(
            text=self.text,
            name=self.name,
            mode=self.mode,
            value=self.value,
            options=_dump(self.options),
            items=_dump(self.items),
            row=self.row,
            tile=self.tile,
            cross_tile=self.cross_tile,
            wrap=self.wrap,
            gap=self.gap,
            grow=self.grow,
            shrink=self.shrink,
            basis=self.basis,
            align=self.align,
            width=self.width,
            height=self.height,
            margin=self.margin,
            padding=self.padding,
            color=self.color,
            background=self.background,
            border=self.border,
            image=self.image,
            fit=self.fit,
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
            error=self.error,
            lines=self.lines,
            multiple=self.multiple,
            required=self.required,
            password=self.password,
            editable=self.editable,
        ))


box = Box


class BoxArrange(Enum):
    Normal = 'normal'
    Stretch = 'stretch'
    Center = 'center'
    Start = 'start'
    End = 'end'
    Between = 'between'
    Around = 'around'
    Evenly = 'evenly'


class BoxAlign(Enum):
    Left = 'left'
    Right = 'right'
    Center = 'center'
    Justify = 'justify'


def row(
        *items: Item,
        name: Optional[str] = None,
        tile: Optional[str] = None,
        cross_tile: Optional[str] = None,
        wrap: Optional[str] = None,
        gap: Optional[Length] = None,
        grow: Optional[int] = None,
        shrink: Optional[int] = None,
        basis: Optional[Length] = None,
        align: Optional[str] = None,
        width: Optional[Sizing] = None,
        height: Optional[Sizing] = None,
        margin: Optional[Sizing] = None,
        padding: Optional[Sizing] = None,
        color: Optional[str] = None,
        background: Optional[str] = None,
        border: Optional[str] = None,
        image: Optional[str] = None,
        fit: Optional[str] = None,
) -> Box:
    return Box(
        items=items,
        name=name,
        row=True,
        tile=tile,
        cross_tile=cross_tile,
        wrap=wrap,
        gap=gap,
        grow=grow,
        shrink=shrink,
        basis=basis,
        align=align,
        width=width,
        height=height,
        margin=margin,
        padding=padding,
        color=color,
        background=background,
        border=border,
        image=image,
        fit=fit,
    )


def col(
        *items: Item,
        name: Optional[str] = None,
        tile: Optional[str] = None,
        cross_tile: Optional[str] = None,
        wrap: Optional[str] = None,
        gap: Optional[Length] = None,
        grow: Optional[int] = None,
        shrink: Optional[int] = None,
        basis: Optional[Length] = None,
        align: Optional[str] = None,
        width: Optional[Sizing] = None,
        height: Optional[Sizing] = None,
        margin: Optional[Sizing] = None,
        padding: Optional[Sizing] = None,
        color: Optional[str] = None,
        background: Optional[str] = None,
        border: Optional[str] = None,
        image: Optional[str] = None,
        fit: Optional[str] = None,
) -> Box:
    return Box(
        items=items,
        name=name,
        tile=tile,
        cross_tile=cross_tile,
        wrap=wrap,
        gap=gap,
        grow=grow,
        shrink=shrink,
        basis=basis,
        align=align,
        width=width,
        height=height,
        margin=margin,
        padding=padding,
        color=color,
        background=background,
        border=border,
        image=image,
        fit=fit,
    )


def _collect_delegates(d: Dict[str, Callable], options: Sequence[Option]):
    for opt in options:
        if opt.delegate:
            d[opt.value] = opt.delegate
        if opt.options:
            _collect_delegates(d, opt.options)


def _interpret(msg, expected: int):
    if isinstance(msg, dict):
        t = msg.get('t')
        if t == _MsgType.Error:
            code = msg.get('c')
            raise RemoteError(f'code {code}')
        if t == _MsgType.Switch:
            raise ContextSwitchError(msg.get('d'))
        if (expected > -1) and t != expected:
            raise ProtocolError(f'unexpected message: want {expected}, got {t}')
        if t == _MsgType.Input:
            d = msg.get('d')
            n = len(d)
            if n == 0:
                return
            elif n == 1:
                return d[0]
            else:
                return tuple(d)
        if t == _MsgType.Join:
            d = msg.get('d')
            return d
        raise ProtocolError(f'unknown message type {t}')
    raise ProtocolError(f'unknown message format: want dict, got {type(msg)}')


def _marshal_set(
        title: str = None,
        caption: str = None,
        menu: Optional[Sequence[Option]] = None,
        nav: Optional[Sequence[Option]] = None,
        theme: Optional[Theme] = None,
) -> dict:
    return _marshal(dict(t=_MsgType.Set, d=_clean(dict(
        title=title,
        caption=caption,
        menu=_dump(menu),
        nav=_dump(nav),
        theme=_dump(theme),
    ))))


class _View:
    def __init__(
            self,
            delegate: Callable,
            context: any = None,
            send: Optional[Callable] = None,
            recv: Optional[Callable] = None,
            title: str = 'H2O Nitro',
            caption: str = 'v0.1.0',  # XXX show actual version
            menu: Optional[Sequence[Option]] = None,
            nav: Optional[Sequence[Option]] = None,
            theme: Optional[Theme] = None,
    ):
        self._delegate = delegate
        self.context = context or {}
        self._send = send
        self._recv = recv
        self._title = title
        self._caption = caption
        self._menu = menu or []
        self._nav = nav or []
        self._theme = theme

        self._delegates: Dict[str, Callable] = dict()
        _collect_delegates(self._delegates, self._menu)
        _collect_delegates(self._delegates, self._nav)

    def _join(self, msg):
        # XXX handle join msg
        return _marshal_set(
            title=self._title,
            caption=self._caption,
            menu=_dump(self._menu),
            nav=_dump(self._nav),
            theme=_dump(self._theme),
        )

    def __getitem__(self, key):
        return self.context.get(key)

    def __setitem__(self, key, value):
        self.context[key] = value

    def _delegate_for(self, key: str):
        d = self._delegates.get(key)
        if d is None:
            raise ProtocolError('Attempt to call unknown delegate')
        return d


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
            theme: Optional[Theme] = None,
    ):
        super().__init__(delegate, context, send, recv, title, caption, menu, nav, theme)

    def serve(self, send: Callable, recv: Callable, context: any = None):
        View(
            self._delegate,
            context,
            send,
            recv,
            self._title,
            self._caption,
            self._menu,
            self._nav,
            self._theme,
        )._run()

    def _run(self):
        self._send(self._join(self._read(_MsgType.Join)))

        target = None
        while True:
            try:
                (self._delegate_for(target) if target else self._delegate)(self)
            except ContextSwitchError as e:
                target = e.target
            except InterruptError:
                return

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

    def __call__(
            self,
            *items: Item,
            read=True,
            overwrite=True,
            position: Optional[int] = None,
            row: Optional[bool] = None,
            tile: Optional[str] = None,
            cross_tile: Optional[str] = None,
            wrap: Optional[str] = None,
            gap: Optional[Length] = None,
            grow: Optional[int] = None,
            shrink: Optional[int] = None,
            basis: Optional[Length] = None,
            align: Optional[str] = None,
            width: Optional[Sizing] = None,
            height: Optional[Sizing] = None,
            margin: Optional[Sizing] = None,
            padding: Optional[Sizing] = None,
            color: Optional[str] = None,
            background: Optional[str] = None,
            border: Optional[str] = None,
            image: Optional[str] = None,
            fit: Optional[str] = None,
    ):
        if len(items):
            b = Box(
                items=items,
                row=row,
                tile=tile,
                cross_tile=cross_tile,
                wrap=wrap,
                gap=gap,
                grow=grow,
                shrink=shrink,
                basis=basis,
                align=align,
                width=width,
                height=height,
                margin=margin,
                padding=padding,
                color=color,
                background=background,
                border=border,
                image=image,
                fit=fit,
            )
            self._send(_marshal(_clean(dict(
                t=_MsgType.Update if overwrite else _MsgType.Insert,
                d=b.dump(),
                p=position,
            ))))
        if read:
            res = self._read(_MsgType.Input)
            return res


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
            theme: Optional[Theme] = None,
    ):
        super().__init__(delegate, context, send, recv, title, caption, menu, nav, theme)

    async def serve(self, send: Callable, recv: Callable, context: any = None):
        await AsyncView(
            self._delegate,
            context,
            send,
            recv,
            self._title,
            self._caption,
            self._menu,
            self._nav,
            self._theme,
        )._run()

    async def _run(self):
        await self._send(self._join(await self._read(_MsgType.Join)))

        target = None
        while True:
            try:
                await (self._delegate_for(target) if target else self._delegate)(self)
            except ContextSwitchError as e:
                target = e.target
            except InterruptError:
                return

    async def _read(self, expected: int):
        m = await self._recv()
        if m:
            return _interpret(_unmarshal(m), expected)
        raise InterruptError()

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

    async def __call__(
            self,
            *items: Item,
            read=True,
            overwrite=True,
            position: Optional[int] = None,
            row: Optional[bool] = None,
            tile: Optional[str] = None,
            cross_tile: Optional[str] = None,
            wrap: Optional[str] = None,
            gap: Optional[Length] = None,
            grow: Optional[int] = None,
            shrink: Optional[int] = None,
            basis: Optional[Length] = None,
            align: Optional[str] = None,
            width: Optional[Sizing] = None,
            height: Optional[Sizing] = None,
            margin: Optional[Sizing] = None,
            padding: Optional[Sizing] = None,
            color: Optional[str] = None,
            background: Optional[str] = None,
            border: Optional[str] = None,
            image: Optional[str] = None,
            fit: Optional[str] = None,
    ):
        if len(items):
            b = Box(
                items=items,
                row=row,
                tile=tile,
                cross_tile=cross_tile,
                wrap=wrap,
                gap=gap,
                grow=grow,
                shrink=shrink,
                basis=basis,
                align=align,
                width=width,
                height=height,
                margin=margin,
                padding=padding,
                color=color,
                background=background,
                border=border,
                image=image,
                fit=fit,
            )
            await self._send(_marshal(_clean(dict(
                t=_MsgType.Update if overwrite else _MsgType.Insert,
                d=b.dump(),
                p=position,
            ))))
        if read:
            return await self._read(_MsgType.Input)


_lorem = '''
lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna 
aliqua ut enim ad minim veniam quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat 
duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur 
excepteur sint occaecat cupidatat non proident sunt in culpa qui officia deserunt mollit anim id est laborum
'''

_lorems = set([w.strip() for w in _lorem.split(' ')])


def _sentence(min, max):
    return ' '.join(random.sample(_lorems, random.randint(min, max))).capitalize()


def lorem(sentences: int = 0):
    if sentences == 0:
        return _sentence(4, 5)
    lines = [_sentence(5, 9) for i in range(sentences)]
    return '. '.join(lines) + '.'
