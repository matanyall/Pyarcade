class ActiveUser(object):
    active = False
    name = ""
    user_id = 0

    def __init__(self):
        self.active = False
        self.name = ""
        self.user_id = 0

    def get_name(self):
        return self.name

    def get_id(self):
        return self.user_id

    def set_user(self, name: str):
        self.name = name
        self.active = True

    def logout(self):
        self.active = False
        self.name = ""
        self.user_id = 0

    def set_id(self, user_id: int):
        self.user_id = user_id





