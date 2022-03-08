from typing import Optional, Tuple, List, Dict, Union, Callable, Set
import msgpack
from enum import IntEnum

from flask import Flask, request
import simple_websocket


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


class _WidgetT(IntEnum):
    Input = 1
    Option = 2


_primitive = (bool, int, float, str)
Primitive = Union[bool, int, float, str]


# Objects = Union[Tuple[dict, ...], List[dict]]


class RemoteError(Exception):
    pass


class ProtocolError(Exception):
    pass


def _marshal(d: dict):
    return msgpack.packb(d)


def _unmarshal(b) -> dict:
    return msgpack.unpackb(b)


def _dump(x):  # recursive
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
            value: V,
            text: Optional[str] = None,
            icon: Optional[str] = None,
            caption: Optional[str] = None,
            selected: Optional[bool] = None,
            options: Optional['Options'] = None,
    ):
        self.value = value
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

Item = Union['Input', str]
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


class Input:
    def __init__(
            self,
            text: Optional[str] = None,
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
            items: Optional[Items] = None,
            inline: Optional[bool] = None,
            size: Optional[V] = None,
            align: Optional[str] = None,
    ):
        self.text = text
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
        self.options = options
        self.items = items
        self.inline = inline
        self.size = size
        self.align = align

    def dump(self) -> dict:
        d = dict(
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
            items=_dump(self.items),
            inline=self.inline,
            size=self.size,
            align=self.align,
        )
        return _clean(d)


def input(
        content: Optional[Union[str, Items]] = None,
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
        inline: Optional[bool] = None,
        size: Optional[V] = None,
        align: Optional[str] = None,
) -> Input:
    text, items = (None, content) if isinstance(content, (tuple, list)) else (content, None)
    return Input(
        text,
        name,
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
        items,
        inline,
        size,
        align,
    )


class UI:
    def __init__(self, send: Callable, recv: Callable, handle: Callable):
        self._send = send
        self._recv = recv
        self._handle = handle

    def run(self):
        self._read(_MsgType.Join)  # XXX handle join
        while True:
            self._handle(self)

    def _read(self, expected: int):
        msg = _unmarshal(self._recv())
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

    def _write(self):
        pass

    def __call__(
            self,
            content: Optional[Union[str, Items]] = None,
            position: Optional[int] = None,
            insert: Optional[bool] = False,
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
            inline: Optional[bool] = None,
            size: Optional[V] = None,
            align: Optional[str] = None,
    ):
        d = input(
            content,
            name,
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
            inline,
            size,
            align,
        ).dump()
        msg = dict(t=_MsgType.Insert if insert else _MsgType.Update, d=d)
        if position is not None:
            msg['p'] = position
        self._send(_marshal(msg))
        return self._read(_MsgType.Input)


# --- userland ---


def main2(ui: UI):
    counter = 0
    while True:
        choice = ui([
            f'Count={counter}',
            input(options=('+', '-')),
        ])
        counter += 1 if choice == '+' else -1


