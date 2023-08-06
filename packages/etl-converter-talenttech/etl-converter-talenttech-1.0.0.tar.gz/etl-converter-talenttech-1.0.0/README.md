ETL table converter and creator
==========

The Python Toolkit for converting table from one database to another

Databases types
-------------

Supported databases. You have to use short name of database
short_name:type of database 
* ch:clickhouse
* pg:postgresql
* mysql:mysql
* vertica:vertica
* exasol:exasol


Supported database conversions
-------------
* mysql to pg
* mysql to vertica
* mysql to exasol
* ch to vertica
* pg to vertica


Credentials
-------------
```sh
sql_credentials = {
        "pg": {
            "type": "pg",
            "database": os.getenv("PG_DATABASE"),
            "schema": os.getenv("PG_SCHEMA"),
            "user": os.getenv("PG_USER"),
            "host": os.getenv("PG_HOST"),
            "port": os.getenv("PG_PORT"),
            "password": os.getenv("PG_PASSWORD")
        },
        "ch": {
            "type": "ch",
            "database": os.getenv("CH_DATABASE"),
            "user": os.getenv("CH_USER"),
            "host": os.getenv("CH_HOST"),
            "port": os.getenv("CH_PORT"),
            "password": os.getenv("CH_PASSWORD")
        },
        "vertica": {
            "type": "vertica",
            "database": os.getenv("VERTICA_DATABASE"),
            "schema": os.getenv("VERTICA_SCHEMA"),
            "user": os.getenv("VERTICA_USER"),
            "host": os.getenv("VERTICA_HOST"),
            "port": os.getenv("VERTICA_PORT"),
            "password": os.getenv("VERTICA_PASSWORD")
        },
        "mysql": {
            "type": "mysql",
            "database": os.getenv("MYSQL_DATABASE"),
            "user": os.getenv("MYSQL_USER"),
            "host": os.getenv("MYSQL_HOST"),
            "port": os.getenv("MYSQL_PORT"),
            "password": os.getenv("MYSQL_PASSWORD")
        },
    }
```

Usage
```sh
pip3 install etl-converter-talenttech
```

```python
import os
from converter.fields_converter import FieldsConverter


from_db = "mysql"
to_db = "pg"
converter = FieldsConverter(sql_credentials, from_db, to_db)
tables = [
    "directions",
    "users"
]
print(converter.create_list_of_tables(tables, to_create=False, dir=None))