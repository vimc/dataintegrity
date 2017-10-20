#!/usr/bin/env python3
import psycopg2
import psycopg2.extras
from os import chdir
from os.path import abspath, dirname


def check():
    tables = get_tables()

    for tablename in tables:
        print("Checking table: {table}".format(table=tablename[0]))
        check_table(tablename[0])


def connect(dbname):
    conn_settings = {
        "host": "localhost",
        "port": 5432,
        "name": dbname,
        "user": "vimc",
        "password": "changeme"
    }
    conn_string_template = "host='{host}' port='{port}' dbname='{name}' user='{user}' password='{password}'"
    conn_string = conn_string_template.format(**conn_settings)
    return psycopg2.connect(conn_string)


def get_tables():
    tables = None
    with connect("montaguold") as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE'""")
            tables = cur.fetchall()
        cur.close()
    return tables


select_primary_key = """SELECT Col.Column_Name from 
    INFORMATION_SCHEMA.TABLE_CONSTRAINTS Tab, 
    INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE Col 
WHERE 
    Col.Constraint_Name = Tab.Constraint_Name
    AND Col.Table_Name = Tab.Table_Name
    AND Constraint_Type = 'PRIMARY KEY'
    AND Col.Table_Name = '{tablename}'"""


def get_table(tablename, dbname):
    rows, columns, primary_key = None, None, None
    with connect(dbname) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(select_primary_key.format(tablename=tablename))
            primary_key = cur.fetchall()[0][0]

            cur.execute("""SELECT * from {tablename} ORDER BY {primary_key} ASC""".format(tablename=tablename,
                                                                                          primary_key=primary_key))
            rows = cur.fetchall()

            cur.execute(
                """SELECT COLUMN_NAME FROM information_schema.columns WHERE table_schema = 'public' AND table_name = '{tablename}'"""
                .format(tablename=tablename))
            columns = cur.fetchall()

    rows = {r[primary_key]: r for r in rows}
    return [rows, columns]


def check_table(tableName):
    old = get_table(tableName, "montaguold")
    new = get_table(tableName, "montagunew")
    oldrows = old[0]
    newrows = new[0]
    for k in oldrows.keys():
        if not oldrows[k] == newrows[k]:
            print("Change in row {rowid}, was {old}, now {new}".format(rowid=k, old=oldrows[k], new=newrows[k]))



if __name__ == "__main__":
    abspath = abspath(__file__)
    chdir(dirname(abspath))
    check()
