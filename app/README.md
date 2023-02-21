# Local development 

## Docker

To access replica state and feature stores the app can be served 
locally using docker-compose. Run `make deploy` with `ENVIRONMENT=local`
set.

## No-docker

Without other Docker services the app can be deployed locally with

```
python -m venv app
. app/bin/activate
pip install -r requirements.txt
python app.py
```
