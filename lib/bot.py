from .interactions import Interaction
from .types.commands import Command
from sanic.response import json, text
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
from aiohttp import ClientSession
from os import getenv
import asyncio

class ApiError(Exception):
    pass

class Bot:
    ApiUrl = "https://discord.com/api/v9"
    def __init__(self, token, publickey):
        self.token = token
        self.publickey = publickey
        self.commands = []

    async def request(self, method, path, *args, **kwargs):
        headers = {
            "Authorization": "Bot {}".format(self.token)
        }
        kwargs["headers"] = headers
        for i in range(5):
            async with ClientSession(loop=self.loop) as session:
                async with session.request(method, self.ApiUrl + path, *args, **kwargs) as r:
                    if r.status == 404:
                        raise ApiError("404 error")
                    elif r.status == 200:
                        return await r.json()
                    elif r.status == 500:
                        raise ApiError("500 error")

    async def process_slash_command(self, name, interaction, *args, **kwargs):
        for command in self.commands:
            if command.name == name:
                interaction.request.conn_info.ctx._wait_response = asyncio.Event()
                asyncio.create_task(self._wait_response(interaction, command))
                return await command.callback(interaction, *args, **kwargs)

    async def _wait_response(self, interaction, command):
        await interaction.request.conn_info.ctx._wait_response.wait()
        command.dispatch()

    def slash_command(self, name, description):
        def decorator(coro):
            cmd = Command(coro, name, description)
            self.commands.append(cmd)
            return cmd
        return decorator

    async def on_interaction(self, interaction):
        if interaction.type == 2:
            return await self.process_slash_command(interaction.command.name, interaction)

    async def start(self, loop):
        self.loop = loop
        datas = await self.request("GET", "/applications/829578365634740225/commands")
        need = []
        for command in self.commands:
            if len(datas) == 0:
                need.append(command)
                continue
            for data in datas:
                if data["name"] == command.name:
                    if data["description"] == command.description:
                        break
                    else:
                        need.append(command)
                        break
            else:
                need.append(command)
        for cmd in need:
            await self.request("POST", "/applications/829578365634740225/commands", json=cmd.to_dict())

    async def interaction(self, request):
        verify_key = VerifyKey(bytes.fromhex(self.publickey))
        signature = request.headers.get("x-signature-ed25519")
        timestamp = request.headers.get("x-signature-timestamp")
        try:
            verify_key.verify(f'{timestamp}{request.body.decode()}'.encode(), bytes.fromhex(signature))
        except BadSignatureError:
            return text("invalid request signature", status=401)
        else:
            data = request.json
            if data["type"] == 1:
                return json({"type": 1})
            else:
                interaction = Interaction(data)
                interaction.request = request
                return await self.on_interaction(interaction)