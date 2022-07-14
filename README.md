# AP_ACADEM

## Prerequisites

To use this code you must have python installed on your machine and also preferably pyenv (or any other alternative you are more comfortable with).

## Setting up the project

First of all, let`s clone the project

```bash
git clone https://github.com/umbrelluck/AP_ACADEM.git
```

Then set up python environment

```bash
# get specific python version
pyenv install 3.8.9
# set specific version for usage in virtual environment
pyenv local 3.8.9

# create virtual environment
python -m venv .venv

# activate environment
# In cmd.exe
venv\Scripts\activate.bat
# In PowerShell
venv\Scripts\Activate.ps1
# Linux and MacOS
$ source myvenv/bin/activate

python -m pip install -r requirements.txt
```

After setting python environment, let`s set up alembic

```bash
# create alembic configurations file and folder for migrations
alembic init migrations
```

In `alembic.ini` find `sqlalchemy.url` and set it to desiarable path (for simplicity lei it be `sqlite:///database.db`). Do not forget to change path also in `app.py` in `app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'`.

Now, in `migrations/env.py` find `target_metadata = None` and change it to

```python
from models import BankAccount, User, Role, db
target_metadata = db.Model.metadata
```

Now it is time for creating migration

```bash
alembic revision --autogenerate -m "name of migration"
alembic upgrade head
```

## Serving

To serve, one may run `flask run`. This project includes `waitress`. To use it, execute

```bash
# url:port may be 127.0.0.1:8080
waitress-serve --listen=url:port app:app #no reload on code change

# or

hupper -m waitress --listen=url:port app:app #auto reload on code change 
```

## Usage

API usage can be seen in `swagger.yaml`.

General information:

* `test-api/bank` is for testing purposes, data is stored in `testData` in `APIs/test_api.py`.
* `api/bank` works with created database.

To view all data in database, go to `SERVE_URL/` or `SERVE_URL/admin`. There is already user created with max authority. You can also register another user and assign him a role.
