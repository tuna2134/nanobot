from sanic.response import json
import asyncio

class Command:
    def __init__(self, coro, name, description):
        self.name = name
        self.description = description
        self.callback = coro
        self._after = []

    async def __call__(self, *args, **kwargs):
        return await self.callback(*args, **kwargs)

    def dispatch(self, *args, **kwargs):
        for f in self._after:
            if hasattr(self, "cog"):
                asyncio.create_task(f(self.cog, *args, **kwargs))
            else:
                asyncio.create_task(f(*args, **kwargs))

    def after(self, coro):
        self._after.append(coro)
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