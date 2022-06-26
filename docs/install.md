# Getting Started

H2O Nitro can be installed from [PyPI](https://pypi.org/project/h2o-nitro/):

```
pip install "h2o-nitro[web]"
```

## Prerequisites

You will need Python 3.7 or later installed on your system.

## Hello World!

To build apps with Nitro, you'll also need something like [Flask](https://flask.palletsprojects.com/),
[Tornado](https://www.tornadoweb.org/), or [Starlette](https://www.starlette.io/)
to host [WebSocket](https://en.wikipedia.org/wiki/WebSocket) connections.

### Using Flask

Get the "Hello World" example [hello.py](https://raw.githubusercontent.com/h2oai/nitro/main/py/examples/hello.py), then:

=== "Linux / macOS"

    ```sh
    # Create a virtual environment
    python3 -m venv venv
    source venv/bin/activate

    # Install Nitro and Flask:
    pip install h2o-nitro flask simple-websocket

    # Run the app:
    python hello.py
    ```
    

=== "Windows"

    ```bat
    :: Create a virtual environment and activate:
    python -m venv env
    .\env\Scripts\activate

    :: Install Nitro and Flask:
    pip install h2o-nitro flask simple-websocket

    :: Run the app:
    python hello.py
    ```

!!! success "Play with the app"
    Go to [http://localhost:5000/](http://localhost:5000/).

### Using Tornado

Get the "Hello World" example [hello_tornado.py](https://raw.githubusercontent.com/h2oai/nitro/main/py/examples/hello_tornado.py), then:

=== "Linux / macOS"

    ```sh
    # Create a virtual environment
    python3 -m venv venv
    source venv/bin/activate

    # Install Nitro and Tornado:
    pip install h2o-nitro tornado

    # Run the app:
    python hello_tornado.py
    ```


=== "Windows"

    ```bat
    :: Create a virtual environment and activate:
    python -m venv env
    .\env\Scripts\activate

    :: Install Nitro and Tornado:
    pip install h2o-nitro flask simple-websocket

    :: Run the app:
    python hello_tornado.py
    ```

!!! success "Play with the app"
    Go to [http://localhost:5000/](http://localhost:5000/).

### Using Starlette

Get the "Hello World" example [hello_starlette.py](https://raw.githubusercontent.com/h2oai/nitro/main/py/examples/hello_starlette.py), then:

=== "Linux / macOS"

    ```sh
    # Create a virtual environment
    python3 -m venv venv
    source venv/bin/activate

    # Install Nitro and Starlette:
    pip install h2o-nitro uvicorn starlette websockets

    # Run the app:
    python -m uvicorn hello_starlette:app --reload --port 5000
    ```


=== "Windows"

    ```bat
    :: Create a virtual environment and activate:
    python -m venv env
    .\env\Scripts\activate

    :: Install Nitro and Starlette:
    pip install h2o-nitro uvicorn starlette websockets

    :: Run the app:
    python -m uvicorn hello_starlette:app --reload --port 5000
    ```

!!! success "Play with the app"
    Go to [http://localhost:5000/](http://localhost:5000/).

## Summary

Nitro is a library, and plugs into [Flask](https://flask.palletsprojects.com/), 
[Tornado](https://www.tornadoweb.org/), [Starlette](https://www.starlette.io/) and other popular frameworks.

There's no need to start a brand new project either, you can easily use it in your existing applications, too!

## Next steps

- [Install the CLI](cli.md): The Nitro CLI makes it easy to set up and play around with apps.
- [Get the live docs](live-docs.md): Play around with an interactive version of these docs.
- [Read the guide](basics.md): Deep-dive into what Nitro can do for you.
- [Try more examples](examples.md): Learn, modify and share your creations with the community.

