# event-registration

A simple Python event registration web app built with Flask.

## Setup

1. Install Python 3.11+.
2. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

## Run

```powershell
python app.py
```

Then open `http://localhost:5000` in your browser.

## Tests

```powershell
pytest -q
```

## Jenkins Pipeline

The included `Jenkinsfile` demonstrates:

- checkout source from SCM
- create a Python virtual environment
- install dependencies from `requirements.txt`
- run `pytest` tests
- package source as a build artifact (`.zip` on Windows, `.tar.gz` on Unix)

> Note: adjust the Windows/Unix commands for your Jenkins agent environment.
