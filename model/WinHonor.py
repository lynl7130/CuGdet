import model.BaseEntity


class WinHonor(model.BaseEntity):
    def __init__(self, data):
        self.aid = data['aid']
        self.hid = data['hid']