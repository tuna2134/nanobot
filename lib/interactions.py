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

    def send(self, content=None, *,
             tts=None, embeds: list=None,
             ephemeral: bool=False):
        payload = {
            "type": 4,
            "data": {}
        }
        if content is not None:
            payload["data"]["content"] = content
        if tts is not None:
            payload["data"]["tts"] = True
        if embeds is not None:
            payload["data"]["embeds"] = [embed.payload for embed in embeds]
        if ephemeral is True:
            payload["flags"] = 1 << 6
        return json(payload)

class InteractionCommand:
    def __init__(self, data):
        self._data = data

    @property
    def name(self):
        return self._data["name"]