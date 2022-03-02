from sanic.response import json

class Interaction:
    def __init__(self, data):
        self.__data = data

    @property
    def command(self):
        return InteractionCommand(self.__data["data"])

    @property
    def type(self):
        return self.__data["type"]

    def send(self, content):
        payload = {
            "type": 4,
            "data": {}
        }
        if content is not None:
            payload["data"]["content"] = content
        return json(payload)

class InteractionCommand:
    def __init__(self, data):
        self._data = data

    @property
    def name(self):
        return self._data["name"]