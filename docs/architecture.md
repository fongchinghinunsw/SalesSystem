# Architecture
Docker + Python 3.7 + Flask + MySQL

## Containers
1. **app** (src/app): Flask core
2. **db** (src/db): MySQL

## Flask Blueprints
1. **customer** (route: /): all frontend functionalities for customers
2. **accounts** (route: /accounts/): register/login/user profile etc
3. **admin** (route: /admin/): all admin/manager functionalities

## Flask Models
Each model in a seperate py file. Put under src/app/app/models/

## Development
For local development, use virtualenv. Usage:
```
cd src/app/
virtualenv --python=python3 venv
pip install -r requirements.txt
source venv/bin/activate
```

To run dev server, cd into `src/`. And run `python -m app`

To run unit tests, cd into `src/app/`. And run `pytest`

After usage, run `deactivate` to exit from virtualenv.

## Deployment
cd into src/ and run `docker-compose up`
