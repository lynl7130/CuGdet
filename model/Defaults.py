import model.BaseEntity


class Defaults(model.BaseEntity):
    def __init__(self, data):
        self.did = data['did']
        self.name = data['name']
        self.be_from = data['be_from']
        self.be_to = data['be_to']
        self.amt = data['amt']
        self.starting = data['starting']
        self.ending = data['ending']
        self.cycle = data['cycle']
        self.remark = data['remark']
        self.aid = data['aid']
        self.tag = data['tag']