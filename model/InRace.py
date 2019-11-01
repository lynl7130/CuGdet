from model.BaseEntity import BaseEntity


class InRace(BaseEntity):
    table = "in_race"

    def __init__(self, data):
        self.aid1 = data['aid1']
        self.aid2 = data['aid2']
        self.rid = data['rid']