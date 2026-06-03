import os
import discord
from discord.ext import commands
from groq import Groq
from flask import Flask
import threading
import random

# -----------------------------
# KEEP-ALIVE WEB SERVER (Render)
# -----------------------------
app = Flask('')

@app.route('/')
def home():
    return "ZwerBo ist wach und voller Magie!"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = threading.Thread(target=run)
    t.start()

# -----------------------------
# DISCORD BOT SETUP
# -----------------------------
TOKEN = os.getenv("TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

client = commands.Bot(command_prefix="!", intents=intents)

groq_client = Groq(api_key=GROQ_API_KEY)

# -----------------------------
# AI-FUNKTION (Deutsch + ZwerBo-Stil)
# -----------------------------
def ask_groq(prompt):
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Du bist ZwerBo, ein kleiner magischer Kobold-Bot. "
                        "Du antwortest IMMER auf Deutsch, niemals auf Englisch. "
                        "Dein Stil ist warm, verspielt, freundlich und leicht mystisch. "
                        "Du redest wie ein kleiner Waldgeist, der neugierig und hilfsbereit ist. "
                        "Halte deine Antworten kurz, klar und mit einem Hauch Magie."
                    )
                },
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Fehler bei Groq: {e}"

# -----------------------------
# TRIGGER-WÖRTER
# -----------------------------
TRIGGER_WORDS = ["hallo", "hi", "hey", "zwerbo"]

MORNING = ["guten morgen", "morgen", "moin"]
DAY = ["guten tag"]
EVENING = ["guten abend", "abend"]

AUTO_EMOJIS = ["✨", "😊", "🌙", "🔥", "🍃"]

# -----------------------------
# REAKTIONEN
# -----------------------------
@client.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return

    if reaction.message.author == client.user:
        await reaction.message.channel.send("Oh! Danke für das kleine Funkeln ✨")

# -----------------------------
# NACHRICHTEN-EVENT
# -----------------------------
@client.event
async def on_message(message):
    if message.author.bot:
        return

    msg = message.content.lower()

    # Auto-Emoji (einmal pro Nachricht)
    if random.random() < 0.25:
        try:
            await message.add_reaction(random.choice(AUTO_EMOJIS))
        except:
            pass

    # Tageszeiten
    if any(word in msg for word in MORNING):
        await message.channel.send("Einen zauberhaften guten Morgen! ✨🌅")
        return

    if any(word in msg for word in DAY):
        await message.channel.send("Einen wundervollen guten Tag wünsche ich dir! ☀️")
        return

    if any(word in msg for word in EVENING):
        await message.channel.send("Einen gemütlichen guten Abend wünsche ich dir! 🌙✨")
        return

    # Trigger
    if any(trigger in msg for trigger in TRIGGER_WORDS):
        await message.channel.send("Huhu! ✨ Ich bin da – was brauchst du?")
        return

    # AI ohne Prefix (!ai)
    if not msg.startswith("!"):
        if len(msg) > 2:  # verhindert Spam durch einzelne Buchstaben
            answer = ask_groq(msg)
            await message.channel.send(answer)
            return

    await client.process_commands(message)

# -----------------------------
# BEFEHLE
# -----------------------------
@client.command()
async def ping(ctx):
    await ctx.send("Pong! 🏓")

@client.command()
async def ai(ctx, *, prompt: str):
    answer = ask_groq(prompt)
    await ctx.send(answer)

# -----------------------------
# START
# -----------------------------
keep_alive()
client.run(TOKEN)
