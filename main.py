from sanic import Sanic
from sanic.response import text, html
from jinja2 import Environment, FileSystemLoader
from lib.bot import Bot
from os import getenv

app = Sanic("app")
token = getenv("token")
publickey = getenv("publickey")
env = Environment(
    loader=FileSystemLoader("./templates"),
    enable_async=True
)

async def template(filename, *args, **kwargs):
    content = await env.get_template(filename).render_async(kwargs)
    return html(content)

bot = Bot(token, publickey)

@app.before_server_start
async def start(app, loop):
    await bot.start(loop)

@app.post("/interaction")
async def interaction(request):
    return await bot.interaction(request)

@app.route("/")
async def main(request):
    return await template("base.html")

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