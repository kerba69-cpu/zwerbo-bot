import os
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

# -----------------------------
# KEEP-ALIVE WEB SERVER (für Render)
# -----------------------------
app = Flask('')

@app.route('/')
def home():
    return "ZwerBo läuft!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# -----------------------------
# DISCORD BOT
# -----------------------------
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"ZwerBo ist online als {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

# -----------------------------
# START
# -----------------------------
keep_alive()  # wichtig für Render Free Web Service
TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)
