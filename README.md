**get started:**

- install python 3.6.7 and set up a virtual environment
- `pip install -r requirements.txt`
- `pip install -e .`
- Open grocery_mart_api/config.py and set `SQLALCHEMY_DATABASE_URI` to your valid uri.
- Start postgreSQL `pg_ctl -D /usr/local/var/postgres -l /usr/local/var/postgres/server.log start`
- From postgre command line run `createdb grocery_mart_api`. If it doesn't work use `CREATE DATABASE grocery_mart_api`
- Run `grocery_mart_api db upgrade` from terminal to match production database.
- Run `grocery_mart_api run` to run ecom data layer
