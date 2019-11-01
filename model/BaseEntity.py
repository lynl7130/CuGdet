class BaseEntity(object):
    table = "base"
    @classmethod
    def select(cls, conn, condition):
        # cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cur = conn.cursor()
        sql = """SELECT * FROM %s WHERE %s;""" % (cls.table, condition)
        cur.execute(sql)
        conn.commit()

    @classmethod
    def insert(cls, conn, value):
        cur = conn.cursor()
        sql = """INSERT INTO  VALUE();"""
        cur.execute(sql)
        conn.commit()

    @classmethod
    def delete(cls, conn, condition):
        cur = conn.cursor()
        sql = """DELETE * FROM %s WHERE %s;""" % (cls.table, condition)
        cur.execute(sql)
        conn.commit()

    @classmethod
    def tmp(cls):
        print(cls.table)
