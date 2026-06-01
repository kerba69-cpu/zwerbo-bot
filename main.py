from keep_alive import keep_alive
keep_alive()

# ============================================
# ZWERBO – Version 3.1.1 – Final Merge + Fix
# ============================================

import os
import random
import discord
import asyncio
from discord.ext import commands, tasks
from datetime import datetime, time

# ============================================
# KONFIGURATION
# ============================================

ZWERBO_VERSION = "3.1.1 – Final Merge + Fix"

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ============================================
# STATUS-SYSTEM
# ============================================

zwerbo_status = "wach"  # wach, schläft, magie, meditierend, hyperaktiv

STATUS_DISCORD = {
    "wach": "✨ Wach und bereit",
    "schläft": "🌙 Schlafmodus – träumt von Magie…",
    "magie": "🔮 Lädt Magie…",
    "meditierend": "🌙 Meditiert im Wald",
    "hyperaktiv": "⚡ Überladen mit Energie"
}

async def update_discord_status():
    activity = discord.Game(STATUS_DISCORD.get(zwerbo_status, "✨"))
    await bot.change_presence(status=discord.Status.online, activity=activity)

# ============================================
# AUTO-SCHLAFMODUS 01:00–05:00
# ============================================

def ist_schlafzeit():
    jetzt = datetime.now().time()
    return time(1, 0) <= jetzt <= time(5, 0)

@tasks.loop(minutes=1)
async def schlaf_check():
    global zwerbo_status
    if ist_schlafzeit():
        if zwerbo_status != "schläft":
            zwerbo_status = "schläft"
            await update_discord_status()
    else:
        if zwerbo_status == "schläft":
            zwerbo_status = "wach"
            await update_discord_status()

# ============================================
# PERSÖNLICHKEIT
# ============================================

ZWERBO_STYLE = {
    "mystisch": ["✨ Die Energien flüstern…", "🌙 Ich spüre die Strömungen…", "💫 Magie liegt in der Luft…"],
    "warm": ["🌿 Ich bin bei dir.", "💛 Ruh dich aus.", "🍃 Atme tief durch."],
    "humor": ["😄 Ich bin klein, aber chaotisch!", "🍪 Hast du Snacks?", "🔥 Ups… das sollte nicht brennen."],
    "verspielt": ["🐾 Ich tappse herum…", "🎐 *kling-klong*", "🌟 Ich glitzere heute!"],
    "schlaf": ["😴 *mmh…*", "🌙 *…schlummer…*", "✨ *…träum…*"]
}

def zwerbo_tonfall(kategorie):
    return random.choice(ZWERBO_STYLE.get(kategorie, ["✨"]))

# ============================================
# LEVEL-4-TRIGGER-SYSTEM (JETZT MIT BEGRÜSSUNGEN)
# ============================================

