import lib

class Bot(lib.Cog):
    def __init__(self, bot):
        self.bot = bot

    @lib.slash_command("ping", "主にサーバーが動いているかをチェックするコマンドです。")
    async def ping(self, interaction):
        return interaction.send(embeds=[
            lib.Embed(title="Pong")
        ], ephemeral=True)

    @lib.slash_command("invite", "botを導入するためのリンクを表示します")
    async def invite(self, interaction):
        return interaction.send("https://discord.com/api/oauth2/authorize?client_id=829578365634740225&permissions=1&scope=bot%20applications.commands")


def setup(bot):
    bot.add_cog(Bot(bot))