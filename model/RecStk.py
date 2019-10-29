import model.BaseEntity


class RecStk(model.BaseEntity):
    def __init__(self, data):
        self.aid = data['aid']
        self.sid = data['sid']