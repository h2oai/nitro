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


# TODO read from env
client_id = 'foo'
client_secret = 'foo'

# TODO SSL options
# To modify the Host, Origin, Cookie, or Sec-WebSocket-Protocol header values of the WebSocket handshake request,
# pass the host, origin, cookie, or subprotocols options to your WebSocket connection.
# https://websocket-client.readthedocs.io/en/latest/faq.html#what-else-can-i-do-with-sslopts
ws = websocket.WebSocket()
ws.connect('ws://localhost:11111/ws/bot?r=/foo/', header={
    'Authorization': 'Basic ' + b64encode(f'{client_id}:{client_secret}'.encode('ascii')).decode('ascii')
})

_primitive = (bool, int, float, str)
Primitive = Union[bool, int, float, str]
Objects = Union[Tuple[dict, ...], List[dict]]
Options = Union[
    Tuple[Primitive, ...],
    List[Primitive],
    Dict[Primitive, any],
    Objects,
]


class RemoteError(Exception):
    pass


class ProtocolError(Exception):
    pass


def _marshal(op: int, data: dict):
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


def _read(t: int = 0) -> dict:
    data = ws.recv()
    d = _unmarshal(data)
    if isinstance(d, dict):
        if t == 0:
            dt = d.get('t')
            if t != dt:
                raise ProtocolError(f'unexpected message: want {t}, got {dt}')
        return d
    raise ProtocolError(f'unknown message format: want dict, got {type(d)}')


def _clean(d: dict) -> dict:
    return {k: v for k, v in d.items() if v is not None}


def option(
        text: Optional[Primitive] = None,
        value: any = None,
) -> dict:
    d = dict(
        text=text,
        value=value,
    )
    return _clean(d)


def input(
        text: Optional[Union[str, Options]] = None,
        options: Optional[Options] = None,
        actions: Optional[Options] = None,
) -> dict:
    is_shorthand = options is None and isinstance(text, (tuple, list, dict))
    d = dict(
        text=None if is_shorthand else text,
        options=text if is_shorthand else options,
        actions=actions,
    )
    return _clean(d)


def read(
        text: Optional[Union[str, Options]] = None,
        options: Optional[Options] = None,
        actions: Optional[Options] = None,
):
    d = input(
        text,
        options,
        actions,
    )
    d['t'] = _MsgType.Read
    _write_message(d)
    return _read(_MsgType.Input)


def output(
        text: Union[str, Objects],
        results: Optional[Objects] = None,
) -> dict:
    has_children = results is not None and isinstance(text, (list, dict))
    d = dict(
        text=None if has_children else text,
        results=text if has_children else results,
    )
    return _clean(d)


def append(
        text: Union[str, Objects],
        results: Optional[Objects] = None,
        # TODO update: dict - selectively update parts
):
    d = output(
        text,
        results,
    )
    d['t'] = _MsgType.Append
    _write_message(d)


def write(
        text: Union[str, Objects],
        results: Optional[Objects] = None,
        # TODO update: dict - selectively update parts
):
    d = output(
        text,
        results,
    )
    d['t'] = _MsgType.Write
    _write_message(d)


def close():
    ws.close()


# Wait for join
_d_join = _read(_MsgType.Join)  # XXX convert to context

# ------ end of bootstrap; begin userland ------

counter = 0

while True:
    choice = read(('incr', 'decr'))
    counter += 1 if input == 'incr' else -1
    append(str(counter))
