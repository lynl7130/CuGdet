import model.BaseEntity


class Friend(model.BaseEntity):
    def __init__(self, data):
        self.aid1 = data['aid1']
        self.aid2 = data['aid2']