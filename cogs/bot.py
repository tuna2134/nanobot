import lib

class Bot(lib.Cog):
    test = lib.CommandGroup("test")
    def __init__(self, bot):
        self.bot = bot

    @test.slash_command("user", "ユーザーを表示します")
    async def user(self, interaction, user: lib.CommandOption("ユーザーを選択してね")):
        return interaction.send("aaaa")

    @lib.slash_command("help", "ヘルプコマンド")
    async def help(self, interaction):
        return interaction.send("https://hortbot-dev.github.io/nanobot.html")

    @lib.slash_command("ping", "主にサーバーが動いているかをチェックするコマンドです。")
    async def ping(self, interaction):
        return interaction.send(embeds=[
            lib.Embed(title="Pong")
        ], ephemeral=True)

    @lib.slash_command("invite", "botを導入するためのリンクを表示します")
    async def invite(self, interaction):
        return interaction.send("https://discord.com/api/oauth2/authorize?client_id=829578365634740225&permissions=1&scope=bot%20applications.commands")

    @lib.slash_command("support", "サポートサーバーを表示します。")
    async def support(self, interaction, user: lib.User = lib.CommandOption("ユーザーを選んでね")):
        return interaction.send("https://discord.gg/SGYGBTeNgW")

def setup(bot):
    bot.add_cog(Bot(bot))