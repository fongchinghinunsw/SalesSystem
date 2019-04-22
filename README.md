**FOR MILESTONE 3 SUBMISSION DETAILS, SEE MILESTONE 3 SUBMISSION SECTION DOWN BELOW**

# Sales System
**COMP 1531 Group Project, 19T1**

Adam Yi, Qingyi Zhang, Stephen Fong <comp1531-mcdonalds@withadamyi.com, {z5231521, z5173546, z5191673}@cse.unsw.edu.au, i@adamyi.com>

For project architecture, please see [architecture.md](docs/architecture.md)

For coding style, please see [style.md](docs/style.md)

User stories currently at https://docs.google.com/spreadsheets/d/1wZ794XR8N1M9bWgASx4JkzMh-WmmB8M1dfChf0Xzh8Y/edit

Typesetted version at https://docs.google.com/document/d/18cd048HCGWWj9Pxx0DIyPlCec7mcsh0LN66ZKyXKw30/edit

UML at https://drive.google.com/open?id=1Vlh4jhX4Qese-rn7upasG6vfkCvUOr6R

## Git at yiad.am

We use [Git @ yiad.am](https://git.yiad.am) for code review and continuous integration. Please follow [quickstart](https://git.yiad.am/review/Documentation/intro-gerrit-walkthrough.html), [user guide](https://git.yiad.am/review/Documentation/intro-user.html), and [documentation]( https://git.yiad.am/review/Documentation/index.html).

All upsteam changes are synced by ReviewBara (not-yet open-sourced) to GitHub.

## Milestone 3 Submission

### Dependencies

src/app/requirements.txt

### Deployment

For Milestone 3 submission, the following value has been set in src/app/settings.py: `SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/db.sql"`

For test server deployment, please run
```
cd src
python -m app createdb
python -m app run
```

For team members (rather than MS3): prod stable deployment
Revert SQLite back to `SQLALCHEMY_DATABASE_URI = "mysql+pymysql://sales:SECURE_SALES_PWD@db/sales"`
Use docker-compose to deploy containers

### Unit Test

For Milestone 3 submission, unit tests are at src/app/milestone3_tests
They can be run via `src/app/milestone3_tests/run_test.sh`

For team members (rather than MS3): internal unit tests are at src/app/tests
