import os
import discord
from discord.ext import commands
import aiohttp
import json
import datetime

# ---------------------------------------------------------
# ZWERBO 4.0.0 – KI EDITION (GROQ + LLAMA)
# ---------------------------------------------------------

TOKEN = os.getenv("TOKEN")
GROQ_KEY = os.getenv("GROQ_API_KEY")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# ---------------------------------------------------------
# MEMORY SYSTEM (einfach, lokal, sicher)
# ---------------------------------------------------------
memory = {
    "user_preferences": {},
    "conversation_history": []
}

def add_memory(key, value):
    memory["user_preferences"][key] = value

def add_history(role, content):
    memory["conversation_history"].append({"role": role, "content": content})
    # Begrenzen, damit es nicht zu groß wird
    if len(memory["conversation_history"]) > 20:
        memory["conversation_history"].pop(0)

# ---------------------------------------------------------
# KI-ANFRAGE AN GROQ (LLAMA 3)
# ---------------------------------------------------------
async def ask_groq(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_KEY}"
    }

    # Persönlichkeit von ZwerBo
    personality = """
    Du bist ZwerBo, ein magischer, verspielter, leicht chaotischer,
    aber weiser und warmherziger Waldgeist-Bot.
    Du antwortest freundlich, mystisch, humorvoll und mit Herz.
    Du nutzt gerne kleine magische Bilder, Metaphern und Emotionen.
    """

    # Memory einbauen
    memory_text = json.dumps(memory["user_preferences"], ensure_ascii=False)

    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": personality},
            {"role": "system", "content": f"Dies sind gespeicherte Erinnerungen über den Nutzer: {memory_text}"},
        ] + memory["conversation_history"] + [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.8
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as resp:
            result = await resp.json()
            try:
                return result["choices"][0]["message"]["content"]
            except:
                return "Uff… da ist mir ein Funken Magie entglitten."

# ---------------------------------------------------------
# AUTO-EMOJI SYSTEM
# ---------------------------------------------------------
def auto_emoji(message):
    text = message.lower()
    if "hallo" in text or "hi" in text:
        return "✨"
    if "wolf" in text:
        return "🐺"
    if "magie" in text:
        return "🔮"
    if "nacht" in text:
        return "🌙"
    return ""

# ---------------------------------------------------------
# DISCORD EVENTS
# ---------------------------------------------------------
@bot.event
async def on_ready():
    print(f"ZwerBo 4.0.0 ist online als {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    user_text = message.content
    add_history("user", user_text)

    # Memory Beispiel: merkt sich Lieblingssnacks
    if "ich mag" in user_text.lower():
        try:
            snack = user_text.lower().split("ich mag")[1].strip()
            add_memory("lieblingssnack", snack)
        except:
            pass

    # Auto-Emoji
    emoji = auto_emoji(user_text)

    # KI-Antwort (Modus B: immer KI)
    ai_answer = await ask_groq(user_text)
    add_history("assistant", ai_answer)

    await message.channel.send(ai_answer + " " + emoji)

# ---------------------------------------------------------
# START
# ---------------------------------------------------------
bot.run(TOKEN)
