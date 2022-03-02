from sanic import Sanic
from sanic.response import text
from lib.bot import Bot
from os import getenv

app = Sanic("app")
token = getenv("token")
publickey = getenv("publickey")
bot = Bot(token, publickey)

@app.before_server_start
async def start(app, loop):
    await bot.start(loop)

@app.post("/interaction")
async def interaction(request):
    return await bot.interaction(request)

@app.route("/")
async def main(request):
    return text("test")

@bot.slash_command("ping", "ping command")
async def ping(interaction):
    return interaction.send("pong!")

@bot.slash_command("invite", "show invite url")
async def invite(interaction):
    return interaction.send("https://discord.com/api/oauth2/authorize?client_id=829578365634740225&permissions=1&scope=bot%20applications.commands")

app.run(
    host="0.0.0.0",
    port=8080
)