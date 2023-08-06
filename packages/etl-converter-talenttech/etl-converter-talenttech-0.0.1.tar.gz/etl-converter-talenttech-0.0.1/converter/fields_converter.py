import logging
import sys
import warnings
from sqlalchemy.engine import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table

warnings.filterwarnings("ignore")

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s  %(name)s  %(levelname)s: %(message)s",
)
logging.basicConfig(
    stream=sys.stderr,
    level=logging.ERROR,
    format="%(asctime)s  %(name)s  %(levelname)s: %(message)s",
)
logging.captureWarnings(True)

types_converter_dict = {
    "mysql-pg": {
        "char": "character",
        "varchar": "character varying",
        "tinytext": "text",
        "mediumtext": "text",
        "text": "text",
        "longtext": "text",
        "tinyblob": "bytea",
        "mediumblob": "bytea",
        "longblob": "bytea",
        "binary": "bytea",
        "varbinary": "bytea",
        "bit": "bit varying",
        "tinyint": "smallint",
        "tinyint unsigned": "smallint",
        "smallint": "smallint",
        "smallint unsigned": "integer",
        "mediumint": "integer",
        "mediumint unsigned": "integer",
        "int": "integer",
        "int unsigned": "bigint",
        "bigint": "bigint",
        "bigint unsigned": "numeric",
        "float": "real",
        "float unsigned": "real",
        "double": "double precision",
        "double unsigned": "double precision",
        "decimal": "numeric",
        "decimal unsigned": "numeric",
        "numeric": "numeric",
        "numeric unsigned": "numeric",
        "date": "date",
        "datetime": "timestamp without time zone",
        "time": "time without time zone",
        "timestamp": "timestamp without time zone",
        "year": "smallint",
        "enum": "character varying (with check constraint)",
        "set": "ARRAY[]::text[]",
    },
    "mysql:vertica": {
        "text": "long varchar",
        "json": "long varchar",
        "enum": "long varchar",
        "double": "double precision",
    },
    "mysql:exasol": {
        "text": "varchar",
        "json": "varchar",
        "enum": "varchar",
        "blob": "varchar",
        "set": "varchar",
        "tinytext": "varchar",
        "datetime": "timestamp",
    },
    "ch:vertica": {
        "string": "long varchar",
        "uuid": "long varchar",
        "uint8": "bigint",
        "uint16": "bigint",
        "uint32": "bigint",
        "uint64": "bigint",
        "int64": "bigint",
        "int8": "bigint",
        "int16": "bigint",
        "int32": "bigint",
        "int64": "bigint",
    },
    "pg:vertica": {},
}


def update_column_type_from_mysql_to_vertica(column):
    type = column["DATA_TYPE"]
    if column["DATA_TYPE"] in ("text", "json", "enum"):
        type = "long varchar"
    elif column["DATA_TYPE"] in ("double"):
        type = "double precision"
    if column["CHARACTER_MAXIMUM_LENGTH"] is not None:
        type += "({CHARACTER_MAXIMUM_LENGTH})".format(
            CHARACTER_MAXIMUM_LENGTH=int(column["CHARACTER_MAXIMUM_LENGTH"] * 2)
        )
        return type
    if column["COLUMN_DEFAULT"] is not None:
        type += " default '{COLUMN_DEFAULT}'".format(
            COLUMN_DEFAULT=column["COLUMN_DEFAULT"]
        ).replace("'CURRENT_TIMESTAMP'", "now()")

    return type


def update_column_type_from_mysql_to_exasol(column):
    type = column["DATA_TYPE"]
    if column["DATA_TYPE"] in ("text", "json", "enum", "blob", "set", "tinytext"):
        type = "varchar"
    if column["DATA_TYPE"] in ("datetime"):
        type = "timestamp"
    if column["CHARACTER_MAXIMUM_LENGTH"] is not None:
        type += "({CHARACTER_MAXIMUM_LENGTH})".format(
            CHARACTER_MAXIMUM_LENGTH=column["CHARACTER_MAXIMUM_LENGTH"]
        )
        return type
    if column["COLUMN_DEFAULT"] is not None:
        type += " default '{COLUMN_DEFAULT}'".format(
            COLUMN_DEFAULT=column["COLUMN_DEFAULT"]
        ).replace("'CURRENT_TIMESTAMP'", "CURRENT_TIMESTAMP")
    if type == "varchar":
        type += "(65500)"
    return type


