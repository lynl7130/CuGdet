from model.BaseEntity import BaseEntity


class Account(BaseEntity):
    table = "account"

    def __init__(self):
        self.aid = None

    def __init__(self, data):
        self.aid = data['aid']
        self.name = data['name']
        self.email = data['email']
        self.pwd = data['pwd']

