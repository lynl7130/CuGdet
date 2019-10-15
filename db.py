import psycopg2


def connect(name, usr, host, pwd):
    conn = None
    try:
        conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (name, usr, host, pwd))
    except:
        print("fail to build connection")
    return conn
