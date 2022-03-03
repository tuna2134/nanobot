from sanic import Sanic
from sanic.response import text, html, redirect, json
from aiohttp import ClientSession
from jinja2 import Environment, FileSystemLoader
from lib.bot import Bot
from lib.oauth2 import require
from os import getenv

app = Sanic("app")
token = getenv("token")
publickey = getenv("publickey")
env = Environment(
    loader=FileSystemLoader("./templates"),
    enable_async=True
)
ApiUrl = "https://discord.com/api/v9"

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

# main

@app.route("/")
async def main(request):
    return await template("base.html")

# dashboard

@app.get("/login")
async def login(request):
    return redirect("https://discord.com/api/oauth2/authorize?client_id=829578365634740225&redirect_uri=https%3A%2F%2Fnano.hortbot.cf%2Fcallback&response_type=code&scope=identify%20guilds")

@app.get("/callback")
async def callback(request):
    code = request.args.get("code")
    payload = {
        "code": code,
        "client_id": "829578365634740225",
        "client_secret": getenv("clientsecret"),
        "grant_type": "authorization_code",
        "redirect_uri": "https://nano.hortbot.cf/callback"
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    async with ClientSession() as session:
        async with session.post(ApiUrl + "/oauth2/token", data=payload, headers=headers) as r:
            data = await r.json()
    res = redirect("/dashboard")
    res.cookies["token"] = data["access_token"]
    return res

@app.get("/dashboard")
@require()
async def dashboard(request, user):
    return await template("dashboard/index.html")

@app.get("/dashboard/<guild>")
@require()
async def dashboard_guild(request, user, guild):
    return await template("dashboard/guild.html", guildid=guild)

@app.get("/dashboard/<guild>/setting")
@require()
async def dashboard_setting(request, user, guild):
    return await template("dashboard/setting.html", guildid=guild)

# api

@app.get("/api/user")
@require()
async def api(request, user):
    return json(user)

@app.get("/api/guilds")
async def guilds(request):
    token = request.cookies.get("token")
    async with ClientSession() as session:
        headers = {
            "Authorization": "Bearer {}".format(token)
        }
        async with session.get(ApiUrl + "/users/@me/guilds", headers=headers) as r:
            return json(await r.json())

# slashcommand

@bot.slash_command("ping", "ping command")
async def ping(interaction):
    return interaction.send("pong!")

@ping.after
async def pingsdd():
    print("after")

@bot.slash_command("naup", "表示順をアップします")
async def naup(interaction):
    return interaction.send("作成中")

@bot.slash_command("invite", "show invite url")
async def invite(interaction):
    return interaction.send("https://discord.com/api/oauth2/authorize?client_id=829578365634740225&permissions=1&scope=bot%20applications.commands")

app.run(
    host="0.0.0.0",
    port=8080
)