def update_column_type_from_ch_to_vertica(column):
    type = column["DATA_TYPE"]
    if column["DATA_TYPE"] in ("string", "uuid"):
        type = "long varchar(65000)"
    elif column["DATA_TYPE"] in (
        "uint8",
        "uint16",
        "uint32",
        "uint64",
        "int64",
        "int8",
        "int16",
        "int32",
        "int64",
    ):
        type = "bigint"
    elif column["DATA_TYPE"] in ("float64"):
        type = "double precision"

    if column["COLUMN_DEFAULT"] is not None and column["COLUMN_DEFAULT"] != "":
        type += " default '{COLUMN_DEFAULT}'".format(
            COLUMN_DEFAULT=column["COLUMN_DEFAULT"]
        )
    return type
    # return "long varchar(30)"


def update_column_type_from_pg_to_vertica(column):
    type = column["DATA_TYPE"]
    if column["DATA_TYPE"] in ("_text", "text", "jsonb", "json"):
        type = "long varchar(65000)"
    elif column["DATA_TYPE"] in ("int2", "int4", "int8"):
        type = "bigint"
    elif column["DATA_TYPE"] in ("float4", "float8"):
        type = "double precision"
    elif column["DATA_TYPE"] in ("numeric"):
        type = "numeric precision"

    if column["COLUMN_DEFAULT"] is not None and column["COLUMN_DEFAULT"] != "":
        type += " default {COLUMN_DEFAULT}".format(
            COLUMN_DEFAULT=column["COLUMN_DEFAULT"]
        )
    return type


def generate_sort_part_vertica(sort_part, date_field="date"):
    part = (
        "PARTITION BY EXTRACT(year FROM {date_field}) * 10000 + EXTRACT(MONTH FROM {date_field}) * 100 + EXTRACT("
        "day FROM {date_field})".format(date_field=date_field)
    )
    sort_field = sort_part[0]["SORTING_KEY"]
    if sort_field != "":
        sort = "ORDER BY {sort_field}".format(sort_field=sort_field)
    else:
        sort = ""
    return sort + " " + part


def get_type_sql_alchemy(type):
    try:
        return str(type.nested_type.__visit_name__).lower()
    except BaseException:
        return str(type.__visit_name__).lower()


def get_length_type_sql_alchemy(type):
    try:
        return type.length
    except BaseException:
        None


def get_default_arg_sql_alchemy(column):
    if column.default is not None:
        return column.default.arg
    elif column.server_default is not None:
        return str(column.server_default.arg)


def get_table_schema(table_name, meta):
    columns_name = [
        "COLUMN_NAME",
        "DATA_TYPE",
        "CHARACTER_MAXIMUM_LENGTH",
        "COLUMN_DEFAULT",
    ]
    table_sql = Table(table_name, meta)
    columns = [c.name for c in table_sql.columns]
    types = [get_type_sql_alchemy(c.type) for c in table_sql.columns]
    length = [get_length_type_sql_alchemy(c.type) for c in table_sql.columns]
    default = [get_default_arg_sql_alchemy(c) for c in table_sql.columns]
    fields = list(zip(columns, types, length, default))
    fields = [dict(zip(columns_name, f)) for f in fields]
    return fields


