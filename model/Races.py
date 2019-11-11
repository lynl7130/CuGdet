from model.BaseEntity import BaseEntity


class Races(BaseEntity):
    table = "races"

    def __init__(self, data):
        self.rid = data['rid']
        self.name = data['name']
        self.type = data['type']
        self.starting = data['starting']
        self.ending = data['ending']
        self.tag = data['tag']