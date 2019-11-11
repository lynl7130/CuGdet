from model.BaseEntity import BaseEntity


class WinHonor(BaseEntity):
    table = "win_honor"
    
    def __init__(self, data):
        self.aid = data['aid']
        self.hid = data['hid']