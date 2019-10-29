import model.BaseEntity


class InRace(model.BaseEntity):
    table = "inrace"

    def __init__(self, data):
        self.aid1 = data['aid1']
        self.aid2 = data['aid2']
        self.rid = data['rid']