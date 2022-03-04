from typing import Optional, Tuple, List, Dict, Union
import websocket
from base64 import b64encode
import msgpack
from enum import IntEnum
from io import BytesIO


class _MsgOp(IntEnum):
    Control = 1
    Message = 2


class _MsgType(IntEnum):
    Error = 1
    Join = 2
    Leave = 3
    Request = 4
    Response = 5
    Watch = 6
    Event = 7
    Text = 8
    Input = 9
    Abort = 10
    Resume = 11
    Read = 12
    Write = 13
    Append = 14


class _ErrorCode(IntEnum):
    PeerUnavailable = 1
    PeerDead = 2
    RateLimited = 3


class _WidgetT(IntEnum):
    Output = 1
    Input = 2
    Option = 3


# TODO read from env
client_id = 'foo'
client_secret = 'foo'

# TODO SSL options
# To modify the Host, Origin, Cookie, or Sec-WebSocket-Protocol header values of the WebSocket handshake request,
# pass the host, origin, cookie, or subprotocols options to your WebSocket connection.
# https://websocket-client.readthedocs.io/en/latest/faq.html#what-else-can-i-do-with-sslopts
ws = websocket.WebSocket()
ws.connect('ws://localhost:11111/ws/b?r=/foo/', header={
    'Authorization': 'Basic ' + b64encode(f'{client_id}:{client_secret}'.encode('ascii')).decode('ascii')
})

_primitive = (bool, int, float, str)
Primitive = Union[bool, int, float, str]


# Objects = Union[Tuple[dict, ...], List[dict]]


class RemoteError(Exception):
    pass


class ProtocolError(Exception):
    pass


def _marshal(op: int, data: dict):
    # Prefix 1-byte op to message
    with BytesIO() as buf:
        buf.write(op.to_bytes(1, 'little'))
        buf.write(msgpack.packb(data))
        buf.seek(0)
        b = buf.read()
        return b


def _unmarshal(b) -> dict:
    return msgpack.unpackb(b)


def _write(op: int, d: dict):
    ws.send_binary(_marshal(op, d))


def _write_message(d: dict):
    _write(_MsgOp.Message, d)


def _read(expected=-1) -> any:
    msg = _unmarshal(ws.recv())
    if isinstance(msg, dict):
        t = msg.get('t')
        if t == _MsgType.Error:
            code = msg.get('c')
            raise RemoteError(f'code {code}')
        if (expected > -1) and t != expected:
            raise ProtocolError(f'unexpected message: want {expected}, got {t}')
        if t == _MsgType.Input:
            d = msg.get('d')
            n = len(d)
            if n == 0:
                raise ProtocolError('unexpected input: got empty list')
            elif n == 1:
                return d[0]
            else:
                return tuple(d)
        if t == _MsgType.Join:
            d = msg.get('d')
            return d
        raise ProtocolError(f'unknown message type {t}')
    raise ProtocolError(f'unknown message format: want dict, got {type(msg)}')


def _clean(d: dict) -> dict:
    return {k: v for k, v in d.items() if v is not None}


N = Union[int, float]
V = Union[N, str]


class Option:
    def __init__(
            self,
            value: V,
            label: Optional[str] = None,
            icon: Optional[str] = None,
            caption: Optional[str] = None,
            selected: Optional[bool] = None,
            options: Optional['Options'] = None,
    ):
        self.value = value
        self.label = label
        self.icon = icon
        self.caption = caption
        self.selected = selected
        self.options = options

    def dump(self) -> dict:
        d = dict(
            t=_WidgetT.Option,
            value=self.value,
            label=self.label,
            icon=self.icon,
            caption=self.caption,
            selected=self.selected,
            options=self.options,
        )
        return _clean(d)


Options = Union[
    Tuple[Primitive, ...],
    List[Primitive],
    Dict[Primitive, any],
    List[Option],
    Tuple[Option, ...],
]

Item = Union['Input', 'Output', str]
Items = Union[List[Item], Tuple[Item, ...]]


def _are_instances(xs, t) -> bool:
    if not isinstance(xs, (tuple, list)):
        return False
    for x in xs:
        if not isinstance(x, t):
            return False
    return True


def _dump(x):
    if isinstance(x, (tuple, list)):
        return [_dump(e) for e in x]
    if callable(getattr(x, 'dump', None)):
        return x.dump()
    return x


