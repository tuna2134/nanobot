from inspect import getmembers
from .types.commands import Command

def slash_command(name, description):
    def decorator(coro):
        cmd = Command(coro, name, description)
        coro._slash_command = cmd
        return coro
    return decorator

class Cog:
    def _inject(self, bot):
        for name, func in getmembers(self):
            if hasattr(func, "_slash_command"):
                func._slash_command.cog = self
                bot.commands.append(func._slash_command)