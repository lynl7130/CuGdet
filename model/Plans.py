class Plans:
    def __init__(self, data):
        self.pid = data['pid']
        self.starting = data['starting']
        self.ending = data['ending']
        self.cycle = data['cycle']
        self.credit = data['credit']
        self.budget = data['budget']
        self.aid = data['aid']