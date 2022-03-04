import lib
from sanic.response import text

class test(lib.Cog):
    def __init__(self, bot):
        self.bot = bot

    @lib.slash_command("naup", "表示順をアップします")
    async def naup(self, interaction):
        return interaction.send("test")

    @naup.after
    async def naup_after(self, interaction):
        message = await interaction.fetch_message()
        await message.edit("現在作成中")

def setup(bot):
    bot.add_cog(test(bot))