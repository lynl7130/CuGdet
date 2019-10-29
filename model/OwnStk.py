import model.BaseEntity


class OwnStk(model.BaseEntity):
    def __init__(self, data):
        self.aid = data['aid']
        self.sid = data['sid']
        self.price = data['price']
        self.num = data['num']