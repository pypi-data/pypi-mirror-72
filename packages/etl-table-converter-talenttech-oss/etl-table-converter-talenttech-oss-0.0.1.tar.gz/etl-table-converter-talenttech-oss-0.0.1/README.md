ETL table converter

config-from db to db
dialect - sql-alchemy dialect
```sh
sql_credentials = {
        "pg": {
            "dialect": "postgresql",
            "database": os.getenv("PG_DATABASE"),
            "schema": os.getenv("PG_SCHEMA"),
            "user": os.getenv("PG_USER"),
            "host": os.getenv("PG_HOST"),
            "port": os.getenv("PG_PORT"),
            "password": os.getenv("PG_PASSWORD")
        },
        "ch": {
            "dialect": "clickhouse+native",
            "database": os.getenv("CH_DATABASE"),
            "user": os.getenv("CH_USER"),
            "host": os.getenv("CH_HOST"),
            "port": os.getenv("CH_PORT"),
            "password": os.getenv("CH_PASSWORD")
        },
        "vertica": {
            "dialect": "vertica+vertica_python",
            "database": os.getenv("VERTICA_DATABASE"),
            "schema": os.getenv("VERTICA_SCHEMA"),
            "user": os.getenv("VERTICA_USER"),
            "host": os.getenv("VERTICA_HOST"),
            "port": os.getenv("VERTICA_PORT"),
            "password": os.getenv("VERTICA_PASSWORD")
        },
    }
```

Usage
```sh
pip3 install etl-table-converter-talenttech-oss
```

```python
from converter.fields_converter import FieldsConverter
from_db="vertica"
to_db="ch"
converter = FieldsConverter(sql_credentials, from_db, to_db)
tables = [
    "table_name1",
    "table_name2"
]
converter.create_list_of_tables(tables, dir="/")
