Welcome to H2O Nitro!
=====================

Learn more at https://nitro.h2o.ai

Like Nitro? Please take a moment to star us on Github:
https://github.com/h2oai/nitro

Thank you, and happy hacking!

Setup
-----

You will need Python 3.7+.

Change to the app directory:

    cd APP_DIR

Create a new virtual environment:

    python3 -m venv venv

Install dependencies:

    ./venv/bin/pip install -r requirements.txt

Run your app:

    ./venv/bin/python app.py

Or, to run your app with auto-reload during development:

    ./venv/bin/uvicorn app:app --reload --port 5000

Access your app at http://localhost:5000/