class Input:
    def __init__(
            self,
            label: Optional[str] = None,
            mode: Optional[str] = None,
            icon: Optional[str] = None,
            value: Optional[Union[V, Tuple[V, V]]] = None,
            min: Optional[V] = None,
            max: Optional[V] = None,
            step: Optional[N] = None,
            precision: Optional[int] = None,
            range: Optional[Union[Tuple[V, V], Tuple[N, N, N], Tuple[N, N, N, int]]] = None,
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
            actions: Optional[Options] = None,
            items: Optional[Items] = None,
            inline: Optional[bool] = None,
            size: Optional[V] = None,
    ):
        self.label = label
        self.mode = mode
        self.icon = icon
        self.value = value
        self.min = min
        self.max = max
        self.step = step,
        self.precision = precision,
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
        self.options = options
        self.actions = actions
        self.items = items
        self.inline = inline
        self.size = size

    def dump(self) -> dict:
        d = dict(
            t=_WidgetT.Input,
            label=self.label,
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
            actions=_dump(self.actions),
            items=_dump(self.items),
            inline=self.inline,
            size=self.size,
        )
        return _clean(d)


class Output:
    def __init__(
            self,
            text: Optional[str] = None,
            items: Optional[Items] = None,
            inline: Optional[bool] = None,
            size: Optional[V] = None,
    ):
        self.text = text
        self.items = items
        self.inline = inline
        self.size = size

    def dump(self) -> dict:
        d = dict(
            t=_WidgetT.Output,
            text=self.text,
            items=_dump(self.items),
            inline=self.inline,
            size=self.size,
        )
        return _clean(d)


option = Option


def input(
        content: Optional[Union[str, Items]] = None,
        mode: Optional[str] = None,
        icon: Optional[str] = None,
        value: Optional[Union[V, Tuple[V, V]]] = None,
        min: Optional[V] = None,
        max: Optional[V] = None,
        step: Optional[N] = None,
        precision: Optional[int] = None,
        range: Optional[Union[Tuple[V, V], Tuple[N, N, N], Tuple[N, N, N, int]]] = None,
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
        actions: Optional[Options] = None,
        inline: Optional[bool] = None,
        size: Optional[V] = None,
) -> Input:
    label, items = (None, content) if isinstance(content, (tuple, list)) else (content, None)
    return Input(
        label,
        mode,
        icon,
        value,
        min,
        max,
        step,
        precision,
        range,
        mask,
        prefix,
        suffix,
        placeholder,
        error,
        lines,
        multiple,
        required,
        password,
        editable,
        options,
        actions,
        items,
        inline,
        size,
    )


def output(
        content: Union[str, Items],
        inline: Optional[bool] = None,
        size: Optional[V] = None,
) -> Output:
    text, items = (None, content) if isinstance(content, (tuple, list)) else (content, None)
    return Output(
        text,
        items,
        inline,
        size,
    )


def read(
        content: Optional[Union[str, Items]] = None,
        mode: Optional[str] = None,
        icon: Optional[str] = None,
        value: Optional[Union[V, Tuple[V, V]]] = None,
        min: Optional[V] = None,
        max: Optional[V] = None,
        step: Optional[N] = None,
        precision: Optional[int] = None,
        range: Optional[Union[Tuple[V, V], Tuple[N, N, N], Tuple[N, N, N, int]]] = None,
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
        actions: Optional[Options] = None,
        inline: Optional[bool] = None,
        size: Optional[V] = None,
):
    i = input(
        content,
        mode,
        icon,
        value,
        min,
        max,
        step,
        precision,
        range,
        mask,
        prefix,
        suffix,
        placeholder,
        error,
        lines,
        multiple,
        required,
        password,
        editable,
        options,
        actions,
        inline,
        size,
    )
    _write_message(dict(t=_MsgType.Read, d=i.dump()))
    return _read(_MsgType.Input)


def append(
        content: Union[str, Items],
        inline: Optional[bool] = None,
        size: Optional[V] = None,
        # TODO update: dict - selectively update parts
):
    o = output(
        content,
        inline,
        size,
    )
    _write_message(dict(t=_MsgType.Append, d=o.dump()))


def write(
        content: Union[str, Items],
        inline: Optional[bool] = None,
        size: Optional[V] = None,
        # TODO update: dict - selectively update parts
):
    o = output(
        content,
        inline,
        size,
    )
    _write_message(dict(t=_MsgType.Write, d=o.dump()))


def close():
    ws.close()


# Wait for join
_d_join = _read(_MsgType.Join)  # XXX convert to context

# ------ end of bootstrap; begin userland ------

counter = 0

while True:
    read()
    choice = read([
        f'Count={counter}',
        input(actions=('incr', 'decr')),
    ])
    print(choice)
    counter += 1 if choice == 'incr' else -1
