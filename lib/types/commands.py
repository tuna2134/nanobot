from sanic.response import json
from inspect import signature
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

    def _change_parameter(self):
        rdata = []
        for p in signature(self.callback).parameters.values():
            if p.name in ["self", "interaction"]:
                continue
            if p.default != p.empty:
                data = p.default.payload
            else:
                data = CommandOption(p.name, "...").payload
            if p.annotation == p.empty:
                data["type"] = 3
            data["name"] = p.name
            rdata.append(data)
        return rdata

    def to_dict(self):
        payload = {
            "name": self.name,
            "description": self.description,
            "options": self._change_parameter(),
            "type": 1
        }
        return payload

    @property
    def _options(self):
        data = {}
        for p in signature(self.callback).parameters.values():
            data[p.name] = p.default.payload["required"]
        return data

class CommandOption:
    def __init__(self, description: str, required: bool=True):
        self.payload = {}
        self.payload["description"] = description
        self.payload["required"] = required

    def __call__(self, *args, **kwargs):
        return None