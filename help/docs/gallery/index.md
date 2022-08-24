---
template: overrides/main.html
---
# Examples

It's easy to run these examples on your computer.

1. [Install the `nitro` CLI](../cli.md#install).
2. Create and switch to a new directory, say, `nitro_examples`.
3. Execute `nitro run http://path/to/example.py`.

!!! info 
    If you run multiple examples from the same working directory, `nitro run` will reuse the virtual environment 
    already present in that directory.

!!! tip
    If you simply want to fetch, but not run the example, use `nitro clone` instead of `nitro run`.

## Basic Examples

### Hello World using Flask

A simple app, using [Flask](https://flask.palletsprojects.com/).

Source: https://github.com/h2oai/nitro/blob/main/py/demo/hello_flask.py

!!!example "Run"
    ```
    nitro run https://raw.githubusercontent.com/h2oai/nitro/main/py/demo/hello_flask.py
    ```

### Hello World using Tornado

Same example as above, but using [Tornado](https://www.tornadoweb.org/en/stable/index.html).

Source: https://github.com/h2oai/nitro/blob/main/py/demo/hello_tornado.py

!!!example "Run"
    ```
    nitro run https://raw.githubusercontent.com/h2oai/nitro/main/py/demo/hello_tornado.py
    ```

### Hello World using Starlette

Same example as above, but using [Starlette](https://www.starlette.io/) and [Uvicorn](https://www.uvicorn.org/).

Source: https://github.com/h2oai/nitro/blob/main/py/demo/hello_starlette.py

!!!example "Run"
    ```
    nitro run https://raw.githubusercontent.com/h2oai/nitro/main/py/demo/hello_starlette.py
    ```

### Apply for space flight

A job application wizard. Seven pages in seven statements!

Source: https://github.com/h2oai/nitro/blob/main/py/demo/space_flight.py

!!!example "Run"
    ```
    nitro run https://raw.githubusercontent.com/h2oai/nitro/main/py/demo/space_flight.py
    ```

### Back button state handling

How to track state when the user clicks back/forward to navigate between pages.

Source: https://github.com/h2oai/nitro/blob/main/py/demo/back_button.py

!!!example "Run"
    ```
    nitro run https://raw.githubusercontent.com/h2oai/nitro/main/py/demo/back_button.py
    ```

## Data Visualization

### Using Matplotlib

How to use [Matplotlib](https://matplotlib.org/stable/index.html) in Nitro apps.

Source: https://github.com/h2oai/nitro-matplotlib/blob/main/examples/matplotlib_basic.py

!!!example "Run"
    ```
    nitro run https://raw.githubusercontent.com/h2oai/nitro-matplotlib/main/examples/matplotlib_basic.py
    ```

### Using Seaborn

How to use [Seaborn](https://seaborn.pydata.org/) in Nitro apps.

Source: https://github.com/h2oai/nitro-matplotlib/blob/main/examples/seaborn_basic.py

!!!example "Run"
    ```
    nitro run https://raw.githubusercontent.com/h2oai/nitro-matplotlib/main/examples/seaborn_basic.py
    ```

### Using Bokeh

How to use [Bokeh](https://docs.bokeh.org/en/latest/) in Nitro apps.

Source: https://github.com/h2oai/nitro-bokeh/blob/main/examples/bokeh_basic.py

!!!example "Run"
    ```
    nitro run https://raw.githubusercontent.com/h2oai/nitro-bokeh/main/examples/bokeh_basic.py
    ```

### Using Altair

How to use [Altair](https://altair-viz.github.io/index.html) in Nitro apps.

Source: https://github.com/h2oai/nitro-altair/blob/main/examples/altair_basic.py

!!!example "Run"
    ```
    nitro run https://raw.githubusercontent.com/h2oai/nitro-altair/main/examples/altair_basic.py
    ```
