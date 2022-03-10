from h2o_nitro import UI, input, option
import simple_websocket
from flask import Flask, request


def main2(ui: UI):
    counter = 0
    while True:
        choice = ui([
            f'Count={counter}',
            input(options=('+', '-')),
        ])
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

According to them, the free subject is an absolute
origin, a first agent capable of creating first causes, who initiates new causal chains *ex nihilo*,
independent of the rest of the world. — Henri Atlan, *Is Science Inhuman*?

**This is bold text**

*This text is italicized*

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


def main(ui: UI):
    x = ui([sample_markdown])
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


@app.route('/nitro', websocket=True)
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
