from h2o_nitro import UI, input, option, stack, ContextSwitchError
import simple_websocket
from flask import Flask, request


def main2(ui: UI):
    counter = 0
    while True:
        choice = ui(
            f'Count={counter}',
            input(options=('+', '-')),
        )
        counter += 1 if choice == '+' else -1


sample_markdown = '''
# Brawny gods just flocked up to quiz and vex him

But how could we fail to see that there is an infinite regress here—if we do not accept, 
as Kantian and post-Kantian philosophies do, a "supersensible" domain of freedom, outside
of the world and its physical determinisms? According to them, the free subject is an absolute
origin, a first agent capable of creating first causes, who initiates new causal chains *ex nihilo*,
independent of the rest of the world. — Henri Atlan, *Is Science Inhuman*?

## Amazingly few discotheques provide jukeboxes

But how could we fail to see that there is an infinite regress here—if we do not accept, 
as Kantian and post-Kantian philosophies do, a "supersensible" domain of freedom, outside
of the world and its physical determinisms? According to them, the free subject is an absolute
origin, a first agent capable of creating first causes, who initiates new causal chains *ex nihilo*,
independent of the rest of the world. — Henri Atlan, *Is Science Inhuman*?


### Why shouldn’t a quixotic Kazakh vampire jog barefoot?

But how could we fail to see that there is an infinite regress here—if we do not accept, 
as Kantian and post-Kantian philosophies do, a "supersensible" domain of freedom, outside
of the world and its physical determinisms? According to them, the free subject is an absolute
origin, a first agent capable of creating first causes, who initiates new causal chains *ex nihilo*,
independent of the rest of the world. — Henri Atlan, *Is Science Inhuman*?

#### Grumpy wizards make a toxic brew for the jovial queen

But how could we fail to see that there is an infinite regress here—if we do not accept, 
as Kantian and post-Kantian philosophies do, a "supersensible" domain of freedom, outside
of the world and its physical determinisms? According to them, the free subject is an absolute
origin, a first agent capable of creating first causes, who initiates new causal chains *ex nihilo*,
independent of the rest of the world. — Henri Atlan, *Is Science Inhuman*?

##### Jackie will budget for the most expensive zoology equipment

But how could we fail to see that there is an infinite regress here—if we do not accept, 
as Kantian and post-Kantian philosophies do, a "supersensible" domain of freedom, outside
of the world and its physical determinisms? According to them, the free subject is an absolute
origin, a first agent capable of creating first causes, who initiates new causal chains *ex nihilo*,
independent of the rest of the world. — Henri Atlan, *Is Science Inhuman*?

But how could we fail to see that there is an infinite regress here—if we do not accept, 
as Kantian and post-Kantian philosophies do, a "supersensible" domain of freedom, outside
of the world and its physical determinisms? According to them, the free subject is an absolute
origin, a first agent capable of creating first causes, who initiates new causal chains *ex nihilo*,
independent of the rest of the world. — Henri Atlan, *Is Science Inhuman*?

###### But how could we fail to see that there is an infinite regress here—if we do not accept, as Kantian and post-Kantian philosophies do.

**Lead-in emphasis.** According to them, the free subject is an absolute
origin, a first agent capable of creating first causes, who initiates new causal chains *ex nihilo*,
independent of the rest of the world. — Henri Atlan, *Is Science Inhuman*?

**This is bold text**

~~This was mistaken text~~

**This text is _extremely_ important**
	
***All this text is important***

> Text that is a quote

Use `git status` to list all new or modified files that haven't yet been committed.

Some basic Git commands are:
```
git status
git add
git commit
```

Python code:
```py
def hello(foo):
    print(foo)
````

This site was built using [GitHub Pages](https://pages.github.com/).

![This is an image](https://myoctocat.com/assets/images/base-octocat.svg)

- George Washington
- John Adams
- Thomas Jefferson
   - First nested list item
     - Second nested list item

1. James Madison
1. James Monroe
1. John Quincy Adams
1. First list item
   1. First nested list item
     1. Second nested list item

     
- [x] #739
- [ ] https://github.com/octo-org/octo-repo/issues/740
- [ ] Add delight to the experience when all tasks are complete :tada:

@octocat :+1: This PR looks great - it's ready to merge! :shipit:


Here is a simple footnote[^1].

A footnote can also have multiple lines[^2].  

You can also use words, to fit your writing style more closely[^note].

[^1]: My reference.
[^2]: Every new line should be prefixed with 2 spaces.  
  This allows you to have a footnote with multiple lines.
[^note]:
    Named footnotes will still render with numbers instead of the text but allow easier identification and linking.  
    This footnote also has been made with a different syntax using 4 spaces for new lines.


'''


