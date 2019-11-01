from model.BaseEntity import BaseEntity


class StockHistory(BaseEntity):
    table = "stock_history"

    def __init__(self, data):
        self.spid = data['spid']
        self.time = data['time']
        self.price = data['price']
        self.sid = data['sid']