from psycopg2.extras import RealDictCursor


class BaseEntity(object):
    table = "base"
    @classmethod
    def select(cls, conn, condition):
        cur = conn.cursor(cursor_factory = RealDictCursor)
        sql = """SELECT * FROM %s WHERE %s;""" % (cls.table, condition)
        cur.execute(sql)
        res = cur.fetchall()
        return res


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
    def update(cls):
        print(cls.table)
