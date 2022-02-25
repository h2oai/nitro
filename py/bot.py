from typing import Optional, Tuple, List, Dict, Union
import json
import websocket
from base64 import b64encode

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


def _write(d: dict):
    # compact representation, without newlines
    ws.send(json.dumps(d, allow_nan=False, separators=(',', ':')))


def _read() -> any:
    data = ws.recv()
    print('data', data)
    d = json.loads(data)
    print('loaded', d)
    if isinstance(d, dict):
        t = d.get('t')
        if t == 'r':  # result
            e = d.get('e')
            if e is not None:
                raise RemoteError(e)
            return d.get('r')
        elif t == 'h':  # hello
            return d.get('h')  # context
        raise ProtocolError(f'unknown message opcode: got "{t}"')
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


def question(
        text: Optional[Union[str, Options]] = None,
        options: Optional[Options] = None,
        actions: Optional[Options] = None,
):
    is_shorthand = options is None and isinstance(text, (tuple, list, dict))
    d = dict(
        t='r',
        text=None if is_shorthand else text,
        options=text if is_shorthand else options,
        actions=actions,
    )
    return _clean(d)


def ask(
        text: Optional[Union[str, Options]] = None,
        options: Optional[Options] = None,
        actions: Optional[Options] = None,
) -> dict:
    q = question(
        text,
        options,
        actions,
    )
    _write(q)
    return _read()


def result(
        text: Union[str, Objects],
        results: Optional[Objects] = None,
        append: Optional[bool] = None,
) -> dict:
    has_children = results is not None and isinstance(text, (list, dict))
    d = dict(
        t='a' if append else 'w',
        text=None if has_children else text,
        results=text if has_children else results,
    )
    return _clean(d)


def show(
        text: Union[str, Objects],
        results: Optional[Objects] = None,
        append: Optional[bool] = None,
        # TODO update: dict - selectively update parts
):
    r = result(
        text,
        results,
        append,
    )
    _write(r)


def close():
    ws.close()


# Wait for handshake/hello
context = _read()

# ------ end of bootstrap; begin userland ------

counter = 0

while True:
    choice = ask(('incr', 'decr'))
    counter += 1 if input == 'incr' else -1
    show(str(counter), append=True)
