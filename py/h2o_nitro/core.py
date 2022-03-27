from typing import Optional, Tuple, Sequence, List, Dict, Union, Callable, Set
from collections import OrderedDict
import msgpack
from enum import Enum, IntEnum

__xid = 0


def _xid() -> str:
    global __xid
    __xid += 1
    return f'p{__xid}'


class _MsgType(IntEnum):
    Error = 1
    Join = 2
    Leave = 3
    Abort = 4
    Resume = 5
    Request = 6
    Response = 7
    Watch = 8
    Event = 9
    Input = 10
    Insert = 11
    Update = 12
    Remove = 13
    Conf = 14
    Switch = 15


class _WidgetT(IntEnum):
    Stack = 1
    Input = 2
    Option = 3


_primitive = (bool, int, float, str)
Primitive = Union[bool, int, float, str]


class RemoteError(Exception):
    pass


class ContextSwitchError(Exception):
    def __init__(self, target: str):
        super().__init__('User switched context')
        self.target = target


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

Delegate = Callable[['View'], None]


class Option:
    def __init__(
            self,
            value: Union[V, Delegate],
            text: Optional[str] = None,
            icon: Optional[str] = None,
            caption: Optional[str] = None,
            selected: Optional[bool] = None,
            options: Optional['Options'] = None,
    ):
        self.delegate = value if callable(value) else None
        self.value = value if self.delegate is None else _xid()
        self.text = text
        self.icon = icon
        self.caption = caption
        self.selected = selected
        self.options = options

    def dump(self) -> dict:
        d = dict(
            t=_WidgetT.Option,
            value=self.value,
            text=self.text,
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

Item = Union[str, 'Zone', 'Box']
Items = Union[List[Item], Tuple[Item, ...]]
Range = Union[
    Tuple[V, V],
    Tuple[N, N],
    Tuple[N, N, N],
    Tuple[N, N, N, int],
    List[V],
]
Value = Union[
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


class Box:
    def __init__(
            self,
            text: Optional[Union[str, Options]] = None,
            name: Optional[str] = None,
            mode: Optional[str] = None,
            icon: Optional[str] = None,
            value: Optional[Value] = None,
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
            options: Optional[Options] = None,
            row: Optional[bool] = None,
            tile: Optional[str] = None,
            cross_tile: Optional[str] = None,
            wrap: Optional[str] = None,
            gap: Optional[Length] = None,
            align: Optional[str] = None,
            width: Optional[Sizing] = None,
            height: Optional[Sizing] = None,
            grow: Optional[int] = None,
            shrink: Optional[int] = None,
            basis: Optional[str] = None,
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
        self.icon = icon
        self.value = value
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
        self.options = opts
        self.row = row
        self.tile = tile
        self.cross_tile = cross_tile
        self.wrap = wrap
        self.gap = gap
        self.align = align
        self.width = width
        self.height = height
        self.grow = grow
        self.shrink = shrink
        self.basis = basis

    def dump(self) -> dict:
        return _clean(dict(
            t=_WidgetT.Input,
            text=self.text,
            name=self.name,
            mode=self.mode,
            icon=self.icon,
            value=self.value,
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
            options=_dump(self.options),
            row=self.row,
            tile=self.tile,
            cross_tile=self.cross_tile,
            wrap=self.wrap,
            gap=self.gap,
            align=self.align,
            width=self.width,
            height=self.height,
            grow=self.grow,
            shrink=self.shrink,
            basis=self.basis,
        ))


box = Box


class ZoneTile(Enum):
    Normal = 'normal'
    Stretch = 'stretch'
    Center = 'center'
    Start = 'start'
    End = 'end'
    Between = 'between'
    Around = 'around'
    Evenly = 'evenly'


class ZoneCrossTile(Enum):
    Normal = 'normal'
    Stretch = 'stretch'
    Center = 'center'
    Start = 'start'
    End = 'end'


class ZoneWrap(Enum):
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


class Zone:
    def __init__(
            self,
            *items: Item,
            row: Optional[bool] = None,
            tile: Optional[str] = None,
            cross_tile: Optional[str] = None,
            wrap: Optional[str] = None,
            gap: Optional[Length] = None,
            align: Optional[str] = None,
            width: Optional[Sizing] = None,
            height: Optional[Sizing] = None,
            margin: Optional[str] = None,
            padding: Optional[str] = None,
            grow: Optional[int] = None,
            shrink: Optional[int] = None,
            basis: Optional[str] = None,
    ):
        self.items = items
        self.row = row
        self.tile = tile
        self.cross_tile = cross_tile
        self.wrap = wrap
        self.gap = gap
        self.align = align
        self.width = width
        self.height = height
        self.margin = margin
        self.padding = padding
        self.grow = grow
        self.shrink = shrink
        self.basis = basis

    def dump(self) -> dict:
        return _clean(dict(
            t=_WidgetT.Stack,
            items=_dump(self.items),
            row=self.row,
            tile=self.tile,
            cross_tile=self.cross_tile,
            wrap=self.wrap,
            gap=self.gap,
            align=self.align,
            width=self.width,
            height=self.height,
            margin=self.margin,
            padding=self.padding,
            grow=self.grow,
            shrink=self.shrink,
            basis=self.basis,
        ))


def row(
        *items: Item,
        tile: Optional[str] = None,
        cross_tile: Optional[str] = None,
        wrap: Optional[str] = None,
        gap: Optional[Length] = None,
        align: Optional[str] = None,
        width: Optional[Sizing] = None,
        height: Optional[Sizing] = None,
        margin: Optional[str] = None,
        padding: Optional[str] = None,
        grow: Optional[int] = None,
        shrink: Optional[int] = None,
        basis: Optional[str] = None,
) -> Zone:
    return Zone(
        *items,
        row=True,
        tile=tile,
        cross_tile=cross_tile,
        wrap=wrap,
        gap=gap,
        align=align,
        width=width,
        height=height,
        margin=margin,
        padding=padding,
        grow=grow,
        shrink=shrink,
        basis=basis,
    )


def col(
        *items: Item,
        tile: Optional[str] = None,
        cross_tile: Optional[str] = None,
        wrap: Optional[str] = None,
        gap: Optional[Length] = None,
        align: Optional[str] = None,
        width: Optional[Sizing] = None,
        height: Optional[Sizing] = None,
        margin: Optional[str] = None,
        padding: Optional[str] = None,
        grow: Optional[int] = None,
        shrink: Optional[int] = None,
        basis: Optional[str] = None,
) -> Zone:
    return Zone(
        *items,
        tile=tile,
        cross_tile=cross_tile,
        wrap=wrap,
        gap=gap,
        align=align,
        width=width,
        height=height,
        margin=margin,
        padding=padding,
        grow=grow,
        shrink=shrink,
        basis=basis,
    )


def _collect_delegates(d: Dict[str, Delegate], options: Sequence[Option]):
    for opt in options:
        if opt.delegate:
            d[opt.value] = opt.delegate
        if opt.options:
            _collect_delegates(d, opt.options)


class View:
    def __init__(
            self,
            delegate: Delegate,
            title: str = 'H2O Nitro',
            caption: str = 'v0.1.0',  # XXX show actual version
            menu: Optional[Sequence[Option]] = None,
            nav: Optional[Sequence[Option]] = None,
            send: Optional[Callable] = None,
            recv: Optional[Callable] = None,
            context: any = None,
    ):
        self._delegate = delegate
        self._title = title
        self._caption = caption
        self._menu = menu or []
        self._nav = nav or []
        self._delegates: Dict[str, Delegate] = dict()
        _collect_delegates(self._delegates, self._menu)
        _collect_delegates(self._delegates, self._nav)
        self._send = send
        self._recv = recv
        self.context = context

    def __getitem__(self, key):
        return self.context.get(key)

    def __setitem__(self, key, value):
        self.context[key] = value

    def _delegate_for(self, key: str):
        d = self._delegates.get(key)
        if d is None:
            raise ProtocolError('Attempt to call unknown delegate')
        return d

    def delegate(self, key: Optional[str] = None):
        if key is None:
            self._delegate(self)
            return

        self._delegate_for(key)(self)

    def serve(self, send: Callable, recv: Callable, context: any = None):
        View(
            self._delegate,
            title=self._title,
            caption=self._caption,
            menu=self._menu,
            nav=self._nav,
            send=send,
            recv=recv,
            context=context or {},
        )._run()

    def _run(self):
        self._read(_MsgType.Join)  # XXX handle join
        self._send(_marshal(dict(
            t=_MsgType.Conf,
            d=dict(
                title=self._title,
                caption=self._caption,
                menu=_dump(self._menu),
                nav=_dump(self._nav),
            ),
        )))
        target = None
        while True:
            try:
                self.delegate(target)
            except ContextSwitchError as e:
                target = e.target

    def _read(self, expected: int):
        msg = _unmarshal(self._recv())
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

    def _write(self, t: _MsgType, s: Zone, position: Optional[int]):
        msg = dict(t=t, d=s.dump())
        if position is not None:
            msg['p'] = position
        self._send(_marshal(msg))

    def read(self):
        return self._read(_MsgType.Input)

    def show(
            self,
            *items: Item,
            row: Optional[bool] = None,
            tile: Optional[str] = None,
            cross_tile: Optional[str] = None,
            wrap: Optional[str] = None,
            gap: Optional[Length] = None,
            align: Optional[str] = None,
            width: Optional[Sizing] = None,
            height: Optional[Sizing] = None,
            margin: Optional[str] = None,
            padding: Optional[str] = None,
            grow: Optional[int] = None,
            shrink: Optional[int] = None,
            basis: Optional[str] = None,
            position: Optional[int] = None,
    ):
        s = Zone(
            *items,
            row=row,
            tile=tile,
            cross_tile=cross_tile,
            wrap=wrap,
            gap=gap,
            align=align,
            width=width,
            height=height,
            margin=margin,
            padding=padding,
            grow=grow,
            shrink=shrink,
            basis=basis,
        )
        self._write(_MsgType.Update, s, position)

    def add(
            self,
            *items: Item,
            row: Optional[bool] = None,
            tile: Optional[str] = None,
            cross_tile: Optional[str] = None,
            wrap: Optional[str] = None,
            gap: Optional[Length] = None,
            align: Optional[str] = None,
            width: Optional[Sizing] = None,
            height: Optional[Sizing] = None,
            margin: Optional[str] = None,
            padding: Optional[str] = None,
            grow: Optional[int] = None,
            shrink: Optional[int] = None,
            basis: Optional[str] = None,
            position: Optional[int] = None,
    ):
        s = Zone(
            *items,
            row=row,
            tile=tile,
            cross_tile=cross_tile,
            wrap=wrap,
            gap=gap,
            align=align,
            width=width,
            height=height,
            margin=margin,
            padding=padding,
            grow=grow,
            shrink=shrink,
            basis=basis,
        )
        self._write(_MsgType.Insert, s, position)

    def remove(self, position: int):
        pass

    def __call__(
            self,
            *items: Item,
            row: Optional[bool] = None,
            tile: Optional[str] = None,
            cross_tile: Optional[str] = None,
            wrap: Optional[str] = None,
            gap: Optional[Length] = None,
            align: Optional[str] = None,
            width: Optional[Sizing] = None,
            height: Optional[Sizing] = None,
            margin: Optional[str] = None,
            padding: Optional[str] = None,
            grow: Optional[int] = None,
            shrink: Optional[int] = None,
            basis: Optional[str] = None,
            position: Optional[int] = None,
    ):
        self.show(
            *items,
            row=row,
            tile=tile,
            cross_tile=cross_tile,
            wrap=wrap,
            gap=gap,
            align=align,
            width=width,
            height=height,
            margin=margin,
            padding=padding,
            grow=grow,
            shrink=shrink,
            basis=basis,
            position=position,
        )
        return self.read()
