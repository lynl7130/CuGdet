class Records:
    def __init__(self, data):
        self.reid = data['reid']
        self.name = data['name']
        self.be_from = data['be_from']
        self.be_to = data['be_to']
        self.amt = data['amt']
        self.tag = data['tag']
        self.time = data['time']
        self.remark = data['remark']
        self.aid = data['aid']