def text_field_with_label(ui: UI):
    x = ui(input('Text field with label'))
    ui(f'You entered `{x}`.')


def main(ui: UI):
    x = ui(sample_markdown)
    x = ui(input('Text field with label'))
    ui(f'You entered `{x}`')
    x = ui(input('Text field with placeholder', placeholder='Enter text here'))
    x = ui(input('Text field with value', value='Some text'))
    x = ui(input('Text field, required', required=True))
    x = ui(input('Text field with input mask', mask='(999) 999 - 9999'))
    x = ui(input('Text field with icon', icon='Calendar'))
    x = ui(input('Text field with prefix', prefix='https://'))
    x = ui(input('Text field with suffix', suffix='.com'))
    x = ui(input('Text field with prefix and suffix', prefix='https://', suffix='.com'))
    x = ui(input('Text field with error', error='Something went wrong'))
    x = ui(input('Password field', password=True))
    x = ui(input('Multiline text field', lines=1))
    x = ui(input('Multiline text field, taller', lines=5))
    x = ui(input('Integer', value=5))
    x = ui(input('Integer within range', range=(0, 10)))
    x = ui(input('Integer within range, with step', range=(0, 10, 2)))
    x = ui(input('Integer within range, with default', value=5, range=(0, 10)))
    x = ui(input('Integer within range, origin from zero', value=3, range=(-5, 5)))
    x = ui(input('Decimal within range, with step', value=0.6, range=(-1, 1, 0.2)))
    x = ui(input('Integer range', value=(3, 7), range=(1, 10)))
    x = ui(input('Integer range, origin from zero', value=(-1, 3), range=(-5, 5)))
    x = ui(input('Integer field', value=5, editable=True))
    x = ui(input('Integer field with range', value=5, range=(1, 10), editable=True))
    x = ui(input('Integer field with range and step', value=50, range=(0, 100, 10), editable=True))
    x = ui(input('Decimal field with range and step', value=0.5, range=(0.0, 1.0, 0.05), editable=True))
    x = ui(input('Decimal field with range, step, and precision', value=0.5, range=(0.0, 1.0, 0.05, 2), editable=True))
    x = ui(input('Rating', mode='rating'))
    x = ui(input('Rating with value', mode='rating', value=3))
    x = ui(input('Rating with zero allowed', mode='rating', min=0))
    x = ui(input('Rating with max', mode='rating', value=3, max=10))
    x = ui(input('Rating with range', mode='rating', value=3, range=(0, 7)))
    x = ui(input('Time', mode='time', value='3:04PM'))
    x = ui(input('Time, with seconds', mode='time', value='3:04:05PM'))
    x = ui(input('Time, hour only', mode='time', value='3PM'))
    x = ui(input('Time, 24-hr clock', mode='time', value='15:04'))
    x = ui(input('Time, 24-hr clock, with seconds', mode='time', value='15:04:05'))
    x = ui(input('Time, hour only, 24-hour clock', mode='time', value='15'))
    x = ui(input('Day picker', mode='day', value='2021-10-10'))
    x = ui(input('Day picker with range', mode='day', value='2021-10-10', range=('2019-01-01', '2022-12-31')))
    x = ui(input('Week picker', mode='week', value='2021-10-10'))
    x = ui(input('Week picker with range', mode='week', value='2021-10-10', range=('2019-01-01', '2022-12-31')))
    x = ui(input('Month picker', mode='month', value='2021-10-10'))
    x = ui(input('Month picker with range', mode='month', value='2021-10-10', range=('2019-01-01', '2022-12-31')))
    x = ui(input('Options from string', options='Apples Bananas Cherries'))
    x = ui(input('Options from tuple', options=('Apples', 'Bananas', 'Cherries')))
    x = ui(input('Options from list', options=['Apples', 'Bananas', 'Cherries']))
    x = ui(input('Options from set', options={'Apples', 'Bananas', 'Cherries'}))
    x = ui(input('Options from tuples', options=(('a', 'Apples'), ('b', 'Bananas'), ('c', 'Cherries'))))
    x = ui(input('Options from dict', options={'Apples': 'a', 'Bananas': 'b', 'Cherries': 'c'}))
    x = ui(input('Options from dict', options=dict(Apples='a', Bananas='b', Cherries='c')))
    x = ui(input('Options', options=[
        option('a', 'Apples'),
        option('b', 'Bananas'),
        option('c', 'Cherries'),
    ]))
    x = ui(input('Options with selection', options=[
        option('a', 'Apples', selected=True),
        option('b', 'Bananas'),
        option('c', 'Cherries'),
    ]))
    x = ui(input('Multiple choice', multiple=True, options=[
        option('a', 'Apples'),
        option('b', 'Bananas'),
        option('c', 'Cherries'),
    ]))
    x = ui(input('Multiple choice, with selection', multiple=True, options=[
        option('a', 'Apples', selected=True),
        option('b', 'Bananas'),
        option('c', 'Cherries'),
    ]))
    x = ui(input('Multiple choice, with multiple selections', multiple=True, options=[
        option('a', 'Apples', selected=True),
        option('b', 'Bananas', selected=True),
        option('c', 'Cherries'),
    ]))
    x = ui(input('Multiple choice, required', multiple=True, required=True, options=[
        option('a', 'Apples'),
        option('b', 'Bananas'),
        option('c', 'Cherries'),
    ]))
    x = ui(input('Multiple choice, with error message', multiple=True, error='Something went wrong', options=[
        option('a', 'Apples'),
        option('b', 'Bananas'),
        option('c', 'Cherries'),
    ]))
    x = ui(input('Multiple choice, editable', multiple=True, editable=True, options=[
        option('a', 'Apples'),
        option('b', 'Bananas'),
        option('c', 'Cherries'),
    ]))
    x = ui(input('Tag Picker', mode='tag', options=[
        option('a', 'Apples'),
        option('b', 'Bananas'),
        option('c', 'Cherries'),
    ]))
    x = ui(input('Choice list', placeholder='Pick a fruit', options=[
        option('a', 'Apples'),
        option('b', 'Bananas'),
        option('c', 'Cherries'),
    ]))
    x = ui(input('Choice list, required', placeholder='Pick a fruit', required=True, options=[
        option('a', 'Apples'),
        option('b', 'Bananas'),
        option('c', 'Cherries'),
    ]))
    x = ui(input('Choice list, with icons', placeholder='Pick a fruit', required=True, options=[
        option('area', 'Area', icon='AreaChart', selected=True),
        option('bar', 'Bar', icon='BarChartHorizontal'),
        option('column', 'Column', icon='BarChartVertical'),
        option('line', 'Line', icon='LineChart'),
        option('scatter', 'Scatter', icon='ScatterChart'),
        option('donut', 'Donut', icon='DonutChart'),
    ]))
    x = ui(input('Choice list, with error message', placeholder='Pick a fruit', error='Something went wrong', options=[
        option('a', 'Apples'),
        option('b', 'Bananas'),
        option('c', 'Cherries'),
    ]))
    x = ui(input('Choice list, editable', placeholder='Pick a fruit', editable=True, options=[
        option('a', 'Apples'),
        option('b', 'Bananas'),
        option('c', 'Cherries'),
    ]))
    x = ui(input('Choice list, grouped', placeholder='Pick an item', options=[
        option('f', 'Fruits', options=[
            option('a', 'Apples'),
            option('b', 'Bananas'),
            option('c', 'Cherries'),
        ]),
        option('v', 'Vegetables', options=[
            option('l', 'Lettuce'),
            option('t', 'Tomato'),
        ]),
    ]))
    x = ui(input('Color picker', mode='color', value='#a241e8'))
    x = ui(input('Color picker, with choices', mode='color', options=[
        option('#ca5010', 'Orange'),
        option('#038387', 'Cyan'),
        option('#8764b8', 'Purple'),
        option('#881798', 'Magenta'),
    ]))
    x = ui(input('Buttons, vertical', options=[
        option('a', 'Apples'),
        option('b', 'Bananas'),
        option('c', 'Cherries'),
    ], inline=False))
    x = ui(input('Compound buttons', options=[
        option('yes', 'Sign me up!', caption='Terms and conditions apply', selected=True),
        option('no', 'Not now', caption="I'll decide later"),
    ]))
    x = ui(input('Button with menu', options=[
        option('yes', 'Yes', selected=True, options=[
            option('later', 'Remind me later', icon='ChatBot'),
            option('never', "Don't ask me again", icon='MuteChat'),
        ]),
        option('no', 'No'),
    ]))
    x = ui(input('Button with menu', options=[
        option('yes', 'Yes', selected=True),
        option('no', 'No', options=[
            option('later', 'Remind me later', icon='ChatBot'),
            option('never', "Don't ask me again", icon='MuteChat'),
        ]),
    ]))
    x = ui(input('Add a new chart', options=[
        option('area', 'Area', icon='AreaChart'),
        option('bar', 'Bar', icon='BarChartHorizontal'),
        option('column', 'Column', icon='BarChartVertical'),
        option('line', 'Line', icon='LineChart'),
        option('scatter', 'Scatter', icon='ScatterChart'),
        option('donut', 'Donut', icon='DonutChart'),
    ]))
    x = ui(
        input('Username', placeholder='someone@company.com'),
        input('Password', password=True),
    )
    x = ui(
        input('Username', placeholder='someone@company.com'),
        input('Password', password=True),
        inline=True,
    )
    x = ui(
        input('Username', placeholder='someone@company.com'),
        input('Password', password=True),
        input(options=[option('login', 'Login', selected=True)]),
        inline=True,
    )
    x = ui(
        stack(input('First name'), input('Last name'), inline=True),
        input('Address line 1'),
        input('Address line 2'),
        stack(input('City'), input('State'), input('Zip'), inline=True),
    )
    x = ui(
        stack(input('First name'), input('M.I.', width='10%'), input('Last name'), inline=True),
        input('Address line 1'),
        input('Address line 2'),
        stack(input('City', grow=5), input('State', width='20%'), input('Zip', grow=1), inline=True),
        input(options=[
            option('yes', 'Sign me up!', caption='Terms and conditions apply', selected=True),
            option('no', 'Not now', caption="I'll decide later"),
        ])
    )


# --- bootstrap ---

def main_wrap(ui: UI):
    try:
        main(ui)
    except ContextSwitchError as e:
        # perform clean-up
        raise e


nitro = UI(main_wrap, title='Nitro', caption='v0.1', menu=[
    option(main2, 'Area Chart', icon='AreaChart'),
    option(main2, 'Bar Chart', icon='BarChartVertical'),
    option(main2, 'Line Chart', icon='LineChart'),
    option(main2, 'Bar Chart', icon='BarChartVertical', options=[
        option(main2, 'Area Chart', icon='AreaChart'),
        option(main2, 'Line Chart', icon='LineChart'),
        option(main2, 'Scatter Chart', icon='ScatterChart'),
    ]),
    option(''),
    option(main2, 'Scatter Chart', icon='ScatterChart'),
])

app = Flask(__name__, static_folder='../web/build', static_url_path='')


@app.route('/nitro', websocket=True)
def socket():
    ws = simple_websocket.Server(request.environ)
    try:
        nitro.serve(ws.send, ws.receive)
    except simple_websocket.ConnectionClosed:
        pass
    return ''


if __name__ == '__main__':
    app.run()
