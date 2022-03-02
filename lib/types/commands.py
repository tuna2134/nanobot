class Command:
    def __init__(self, coro, name, description):
        self.name = name
        self.description = description
        self.callback = coro

    def to_dict(self):
        payload = {
            "name": self.name,
            "description": self.description,
            "type": 1
        }
        return payload