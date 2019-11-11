from model.BaseEntity import BaseEntity


class RecStk(BaseEntity):
    table = "rec_stk"

    def __init__(self, data):
        self.aid = data['aid']
        self.sid = data['sid']