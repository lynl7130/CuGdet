from model.BaseEntity import BaseEntity


class OwnStk(BaseEntity):
    table = "own_stk"

    def __init__(self, data):
        self.aid = data['aid']
        self.sid = data['sid']
        self.price = data['price']
        self.num = data['num']