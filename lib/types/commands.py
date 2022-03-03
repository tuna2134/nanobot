from sanic.response import json

class Command:
    def __new__(cls, *args, **kwargs):
        self = super().__new__(cls)
        return self
        
    def __init__(self, coro, name, description):
        self.name = name
        self.description = description
        self.callback = coro
        self.after = []

    async def __call__(self, *args, **kwargs):
        return await self.callback(*args, **kwargs)

    def response_json(self, data, *args, **kwargs):
        pass

    def after(self, coro):
        self.after.append(coro)
        return coro

    def to_dict(self):
        payload = {
            "name": self.name,
            "description": self.description,
            "type": 1
        }
        return payload

class CommandOption:
    def __init__(self, name, description):
        self.name = name
        self.description = description