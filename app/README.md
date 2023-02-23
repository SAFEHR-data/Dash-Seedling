# Local development 

## Docker

To access replica state and feature stores the app can be served 
locally using docker-compose. Run `make serve-local` with `ENVIRONMENT=local`
set.

## No-docker

Without other containerised services the app can be deployed locally with

```
python -m venv app  # create a virtual environment
. app/bin/activate
pip install -r requirements.txt
python app.py
```
