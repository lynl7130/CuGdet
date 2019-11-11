from psycopg2.extras import RealDictCursor

def condition_to_sql(condition):
    res = []
    for t in condition:
        for k in condition[t]:
            res.append("""%s.%s = '%s'""" % (t, k, condition[t][k]))
    res = " AND ".join(res)
    return res


def tables_to_sql(tables):
    res = []
    i = 1
    for join_type in tables:
        tmp = []
        for table in tables[join_type]:
            tmp.append("%s as T%s" % (table, str(i)))
            i += 1
        tmp_s = " %s " % join_type
        res.append(tmp_s.join(tmp))
    res = ", ".join(res)
    return res


def columns_to_sql(columns):
    tmp = []
    if columns == "*":
        return "*"
    for t in columns:
        for col in columns[t]:
            tmp.append("%s.%s" % (t, col))
    res = ", ".join(tmp)
    return res


def values_to_sql(values):
    vals = []
    for t in values:
        if t == "=":
            for k in values[t]:
                vals.append("%s = '%s'" % (k, values[t][k]))
        else:
            for k in values[t]:
                vals.append("%s = %s %s '%s'" % (k, k, t, values[t][k]))
    return ", ".join(vals)

def valid_honor(conn, aid):
    formed_aid = "'%s'" % (aid)
    sql = '''
    DELETE FROM win_honor WHERE aid=''' + formed_aid + ''';
    INSERT INTO win_honor (aid, hid)
    SELECT records.aid, honors.hid
    FROM records, honors 
    WHERE records.aid= ''' + formed_aid + \
    ''' AND (honors.starting IS NULL OR records.time >= honors.starting)
        AND (honors.ending IS NULL OR records.time <= honors.ending)
        AND (honors.tag IS NULL OR records.tag = honors.tag)
    GROUP BY honors.hid
    HAVING CASE WHEN honors.type = 'beq' THEN SUM(records.amt) >= honors.amt ELSE SUM(records.amt) <= honors.amt END; 
    '''
    print(sql)
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(sql)
        conn.commit()
    except:
        conn.rollback()