import model.BaseEntity


class Logs(model.BaseEntity):

    def __init__(self, data):
        self.lid = data['lid']
        self.if_log_in = data['if_log_in']
        self.time = data['time']
        self.location = data['location']
        self.aid = data['aid']