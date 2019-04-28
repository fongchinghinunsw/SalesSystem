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
Models grouped to multiple py files. Put under src/app/app/models/

## Development
**For Milestone 3: see Milestone 3 Submission Details in root README.md**

For local development, use virtualenv. Usage:
```
cd src/app/
virtualenv --python=python3 venv
pip install -r requirements.txt
source venv/bin/activate
```

To run dev server, cd into `src/`. And run `python -m app run`

To run unit tests, run `pytest`

After usage, run `deactivate` to exit from virtualenv.

## Deployment
**For Milestone 3: see Milestone 3 Submission Details in root README.md**

cd into src/ and run `docker-compose up`
