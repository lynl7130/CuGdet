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
        cur.execute(sql)



def import_stock_history(cur):
    print("---------------importing stock history price---------------")
    valid_symbol = set(pd.read_csv("./stock-data/symbol-name.csv")['Symbol'].values)
    for f in get_file("./stock-data/Data/"):
        symbol = f.strip().split("/")[-1].split(".")[0]
        
        cnt = open(f, 'r').read()
        if len(cnt) == 0:
            continue
        else:
            data = pd.read_csv(f)
        
        if symbol in valid_symbol:
            spid = 0
            for index, row in data.iterrows():
                sql = """INSERT INTO stock_history(spid, time, price, sid) VALUES ('%s', '%s', %s, '%s')""" % (symbol + str(spid), row['Date'], row['Close'], symbol)
                cur.execute(sql)
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
    conn = db.connect(name = "proj1part2", usr = "yl4323", host = "35.243.220.243", pwd = "2262")
    if conn is None:
        exit(1)
    else:
        cur = conn.cursor()
        # import_stock(cur)
        # conn.commit()

        import_stock_history(cur)
        conn.commit()


def check_data():
    valid_symbols = set(pd.read_csv("./stock-data/symbol-name.csv")['Symbol'].values)
    for f in get_file("./stock-data/Data/"):
        symbol = f.strip().split("/")[-1].split(".")[0]
        if symbol in valid_symbols:
            cnt = open(f, 'r').read()
            if len(cnt) == 0:
                continue
            else:
                data = pd.read_csv(f)
            

if __name__ == '__main__':
    check_data()

