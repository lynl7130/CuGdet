import psycopg2
from psycopg2.extras import RealDictCursor

from db.utils import condition_to_sql, tables_to_sql, columns_to_sql


def connect(name, usr, host, pwd):
    try:
        conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (name, usr, host, pwd))
        return conn
    except:
        print("fail to build connection")
        return None


def select(conn, tables, columns, condition, special = ""):
    cur = conn.cursor(cursor_factory = RealDictCursor)

    sql = """SELECT %s FROM %s WHERE %s %s;""" % (columns_to_sql(columns), tables_to_sql(tables), condition_to_sql(condition), special)
    cur.execute(sql)
    return cur.fetchall()


def insert(conn, table, data):
    cur = conn.cursor(cursor_factory = RealDictCursor)

    cols = ",".join(data.keys())
    cols = "(%s)" % cols
    vals = ", ".join(data.values())
    vals = "(%s)" % vals

    sql = "INSERT INTO %s %s VALUES %s;" % (table, cols, vals)
    try:
        cur.execute(sql)
        conn.commit()
        return True
    except:
        return False


def delete(conn, table, condition):
    cur = conn.cursor(cursor_factory = RealDictCursor)

    sql = "DELETE FROM %s WHERE %s;" % (tables_to_sql({"": [table]}), condition_to_sql({"T1": condition}))
    try:
        cur.execute(sql)
        conn.commit()
        return True
    except:
        return False


def update(conn, table, new_values, condition):
    cur = conn.cursor(cursor_factory = RealDictCursor)

    vals = []
    for k in new_values:
        vals += "T1.%s = '%s'" % (k, new_values[k])
    vals = ", ".join(vals)
    sql = "UPDATE %s SET %s WHERE %s;" % (tables_to_sql({"": [table]}), vals, condition_to_sql({"T1": condition}))
    try:
        cur.execute(sql)
        conn.commit()
        return True
    except:
        return False

