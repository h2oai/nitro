# Markdown



## Basics

Strings passed to `view()` are interpreted as [Github Flavored Markdown](https://github.github.com/gfm/) (GFM).

`view(text)` is shorthand for `view(box(text))`.


```py
view('''
# Heading 1
## Heading 2
### Heading 3 
#### Heading 4
##### Heading 5 
###### Heading 6

This is a paragraph, with **bold**, *italics* 
(or _italics_), ***important***, `code`
and ~~strikethrough~~ formatting.

Here's a [hyperlink](https://example.com) to https://example.com.

![An image](https://picsum.photos/200)

> This is a block quote.

- List item 1
- List item 2
  - Sublist item 1
  - Sublist item 2
- List item 3

1. Numbered list item 1
1. Numbered list item 2
  1. Sublist item 1
  1. Sublist item 2
1. Numbered list item 3

Here is a footnote[^1] and another one[^another].

[^1]: A reference.
[^another]: Another reference.
''')
```


Any uniform indentation is automatically ignored.


![Screenshot](assets/screenshots/markdown_basic.png)


## Links as inputs

Local links in markdown content behave just like any other input.

Clicking on a local link returns the name of the link.


```py
choice = view('''
Pick a flavor:
- [Vanilla](#vanilla)
- [Strawberry](#strawberry)
- [Chocolate](#chocolate)

Or, [surprise me](#surprise-me)!
''')
view(f'You clicked on {choice}.')
```


![Screenshot](assets/screenshots/markdown_links.png)


## Tables

Draw tables using `---` and `|`.

- Use three or more hyphens (`---`) to create each column’s header.
- Use `|` to separate each column.
- Use `:---` to left-align text.
- Use `:---:` to center text.
- Use `---:` to right-align text.


```py
view('''

### Basic Tables

| Flavor         | Super cheap! |
| -------------- | ------------ |
| Cinnamon Sugar | $1.99        |
| Powdered Sugar | $1.99        |
| Vanilla        | $2.99        |
| Chocolate      | $2.99        |
| Blueberry      | $2.99        |

### Column alignment

| Flavor         | Super cheap! | Extras                |
| -------------: | :----------: | :-------------------- |
| Cinnamon Sugar | $1.99        | Sugar and spice.      |
| Powdered Sugar | $1.99        | Served warm.          |
| Vanilla        | $2.99        | With cookie crumbles. |
| Chocolate      | $2.99        | With sprinkles.       |
| Blueberry      | $2.99        | With real blueberry.  |

''')
```


![Screenshot](assets/screenshots/markdown_table.png)


## Tables from lists

It's often easier to construct tables from lists of things, as shown below.


```py
def show_table(view: View):
    view(make_table([
        ['Flavor', 'Super cheap!'],
        ['Cinnamon Sugar', '$1.99'],
        ['Powdered Sugar', '$1.99'],
        ['Vanilla', '$2.99'],
        ['Chocolate', '$2.99'],
        ['Blueberry', '$2.99'],
    ]))


def make_table_row(row):
    return f"| {' | '.join(row)} |"


def make_table(rows):
    rows = [rows[0], ['---'] * len(rows[0]), *rows[1:]]
    return '\n'.join([make_table_row(row) for row in rows])
```


![Screenshot](assets/screenshots/show_table.png)


## Syntax highlighting

Code blocks in Markdown support syntax highlighting for 180+ languages using [highlight.js](https://highlightjs.org/).

To enable syntax highlighting, suffix the language to the opening triple-backticks.

[See list of supported languages](https://github.com/highlightjs/highlight.js/blob/main/SUPPORTED_LANGUAGES.md).


```py
view('''
Python:
```py
def hello():
    print('Hello!')
```

Ruby:
```rb
def hello
    puts "Hello!"
end
```

Javascript:
```js
function hello() {
    console.log('Hello!');
}
```
''')
```


![Screenshot](assets/screenshots/markdown_syntax_highlighting.png)
