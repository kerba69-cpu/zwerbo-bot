import os
import discord
from discord.ext import commands
from groq import Groq
from flask import Flask
import threading

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
# TRIGGER
# -----------------------------
TRIGGER_WORDS = [
    "hallo zwerbo", "hi zwerbo", "hey zwerbo",
    "zwerbo?", "zwerbo!", "zwerbo"
]

# -----------------------------
# EVENT: NACHRICHTEN
# -----------------------------
@client.event
async def on_message(message):
    if message.author.bot:
        return

    msg = message.content.lower()

    # Trigger
    if any(trigger in msg for trigger in TRIGGER_WORDS):
        await message.channel.send("Huhu! ✨ Ich bin da – was brauchst du?")
        return

    # AI
    if msg.startswith("!ai "):
        prompt = msg.replace("!ai ", "")
        answer = ask_groq(prompt)
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
async def joke(ctx):
    joke = ask_groq("Erzähl einen kurzen lustigen Witz.")
    await ctx.send(joke)

@client.command()
async def quote(ctx):
    quote = ask_groq("Gib mir ein kurzes inspirierendes Zitat.")
    await ctx.send(quote)

# -----------------------------
# START
# -----------------------------
keep_alive()
client.run(TOKEN)
