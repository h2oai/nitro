# Writing plugins

Plugins can load third-party or custom Javascript into Nitro's user interface, and provide new variations of
Nitro's `box()` function that can allow an app to render and interact with new kinds of components, like visualizations,
graphics, tables, and so on.

!!! warning 
    This is an experimental feature. API is subject to change.

## Write a plugin

Writing your own plugin is easy if you know Javascript, HTML, CSS and a bit of client-server programming.

There are two parts to a plugin: *client-side* (the part that executes in the web browser) and *server-side*
(the part that executes on the server).

- The *client-side* can dynamically import Javascript files and source code into the browser.
- The *server-side* consists of plain Python code that can do two things:
    - Invoke the imported Javascript to render components, and
    - Handle inputs or events from these components.

Writing the client-side part is simply a matter of providing a list of Javascript files and/or source code to import:

```py
# unicorn_plugin_package.py

from h2o_nitro import Plugin, Script

custom_javascript = '''
exports.show_count = (context, element, data) => {
    // - 'context' is an object with two methods:
    //   - 'context.record(value)' records the value of this box.
    //   - 'context.commit()' commits all recorded values.
    // - 'element' is the box's HTML element.
    // - 'data' is a dictionary-like object whose fields
    //   hold values sent by Python. 
    element.innerText = data.unicorn_count
};
'''

unicorn_plugin = Plugin(
    name='unicorn',
    scripts=[
        Script(source='https://cdn.example.com/foo.js'),
        Script(source='https://cdn.example.com/bar.js'),
        Script(source='/qux.js'),
        Script(source=custom_javascript, type='inline'),
    ],
)
```

In the above example, `custom_javascript` is expected to add one or more functions to the `exports` object.

The server-side part of the plugin can invoke the exported Javascript like this:

```py 
def unicorn_box(count: int) -> Box:
    return box(mode='plugin:unicorn.show_count', data=dict(unicorn_count=count))
```

## Use the plugin

The plugin `unicorn_plugin` can now be loaded to a Nitro instance during initialization, like this:

```py
# app.py

from unicorn_plugin_package import unicorn_plugin

nitro = View(
    main,
    title='My App',
    caption='v0.42',
    plugins=[unicorn_plugin],  # Include the plugin
)
```

Finally, use the `unicorn_box()` function to render the custom box.

```py 
# app.py

from unicorn_plugin_package import unicorn_box

def main(view: View):
    view(unicorn_box(42))
```

Effectively, `unicorn_box(42)` translates to `box(mode='plugin:unicorn.show_count', data={'unicorn_count':42})`, which
in turn translates to a Javascript invocation `unicorn.show_count(context, element, { unicorn_count: 42 })`.

## Learn more

A good way to write your own plugin is to find an existing plugin that's similar, then copy and modify it.

Happy hacking!
