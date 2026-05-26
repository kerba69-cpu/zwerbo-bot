from keep_alive import keep_alive
keep_alive()

# ============================================
# ZWERBO – Ultimate Edition

# ============================================
# ZWERBO – Ultimate Edition
# Version: 3.0.0 – Ausgewogen Plus
# ============================================

import os
import random
import discord
from discord.ext import commands

# ============================================
# KONFIGURATION
# ============================================

ZWERBO_VERSION = "3.0.0 – Ultimate Edition"

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ============================================
# PERSÖNLICHKEITSMODUL – Ausgewogen Plus
# ============================================

ZWERBO_STYLE = {
    "mystisch": [
        "✨ Die Energien flüstern…",
        "🌙 Ich spüre die Strömungen der Elemente…",
        "💫 Ein Funke Magie berührt die Luft…"
    ],
    "warm": [
        "🌿 Ich bin bei dir.",
        "💛 Ruh dich einen Moment aus.",
        "🍃 Atme tief durch, ich halte Wache."
    ],
    "humor": [
        "😄 Ich bin klein, aber voller Chaos!",
        "🍪 Hast du Snacks? Ich frage für… mich.",
        "🔥 Ups… das sollte nicht brennen. Eigentlich."
    ],
    "verspielt": [
        "🐾 Ich tappse mal kurz herum…",
        "🎐 *kling-klong* … oh, das war ich.",
        "🌟 Ich glitzere heute besonders stark!"
    ]
}

def zwerbo_tonfall(kategorie):
    return random.choice(ZWERBO_STYLE.get(kategorie, ["✨"]))

# ============================================
# TRIGGER-MODUL – Synonyme, Fuzzy, Kategorien
# ============================================

TRIGGER = {
    "müde": {
        "synonyme": ["erschöpft", "kaputt", "schlafen", "mued", "müüde", "müdeee"],
        "antworten": [
            "🌙 Du wirkst müde… ruh dich aus.",
            "💤 Ich lege dir ein kleines Traumlicht hin.",
            "✨ Schlaf gut, ich halte die Elemente ruhig."
        ],
        "stil": "warm"
    },
    "snack": {
        "synonyme": ["essen", "hunger", "schokolade", "kaffee", "keks"],
        "antworten": [
            "🍪 Snacks? Ich liebe Snacks!",
            "☕ Kaffee? Ich vibriere schon.",
            "🍫 Schokolade ist pure Magie."
        ],
        "stil": "humor"
    },
    "hallo": {
        "synonyme": ["hi", "hey", "servus", "moin"],
        "antworten": [
            "✨ Hallo, Reisende.",
            "🌟 Ich grüße dich.",
            "💫 Deine Anwesenheit lässt die Luft funkeln."
        ],
        "stil": "verspielt"
    }
}

def finde_trigger(text):
    text = text.lower()
    for key, daten in TRIGGER.items():
        if key in text:
            return key
        for syn in daten["synonyme"]:
            if syn in text:
                return key
    return None

# ============================================
# FEATURE-MODUL – Magische Fähigkeiten
# ============================================

ELEMENTE = ["🔥 Feuer", "💧 Wasser", "🌿 Erde", "🌪️ Luft", "⚡ Blitz", "🌙 Schatten", "✨ Licht"]

RUNEN = {
    "ᚠ Fehu": "Wohlstand, Neubeginn, Energiefluss.",
    "ᚢ Uruz": "Kraft, Mut, innere Stärke.",
    "ᚦ Thurisaz": "Schutz, Entscheidung, Wandel.",
    "ᚨ Ansuz": "Weisheit, Klarheit, Führung."
}

def zufalls_element():
    return random.choice(ELEMENTE)

def zufalls_rune():
    return random.choice(list(RUNEN.items()))

# ============================================
# SLASH COMMANDS
# ============================================

@bot.tree.command(name="version", description="Zeigt die aktuelle ZwerBo-Version.")
async def version(interaction: discord.Interaction):
    await interaction.response.send_message(f"✨ **ZwerBo Version:** {ZWERBO_VERSION}")

@bot.tree.command(name="element", description="Zieht ein zufälliges Element.")
async def element(interaction: discord.Interaction):
    elem = zufalls_element()
    await interaction.response.send_message(f"{zwerbo_tonfall('mystisch')} Dein Element lautet: **{elem}**")

@bot.tree.command(name="rune", description="Zieht eine magische Runenkarte.")
async def rune(interaction: discord.Interaction):
    rune, bedeutung = zufalls_rune()
    await interaction.response.send_message(
        f"{zwerbo_tonfall('mystisch')} Deine Rune ist **{rune}**\n➡️ *{bedeutung}*"
    )

# ============================================
# ON_MESSAGE – Herzstück
# ============================================

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    text = message.content.lower()
    trigger = finde_trigger(text)

    if trigger:
        daten = TRIGGER[trigger]
        stil = daten["stil"]
        antwort = random.choice(daten["antworten"])
        prefix = zwerbo_tonfall(stil)
        await message.channel.send(f"{prefix} {antwort}")

    await bot.process_commands(message)

# ============================================
# START
# ============================================

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    print("❌ Kein Token gefunden! Bitte in Render → Environment Variables setzen.")
else:
    print(f"✨ ZwerBo {ZWERBO_VERSION} erwacht…")
    bot.run(TOKEN)
