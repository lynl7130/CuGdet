import model.BaseEntity


class Account(model.BaseEntity):
    table = "account"

    def __init__(self, data):
        self.aid = data['aid']
        self.name = data['name']
        self.email = data['email']
        self.pwd = data['pwd']

