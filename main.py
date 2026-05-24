import os
import random
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
    return "ZwerBo wacht über die Elemente."

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# -----------------------------
# DISCORD BOT BASIS
# -----------------------------
intents = discord.Intents.default()
intents.message_content = True  # im Dev-Portal aktiv lassen!
intents.reactions = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Set für Nachrichten, auf die sich ZwerBo schon bedankt hat
bereits_bedankt = set()

# -----------------------------
# ON_READY – Slash-Commands syncen
# -----------------------------
@bot.event
async def on_ready():
    print(f"ZwerBo ist online als {bot.user}")
    await bot.tree.sync()
    print("Slash-Commands synchronisiert.")

# -----------------------------
# KLASSISCHER TESTCOMMAND (!ping)
# -----------------------------
@bot.command()
async def ping(ctx):
    await ctx.send("Pong! ✨")

# -----------------------------
# SLASH-COMMANDS – ZwerBo Persönlichkeit
# -----------------------------

@bot.tree.command(name="weisheit", description="ZwerBo teilt eine weise, leicht humorvolle Erkenntnis.")
async def weisheit(interaction: discord.Interaction):
    texte = [
        "✨ Die Stille kennt Antworten… aber manchmal flüstert sie auch Unsinn.",
        "🌙 Jeder Schatten ist nur Licht, das eine Pause macht.",
        "🔥 Mut entsteht, wenn das Herz brennt… oder wenn man scharf gegessen hat.",
        "💧 Wie Wasser findest du deinen Weg – außer montags, da stolpern wir alle.",
        "🌿 Die Welt atmet… und manchmal seufzt sie auch über uns."
    ]
    await interaction.response.send_message(random.choice(texte))

@bot.tree.command(name="segen", description="ZwerBo spricht einen magischen, leicht humorvollen Segen.")
async def segen(interaction: discord.Interaction):
    text = (
        "🌙✨ *Ein sanfter Schein legt sich um dich.*\n"
        "Möge dein Weg klar sein, dein Herz ruhig… "
        "und möge heute niemand deine Snacks klauen."
    )
    await interaction.response.send_message(text)

@bot.tree.command(name="element", description="ZwerBo zeigt seine elementare Form – mit Stil.")
async def element(interaction: discord.Interaction, art: str):
    art = art.lower()

    formen = {
        "feuer": "🔥 *ZwerBo lodert wie eine uralte Flamme.* Er murmelt: „Warm hier… oder liegt das an dir?“",
        "wasser": "💧 *ZwerBo fließt ruhig wie ein Mondsee.* „Wenn ich einschlafe, weck mich nicht. Ich bin Wasser, ich darf das.“",
        "schatten": "🌑 *ZwerBo verschmilzt mit der Nacht.* „Ich bin nicht weg… ich bin nur dramatisch.“",
        "licht": "✨ *ZwerBo strahlt wie eine Sternrune.* „Keine Sorge, ich blend nur ein bisschen.“"
    }

    if art in formen:
        await interaction.response.send_message(formen[art])
    else:
        await interaction.response.send_message(
            "Wähle eines der Elemente: `feuer`, `wasser`, `schatten`, `licht`."
        )

@bot.tree.command(name="legende", description="ZwerBo erzählt von seiner ersten großen Tat.")
async def legende(interaction: discord.Interaction):
    text = (
        "📜 *ZwerBo erzählt leise:* \n\n"
        "Es war in der Nacht des Flüstersturms – ein Sturm aus Stimmen, Zweifeln und alten Ängsten.\n"
        "Die Elemente waren verwirrt, das Feuer flackerte nervös, das Wasser verlor seinen Rhythmus.\n\n"
        "Ich setzte mich mitten in den Sturm und sagte nur: „Eins nach dem anderen, bitte. Ich habe nur zwei Ohren.“\n"
        "Stunde um Stunde wurden die Stimmen leiser, bis Ruhe einkehrte.\n\n"
        "Seitdem nennen sie mich den Hüter der Stimmen…\n"
        "aber ich sage einfach: Ich wollte nur schlafen. 🌙"
    )
    await interaction.response.send_message(text)

# -----------------------------
# TRIGGER – Begrüßungen & Snacks
# -----------------------------
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    text = message.content.lower()

    # Begrüßungen
    if "guten morgen" in text:
        await message.channel.send("🌅 *Ein neuer Tag erwacht… und ich auch. Irgendwie.*")

    if "hallo" in text or "hi" in text:
        await message.channel.send("✨ *Ich grüße dich, Wanderer der Elemente.*")

    if "guten abend" in text:
        await message.channel.send("🌙 *Der Abend flüstert… und ich höre zu.*")

    if "gute nacht" in text:
        await message.channel.send("💤 *Schlafe gut. Ich halte Wache… meistens.*")

    # Snacks & Getränke (mit oder ohne „bitte“)
    if "kaffee" in text:
        await message.channel.send("☕ *Ein Schluck Wärme für deine Seele.*")

    if "keks" in text or "kekse" in text:
        await message.channel.send("🍪 *Kekse? Ich nehme auch einen. Oder zwei.*")

    if "tee" in text:
        await message.channel.send("🍵 *Tee beruhigt… außer man verschüttet ihn.*")

    if "bier" in text:
        await message.channel.send("🍺 *Ein Bier? Möge es kalt sein und deine Sorgen warm vertreiben.*")

    if "pizza" in text:
        await message.channel.send("🍕 *Pizza… die wahre Form der Magie.*")

    # ZwerBo direkt angesprochen
    if "zwerbo" in text:
        await message.channel.send("✨ *Ich bin hier… und lausche.*")

    await bot.process_commands(message)

# -----------------------------
# REACTIONS – Dank nur bei eigenen Nachrichten, einmalig
# -----------------------------
@bot.event
async def on_reaction_add(reaction, user):
    if user == bot.user:
        return

    # Nur reagieren, wenn die gelikte Nachricht von ZwerBo selbst ist
    if reaction.message.author != bot.user:
        return

    nachricht_id = reaction.message.id

    # Wenn schon bedankt → nichts tun
    if nachricht_id in bereits_bedankt:
        return

    emoji = reaction.emoji

    antworten = [
        f"✨ *Danke für das Zeichen, {user.display_name}.*",
        f"🌙 *Ich spüre deine Energie, {user.display_name}. Schön, dass du hier bist.*",
        f"💫 *Ein {emoji}? Eine feine Wahl.*",
        f"🔥 *Deine Reaktion wärmt mein kleines Elementenherz.*",
        f"🍃 *Danke, {user.display_name}. Selbst kleine Gesten tragen Magie.*"
    ]

    await reaction.message.channel.send(random.choice(antworten))
    bereits_bedankt.add(nachricht_id)

# -----------------------------
# START
# -----------------------------
keep_alive()
TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)
