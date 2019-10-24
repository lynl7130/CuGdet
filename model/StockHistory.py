class StockHistory:
    def __init__(self, data):
        self.spid = data['spid']
        self.time = data['time']
        self.price = data['price']
        self.sid = data['sid']