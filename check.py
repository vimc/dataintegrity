#!/usr/bin/env python3
import psycopg2
import psycopg2.extras
import utils
from os import chdir
from os.path import abspath, dirname
import settings


database_settings = settings.load_settings()


select_primary_key_query = """SELECT Col.Column_Name from 
    INFORMATION_SCHEMA.TABLE_CONSTRAINTS Tab, 
    INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE Col 
WHERE 
    Col.Constraint_Name = Tab.Constraint_Name
    AND Col.Table_Name = Tab.Table_Name
    AND Constraint_Type = 'PRIMARY KEY'
    AND Col.Table_Name = '{table_name}'"""


def connect(dbname):
    conn_settings = {
        "host": database_settings["host"],
        "port": database_settings["port"],
        "name": dbname,
        "user": database_settings["user"],
        "password": database_settings["password"]
    }
    conn_string_template = "dbname='{name}' user='{user}' password='{password}' host='{host}' port={port}"
    conn_string = conn_string_template.format(**conn_settings)
    return psycopg2.connect(conn_string)


def get_table(table_name, db_name):
    rows = None
    with connect(db_name) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(select_primary_key_query.format(table_name=table_name))
            primary_key = cur.fetchall()[0][0]

            cur.execute("""SELECT * from {table_name} ORDER BY {primary_key} ASC""".format(table_name=table_name,
                                                                                           primary_key=primary_key))
            rows = cur.fetchall()

    rows = {r[primary_key]: r for r in rows}
    return rows


def check_table(table_name):
    original_rows = get_table(table_name, database_settings["original_db_name"])
    new_rows = get_table(table_name, database_settings["new_db_name"])
    for k in original_rows.keys():
        if not original_rows[k] == new_rows[k]:
            # only do this more expensive equality check if the first one fails
            if not utils.ARRAYEQUAL(original_rows[k], new_rows[k]):
                print("Change in row {rowid}: was {old}, now {new}".format(rowid=k, old=original_rows[k], new=new_rows[k]))


def get_tables():
    tables = None
    with connect(database_settings["original_db_name"]) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE'""")
            tables = cur.fetchall()
        cur.close()
    return tables


def check():
    tables = get_tables()
    for table in tables:
        table_name = table[0]
        print("Checking table: {table_name}".format(table_name=table_name))
        check_table(table_name)


if __name__ == "__main__":
    abspath = abspath(__file__)
    chdir(dirname(abspath))
    check()