TRIGGER = {
    "müde": {
        "synonyme": ["erschöpft", "kaputt", "schlafen", "mued", "müüde", "müdeee"],
        "antworten": ["Du wirkst müde… ruh dich aus.", "Ich lege dir ein Traumlicht hin.", "Schlaf gut, Reisende."],
        "stil": "warm"
    },
    "snack": {
        "synonyme": ["essen", "hunger", "schokolade", "kaffee", "keks"],
        "antworten": ["Snacks? Ich liebe Snacks!", "Kaffee? Ich vibriere schon.", "Schokolade ist Magie."],
        "stil": "humor"
    },
    "hallo": {
        "synonyme": ["hi", "hey", "servus", "moin"],
        "antworten": ["Hallo, Reisende.", "Ich grüße dich.", "Deine Anwesenheit funkelt."],
        "stil": "verspielt"
    },
    "guten_morgen": {
        "synonyme": ["guten morgen", "morgen", "gm"],
        "antworten": ["Guten Morgen, Reisende.", "Die Sonne grüßt dich.", "Ein neuer Tag beginnt."],
        "stil": "warm"
    },
    "guten_tag": {
        "synonyme": ["guten tag", "tag"],
        "antworten": ["Einen wundervollen Tag dir.", "Der Tag funkelt hell.", "Ich grüße dich zur hellen Stunde."],
        "stil": "verspielt"
    },
    "guten_abend": {
        "synonyme": ["guten abend", "abend"],
        "antworten": ["Einen ruhigen Abend dir.", "Die Nacht senkt sich.", "Der Abend trägt Magie."],
        "stil": "mystisch"
    },
    "gute_nacht": {
        "synonyme": ["gute nacht", "nacht"],
        "antworten": ["Schlaf gut, Reisende.", "Die Sterne wachen über dich.", "Möge die Nacht dir Ruhe schenken."],
        "stil": "warm"
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
# AUTO-EMOJI (VARIANTE B)
# ============================================

AUTO_EMOJI = {
    "müde": ("😴", "Ohje…"),
    "kaffee": ("☕", "Koffein-Magie!"),
    "schokolade": ("🍫", "Süße Energie!"),
    "yay": ("✨", "Glitzer-Boost!"),
    "juhu": ("✨", "Glitzer-Boost!"),
    "lol": ("😂", "Chaos-Lachen!"),
    "magie": ("✨", "Ich spüre es…"),
    "feuer": ("🔥", "Heiß!"),
    "licht": ("✨", "Heller wird’s…"),
    "schatten": ("🌙", "Dunkle Ruhe…"),
    "element": ("⚡", "Die Kräfte erwachen…"),
    "rune": ("ᚠ", "Alte Zeichen flüstern…"),
    "snack": ("🍪", "Ich nehme auch einen!"),
    "uff": ("😮‍💨", "Ich fühle es…"),
    "cute": ("💛", "Awww…"),
    "süß": ("💛", "Awww…"),
    "omg": ("🤯", "Dramaaa…")
}

def finde_autoemoji(text):
    text = text.lower()
    for wort, (emoji, ton) in AUTO_EMOJI.items():
        if wort in text:
            return emoji, ton
    return None

# ============================================
# RUNEN & ELEMENTE (aus 3.0.0)
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
async def version(interaction):
    await interaction.response.send_message(f"✨ **ZwerBo Version:** {ZWERBO_VERSION}")

@bot.tree.command(name="element", description="Zieht ein zufälliges Element.")
async def element(interaction):
    elem = zufalls_element()
    await interaction.response.send_message(f"{zwerbo_tonfall('mystisch')} Dein Element lautet: **{elem}**")

@bot.tree.command(name="rune", description="Zieht eine magische Runenkarte.")
async def rune(interaction):
    rune_symbol, bedeutung = zufalls_rune()
    await interaction.response.send_message(
        f"{zwerbo_tonfall('mystisch')} Deine Rune ist **{rune_symbol}**\n➡️ *{bedeutung}*"
    )

@bot.tree.command(name="status", description="Zeigt den aktuellen ZwerBo-Status.")
async def status_cmd(interaction):
    await interaction.response.send_message(f"✨ **ZwerBo Status:** {zwerbo_status}")

@bot.tree.command(name="status_set", description="Setzt den ZwerBo-Status.")
async def status_set(interaction, neuer_status: str):
    global zwerbo_status
    zwerbo_status = neuer_status
    await update_discord_status()
    await interaction.response.send_message(f"🌟 Neuer Status: **{neuer_status}**")

# ============================================
# PREFIX COMMANDS (aus 3.0.0)
# ============================================

@bot.command()
async def ping(ctx):
    await ctx.send("Pong! 🏓")

@bot.command()
async def zwerbo(ctx):
    await ctx.send("Ich bin ZwerBo – bereit für Action! 🤖🔥")

# ============================================
# REAKTIONS-DANKES-MODUL (aus 3.0.0)
# ============================================

letzter_dank = {}

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return

    if reaction.message.author != bot.user:
        return

    positive = ["❤️", "💛", "✨", "🌟", "👍", "💖", "🔥"]

    if reaction.emoji not in positive:
        return

    user_id = user.id
    jetzt = discord.utils.utcnow().timestamp()

    if user_id in letzter_dank:
        if jetzt - letzter_dank[user_id] < 5:
            return

    letzter_dank[user_id] = jetzt

    antworten = [
        "✨ Danke für die Energie!",
        "🌟 Deine Reaktion lässt mich heller leuchten.",
        "💛 Das bedeutet mir viel.",
        "🔥 Ich spüre deine Unterstützung!",
        "💫 Danke, Reisende."
    ]

    await reaction.message.channel.send(random.choice(antworten))

# ============================================
# ON_READY
# ============================================

@bot.event
async def on_ready():
    await bot.tree.sync()
    schlaf_check.start()
    await update_discord_status()
    print(f"✨ ZwerBo {ZWERBO_VERSION} ist online!")

# ============================================
# ON_MESSAGE – Trigger + Auto-Emoji + Schlafmodus
# ============================================

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    global zwerbo_status
    text = message.content.lower()

    # Auto-Emoji
    auto = finde_autoemoji(text)
    if auto:
        emoji, ton = auto
        if zwerbo_status == "schläft":
            ton = "…mmh…"
        await message.channel.send(f"{emoji} *{ton}*")

    # Trigger
    trigger = finde_trigger(text)
    if trigger:
        daten = TRIGGER[trigger]
        stil = daten["stil"]
        antwort = random.choice(daten["antworten"])

        if zwerbo_status == "schläft":
            stil = "schlaf"

        prefix = zwerbo_tonfall(stil)
        await message.channel.send(f"{prefix} {antwort}")

    await bot.process_commands(message)

# ============================================
# START
# ============================================

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    print("❌ Kein Token gefunden!")
else:
    bot.run(TOKEN)
