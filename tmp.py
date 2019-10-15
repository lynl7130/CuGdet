import os
import db
import pandas as pd


def get_file(path):
    dirs = os.listdir(path)
    for dir in dirs:
        if dir[0] != ".":
            files = os.listdir(os.path.join(path, dir))
            for file in files:
                if file[0] != ".":
                    yield os.path.join(os.path.join(path, dir), file)


def import_stock(cur):
    print("---------------importing stock---------------")
    names = pd.read_csv("./stock-data/symbol-name.csv")
    for i, row in names.iterrows():
        symbol = row['Symbol']
        name = row['Name']

        sql = """INSERT INTO stocks(sid, name) VALUES ('%s', '%s')""" % (symbol, name)
        cur.excute(sql)
        cur.commit()

def import_stock_history(cur):
    print("---------------importing stock history price---------------")
    for f in get_file("./stock-data/Data/"):
        symbol = f.strip().split("/")[-1].split(".")[0]
        data = pd.read_csv(f)

        spid = 0
        for index, row in data.iterrows():
            sql = """INSERT INTO stocks_history(spid, time, price, sid) VALUES ('%s', '%s', %s, '%s')""" % (symbol + str(spid), row['Date'], row['Close'], symbol)
            cur.execute(sql)
            cur.commit()
            spid += 1


def get_symbol_list():
    symbols = []
    for f in get_file("./stock-data/Data/"):
        symbols.append(f.split("/")[-1].split(".")[0])
    return symbols


def check_name():
    symbols = set(get_symbol_list())
    data = pd.read_csv("./stock-data/companylist.csv")
    valid_symbols = set([s.lower() for s in data["Symbol"].tolist()])
    return symbols.intersection(valid_symbols), data


def make_symbol_name_mapping():
    symbols, data = check_name()
    res = {'Symbol': [], 'Name': []}
    for symbol in symbols:
        name = data[data['Symbol'] == symbol.upper()]['Name'].values[0]
        print(name)
        res['Symbol'].append(symbol)
        res['Name'].append(name)
    res = pd.DataFrame(res)
    res.to_csv("./stock-data/symbol-name.csv", index = False)


def import_stock_data():
    conn = db.connect(name = "", usr = "", host = "", pwd = "")
    if conn is None:
        exit(1)
    else:
        cur = conn.cursor()
        import_stock(cur)

        import_stock_history(cur)


if __name__ == '__main__':
    import_stock_data()

