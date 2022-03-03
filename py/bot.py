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


class _WidgetType(IntEnum):
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


class Option:
    def __init__(
            self,
            text: Optional[Primitive] = None,
            value: any = None,
    ):
        self.text = text
        self.value = value

    def dump(self) -> dict:
        d = dict(
            t=_WidgetType.Option,
            text=self.text,
            value=self.value
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
            options: Optional[Options] = None,
            actions: Optional[Options] = None,
            items: Optional[Items] = None,
    ):
        self.label = label
        self.options = options
        self.actions = actions
        self.items = items

    def dump(self) -> dict:
        d = dict(
            t=_WidgetType.Input,
            label=self.label,
            options=_dump(self.options),
            actions=_dump(self.actions),
            items=_dump(self.items),
        )
        return _clean(d)


class Output:
    def __init__(
            self,
            text: Optional[str] = None,
            items: Optional[Items] = None,
    ):
        self.text = text
        self.items = items

    def dump(self) -> dict:
        d = dict(
            t=_WidgetType.Output,
            text=self.text,
            items=_dump(self.items),
        )
        return _clean(d)


def option(
        text: Optional[Primitive] = None,
        value: any = None,
) -> Option:
    return Option(
        text,
        value
    )


def input(
        content: Optional[Union[str, Items]] = None,
        options: Optional[Options] = None,
        actions: Optional[Options] = None,
) -> Input:
    label, items = (None, content) if isinstance(content, (tuple, list)) else (content, None)
    return Input(
        label,
        options,
        actions,
        items,
    )


def output(
        content: Union[str, Items],
) -> Output:
    text, items = (None, content) if isinstance(content, (tuple, list)) else (content, None)
    return Output(
        text,
        items,
    )


def read(
        content: Optional[Union[str, Items]] = None,
        options: Optional[Options] = None,
        actions: Optional[Options] = None,
):
    i = input(
        content,
        options,
        actions,
    )
    _write_message(dict(t=_MsgType.Read, d=i.dump()))
    return _read(_MsgType.Input)


def append(
        content: Union[str, Items],
        # TODO update: dict - selectively update parts
):
    o = output(
        content,
    )
    _write_message(dict(t=_MsgType.Append, d=o.dump()))


def write(
        content: Union[str, Items],
        # TODO update: dict - selectively update parts
):
    o = output(
        content,
    )
    _write_message(dict(t=_MsgType.Write, d=o.dump()))


def close():
    ws.close()


# Wait for join
_d_join = _read(_MsgType.Join)  # XXX convert to context

# ------ end of bootstrap; begin userland ------

counter = 0

while True:
    choice = read([
        f'Count={counter}',
        input(options=('incr', 'decr')),
    ])
    print(choice)
    counter += 1 if choice == 'incr' else -1
