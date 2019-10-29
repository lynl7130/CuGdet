import model.BaseEntity


class Stocks(model.BaseEntity):
    def __init__(self, data):
        self.sid = data['sid']
        self.name = data['name']
        self.type = data['type']
        self.info = data['info']