class FieldsConverter:
    def __init__(self, sql_credentials, from_db, to_db):
        self.from_db = from_db
        self.to_db = to_db
        self.sql_credentials = sql_credentials
        if self.to_db == "vertica":
            self.quote_char = '"'
        elif self.to_db == "exasol":
            self.quote_char = '"'
        else:
            self.quote_char = "`"

        cred_from = self.sql_credentials[self.from_db]
        uri_sql_alchemy_from = "{0}://{1}:{2}@{3}:{4}/{5}".format(
            cred_from["dialect"],
            cred_from["user"],
            cred_from["password"],
            cred_from["host"],
            cred_from["port"],
            cred_from["database"],
        )

        cred_to = self.sql_credentials[self.to_db]
        uri_sql_alchemy_to = "{0}://{1}:{2}@{3}:{4}/{5}".format(
            cred_to["dialect"],
            cred_to["user"],
            cred_to["password"],
            cred_to["host"],
            cred_to["port"],
            cred_to["database"],
        )

        engine_from = create_engine(uri_sql_alchemy_from)
        self.conn_from = engine_from.connect()
        engine_to = create_engine(uri_sql_alchemy_to)
        self.conn_to = engine_to.connect()

        if "schema" in cred_from:
            self.schema_from = cred_from["schema"]
            self.meta_from = MetaData(
                bind=engine_from, reflect=True, schema=self.schema_from
            )
        else:
            self.meta_from = MetaData(bind=engine_from, reflect=True)
        if "schema" in cred_to:
            self.schema_to = cred_to["schema"]
            self.meta_to = MetaData(bind=engine_to, reflect=True, schema=self.schema_to)
        else:
            self.meta_to = MetaData(bind=engine_to, reflect=True)

    def __del__(self):
        self.conn_from.close()
        self.conn_to.close()

    def generate_create(self, fields, table_name, sort_part=None):
        add_part = ""
        if self.to_db == "vertica":
            cur_schema = self.schema_to
            if "date" in [f.lower() for f in fields.keys()]:
                date_field = "date"
            else:
                date_field = ""
            if sort_part is not None:
                add_part = generate_sort_part_vertica(sort_part, date_field=date_field)
                if (
                    date_field != ""
                    and fields[date_field].lower().find("not null") == -1
                ):
                    fields[date_field] += " not null"
        elif self.to_db == "exasol":
            cur_schema = self.exasol_schema
        txt = "CREATE TABLE IF NOT EXISTS {schema}.{table} (".format(
            schema=cur_schema, table=table_name
        )

        txt += ",".join(
            [
                field + " " + str(fields[field])
                for field in fields
                if field != "password"
            ]
        )
        txt += ")"
        return txt + " " + add_part

    def get_partition_and_sort_keys_ch(self, table_name):
        columns = ["PARTITION_KEY", "SORTING_KEY", "ENGINE"]
        sql = """SELECT partition_key, 
                        sorting_key,
                        engine
                        FROM system.tables
                        WHERE name = '{table_name}'
                              AND database = '{database}'
              """.format(
            table_name=table_name, database=self.ch_database
        )
        print(sql)
        rows = self.ch_client.execute(sql)
        if rows[0][2] == "MaterializedView":
            return self.get_partition_and_sort_keys_ch(".inner." + table_name)
        else:
            return [dict(zip(columns, r)) for r in rows]

    def get_columns(self, table_name, db="mysql", type=None):
        if db == "mysql":
            fields = self.get_table_scheme_mysql(table_name)
        elif db == "vertica":
            fields = self.get_table_scheme_vertica(table_name)
        elif db == "ch":
            if type == "engine":
                fields = self.get_table_scheme_ch(table_name + "_data")
            else:
                fields = self.get_table_scheme_ch(table_name)
        elif db == "exasol":
            fields = self.get_table_scheme_exasol(table_name)
        columns = [
            f["COLUMN_NAME"]
            for f in fields
            if f["COLUMN_NAME"] not in ("password", "from")
        ]
        types = [
            f["DATA_TYPE"]
            for f in fields
            if f["COLUMN_NAME"] not in ("password", "from")
        ]
        return dict(zip(columns, types))

    def create_ddl(self, table_name):
        sort_part = None
        fields = get_table_schema(table_name, self.meta_from)
        fields_new = {}
        for f in fields:
            if self.from_db == "mysql" and self.to_db == "vertica":
                fields_new[f["COLUMN_NAME"]] = update_column_type_from_mysql_to_vertica(
                    f
                )
            elif self.from_db == "ch" and self.to_db == "vertica":
                fields_new[f["COLUMN_NAME"]] = update_column_type_from_ch_to_vertica(f)

            elif self.from_db == "mysql" and self.to_db == "exasol":
                fields_new[f["COLUMN_NAME"]] = update_column_type_from_mysql_to_exasol(
                    f
                )
            elif self.from_db == "pg" and self.to_db == "vertica":
                fields_new[f["COLUMN_NAME"]] = update_column_type_from_pg_to_vertica(f)
        return self.generate_create(
            fields_new, table_name.replace("_data", ""), sort_part
        )

    def drop_list_of_tables(self, tables):
        for table in tables:
            sql = "drop table {schema}.{table} cascade ".format(
                schema=self.schema_to, table=table
            )
            self.conn_to.execute(sql)

    def create_list_of_tables(self, tables, dir=None):
        for table in tables:
            sql = self.create_ddl(table_name=table)
            # self.conn_to.execute(sql)
            if dir is not None:
                f = open(
                    dir
                    + "/"
                    + self.schema_to
                    + "_"
                    + table.replace("_date", "")
                    + ".sql",
                    "w",
                )
                f.write(sql)
                f.close()
