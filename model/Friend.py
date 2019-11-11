from model.BaseEntity import BaseEntity


class Friend(BaseEntity):
    table = "friend"

    def __init__(self, data):
        self.aid1 = data['aid1']
        self.aid2 = data['aid2']