def main(ui: UI):
    x = ui('Text field with label')
    x = ui('Text field with placeholder', placeholder='Enter text here')
    x = ui('Text field with value', value='Some text')
    x = ui('Text field, required', required=True)
    x = ui('Text field with input mask', mask='(999) 999 - 9999')
    x = ui('Text field with icon', icon='Calendar')
    x = ui('Text field with prefix', prefix='https://')
    x = ui('Text field with suffix', suffix='.com')
    x = ui('Text field with prefix and suffix', prefix='https://', suffix='.com')
    x = ui('Text field with error', error='Something went wrong')
    x = ui('Password field', password=True)
    x = ui('Multiline text field', lines=1)
    x = ui('Multiline text field, taller', lines=5)
    x = ui('Integer', value=5)
    x = ui('Integer within range', range=(0, 10))
    x = ui('Integer within range, with step', range=(0, 10, 2))
    x = ui('Integer within range, with default', value=5, range=(0, 10))
    x = ui('Integer within range, origin from zero', value=3, range=(-5, 5))
    x = ui('Decimal within range, with step', value=0.6, range=(-1, 1, 0.2))
    x = ui('Integer range', value=(3, 7), range=(1, 10))
    x = ui('Integer range, origin from zero', value=(-1, 3), range=(-5, 5))
    x = ui('Integer field', value=5, editable=True)
    x = ui('Integer field with range', value=5, range=(1, 10), editable=True)
    x = ui('Integer field with range and step', value=50, range=(0, 100, 10), editable=True)
    x = ui('Decimal field with range and step', value=0.5, range=(0.0, 1.0, 0.05), editable=True)
    x = ui('Decimal field with range, step, and precision', value=0.5, range=(0.0, 1.0, 0.05, 2), editable=True)
    x = ui('Rating', mode='rating')
    x = ui('Rating with value', mode='rating', value=3)
    x = ui('Rating with zero allowed', mode='rating', min=0)
    x = ui('Rating with max', mode='rating', value=3, max=10)
    x = ui('Rating with range', mode='rating', value=3, range=(0, 7))
    x = ui('Time', mode='time', value='3:04PM')
    x = ui('Time, with seconds', mode='time', value='3:04:05PM')
    x = ui('Time, hour only', mode='time', value='3PM')
    x = ui('Time, 24-hr clock', mode='time', value='15:04')
    x = ui('Time, 24-hr clock, with seconds', mode='time', value='15:04:05')
    x = ui('Time, hour only, 24-hour clock', mode='time', value='15')
    x = ui('Day picker', mode='day', value='2021-10-10')
    x = ui('Day picker with range', mode='day', value='2021-10-10', range=('2019-01-01', '2022-12-31'))
    x = ui('Week picker', mode='week', value='2021-10-10')
    x = ui('Week picker with range', mode='week', value='2021-10-10', range=('2019-01-01', '2022-12-31'))
    x = ui('Month picker', mode='month', value='2021-10-10')
    x = ui('Month picker with range', mode='month', value='2021-10-10', range=('2019-01-01', '2022-12-31'))
    x = ui('Options from string', options='Apples Bananas Cherries')
    x = ui('Options from tuple', options=('Apples', 'Bananas', 'Cherries'))
    x = ui('Options from list', options=['Apples', 'Bananas', 'Cherries'])
    x = ui('Options from set', options={'Apples', 'Bananas', 'Cherries'})
    x = ui('Options from tuples', options=(('a', 'Apples'), ('b', 'Bananas'), ('c', 'Cherries')))
    x = ui('Options from dict', options={'Apples': 'a', 'Bananas': 'b', 'Cherries': 'c'})
    x = ui('Options from dict', options=dict(Apples='a', Bananas='b', Cherries='c'))
    x = ui('Options', options=[
        option('a', 'Apples'),
        option('b', 'Bananas'),
        option('c', 'Cherries'),
    ])
    x = ui('Options with selection', options=[
        option('a', 'Apples', selected=True),
        option('b', 'Bananas'),
        option('c', 'Cherries'),
    ])
    x = ui('Multiple choice', multiple=True, options=[
        option('a', 'Apples'),
        option('b', 'Bananas'),
        option('c', 'Cherries'),
    ])
    x = ui('Multiple choice, with selection', multiple=True, options=[
        option('a', 'Apples', selected=True),
        option('b', 'Bananas'),
        option('c', 'Cherries'),
    ])
    x = ui('Multiple choice, with multiple selections', multiple=True, options=[
        option('a', 'Apples', selected=True),
        option('b', 'Bananas', selected=True),
        option('c', 'Cherries'),
    ])
    x = ui('Multiple choice, required', multiple=True, required=True, options=[
        option('a', 'Apples'),
        option('b', 'Bananas'),
        option('c', 'Cherries'),
    ])
    x = ui('Multiple choice, with error message', multiple=True, error='Something went wrong', options=[
        option('a', 'Apples'),
        option('b', 'Bananas'),
        option('c', 'Cherries'),
    ])
    x = ui('Multiple choice, editable', multiple=True, editable=True, options=[
        option('a', 'Apples'),
        option('b', 'Bananas'),
        option('c', 'Cherries'),
    ])
    x = ui('Tag Picker', mode='tag', options=[
        option('a', 'Apples'),
        option('b', 'Bananas'),
        option('c', 'Cherries'),
    ])
    x = ui('Choice list', placeholder='Pick a fruit', options=[
        option('a', 'Apples'),
        option('b', 'Bananas'),
        option('c', 'Cherries'),
    ])
    x = ui('Choice list, required', placeholder='Pick a fruit', required=True, options=[
        option('a', 'Apples'),
        option('b', 'Bananas'),
        option('c', 'Cherries'),
    ])
    x = ui('Choice list, with icons', placeholder='Pick a fruit', required=True, options=[
        option('area', 'Area', icon='AreaChart', selected=True),
        option('bar', 'Bar', icon='BarChartHorizontal'),
        option('column', 'Column', icon='BarChartVertical'),
        option('line', 'Line', icon='LineChart'),
        option('scatter', 'Scatter', icon='ScatterChart'),
        option('donut', 'Donut', icon='DonutChart'),
    ])
    x = ui('Choice list, with error message', placeholder='Pick a fruit', error='Something went wrong', options=[
        option('a', 'Apples'),
        option('b', 'Bananas'),
        option('c', 'Cherries'),
    ])
    x = ui('Choice list, editable', placeholder='Pick a fruit', editable=True, options=[
        option('a', 'Apples'),
        option('b', 'Bananas'),
        option('c', 'Cherries'),
    ])
    x = ui('Choice list, grouped', placeholder='Pick an item', options=[
        option('f', 'Fruits', options=[
            option('a', 'Apples'),
            option('b', 'Bananas'),
            option('c', 'Cherries'),
        ]),
        option('v', 'Vegetables', options=[
            option('l', 'Lettuce'),
            option('t', 'Tomato'),
        ]),
    ])
    x = ui('Color picker', mode='color', value='#a241e8')
    x = ui('Color picker, with choices', mode='color', options=[
        option('#ca5010', 'Orange'),
        option('#038387', 'Cyan'),
        option('#8764b8', 'Purple'),
        option('#881798', 'Magenta'),
    ])
    x = ui('Buttons, vertical', options=[
        option('a', 'Apples'),
        option('b', 'Bananas'),
        option('c', 'Cherries'),
    ], inline=False)
    x = ui('Compound buttons', options=[
        option('yes', 'Sign me up!', caption='Terms and conditions apply', selected=True),
        option('no', 'Not now', caption="I'll decide later"),
    ])
    x = ui('Button with menu', options=[
        option('yes', 'Yes', selected=True, options=[
            option('later', 'Remind me later', icon='ChatBot'),
            option('never', "Don't ask me again", icon='MuteChat'),
        ]),
        option('no', 'No'),
    ])
    x = ui('Button with menu', options=[
        option('yes', 'Yes', selected=True),
        option('no', 'No', options=[
            option('later', 'Remind me later', icon='ChatBot'),
            option('never', "Don't ask me again", icon='MuteChat'),
        ]),
    ])
    x = ui('Add a new chart', options=[
        option('area', 'Area', icon='AreaChart'),
        option('bar', 'Bar', icon='BarChartHorizontal'),
        option('column', 'Column', icon='BarChartVertical'),
        option('line', 'Line', icon='LineChart'),
        option('scatter', 'Scatter', icon='ScatterChart'),
        option('donut', 'Donut', icon='DonutChart'),
    ])
    x = ui([
        input('Username', placeholder='someone@company.com'),
        input('Password', password=True),
    ])
    x = ui([
        input('Username', placeholder='someone@company.com'),
        input('Password', password=True),
    ], inline=True)
    x = ui([
        input('Username', placeholder='someone@company.com'),
        input('Password', password=True),
        input(options=[option('login', 'Login', selected=True)])
    ], inline=True)
    x = ui([
        input([input('First name'), input('Last name')], inline=True),
        input('Address line 1'),
        input('Address line 2'),
        input([input('City'), input('State'), input('Zip')], inline=True),
    ])
    x = ui([
        input([input('First name'), input('M.I.', size='10%'), input('Last name')], inline=True),
        input('Address line 1'),
        input('Address line 2'),
        input([input('City', size=5), input('State', size='20%'), input('Zip', size=1)], inline=True),
        input(options=[
            option('yes', 'Sign me up!', caption='Terms and conditions apply', selected=True),
            option('no', 'Not now', caption="I'll decide later"),
        ])
    ])


# --- bootstrap ---

app = Flask(__name__, static_folder='../web/build', static_url_path='')


@app.route('/wsui', websocket=True)
def socket():
    ws = simple_websocket.Server(request.environ)
    ui = UI(ws.send, ws.receive, main)
    try:
        ui.run()
    except simple_websocket.ConnectionClosed:
        pass
    return ''


if __name__ == '__main__':
    app.run()
