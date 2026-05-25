import os
import random
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

# -----------------------------
# KEEP-ALIVE SERVER (Render)
# -----------------------------
app = Flask(__name__)

@app.route("/")
def home():
    return "ZwerBo wacht über die Elemente."

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    thread = Thread(target=run)
    thread.start()

# -----------------------------
# DISCORD BOT BASIS
# -----------------------------
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

bot = commands.Bot(command_prefix="!", intents=intents)
bereits_bedankt = set()

# -----------------------------
# ON_READY – Slash Commands Sync
# -----------------------------
@bot.event
async def on_ready():
    print(f"ZwerBo ist online als {bot.user}")

    try:
        synced = await bot.tree.sync()
        print(f"Slash-Commands synchronisiert ({len(synced)} Befehle).")
    except Exception as e:
        print("Fehler beim Sync:", e)

# -----------------------------
# SLASH COMMANDS
# -----------------------------
@bot.tree.command(name="weisheit", description="ZwerBo teilt eine weise Erkenntnis.")
async def weisheit(interaction: discord.Interaction):
    texte = [
        "✨ Die Stille kennt Antworten… aber manchmal flüstert sie auch Unsinn.",
        "🌙 Jeder Schatten ist nur Licht, das eine Pause macht.",
        "🔥 Mut entsteht, wenn das Herz brennt… oder wenn man scharf gegessen hat.",
        "💧 Wie Wasser findest du deinen Weg – außer montags.",
        "🌿 Die Welt atmet… und manchmal seufzt sie auch über uns."
    ]
    await interaction.response.send_message(random.choice(texte))

@bot.tree.command(name="segen", description="ZwerBo spricht einen magischen Segen.")
async def segen(interaction: discord.Interaction):
    text = (
        "🌙✨ *Ein sanfter Schein legt sich um dich.*\n"
        "Möge dein Weg klar sein, dein Herz ruhig… "
        "und möge heute niemand deine Snacks klauen."
    )
    await interaction.response.send_message(text)

@bot.tree.command(name="element", description="ZwerBo zeigt seine elementare Form.")
async def element(interaction: discord.Interaction, art: str):
    formen = {
        "feuer": "🔥 *ZwerBo lodert wie eine uralte Flamme.*",
        "wasser": "💧 *ZwerBo fließt ruhig wie ein Mondsee.*",
        "schatten": "🌑 *ZwerBo verschmilzt mit der Nacht.*",
        "licht": "✨ *ZwerBo strahlt wie eine Sternrune.*"
    }
    art = art.lower()
    if art in formen:
        await interaction.response.send_message(formen[art])
    else:
        await interaction.response.send_message("Wähle: feuer, wasser, schatten, licht.")

@bot.tree.command(name="geisttier", description="ZwerBo enthüllt dein Geisttier.")
async def geisttier_cmd(interaction: discord.Interaction):
    tiere = [
        "🌙 Mondwolf – ruhig und wachsam",
        "🔥 Funkenfuchs – mutig und chaotisch",
        "🌑 Schattenkatze – elegant und geheimnisvoll",
        "💧 Wassereule – weise und tief",
        "✨ Kristallhirsch – rein und stolz",
        "🍃 Windhase – frei und verspielt"
    ]
    await interaction.response.send_message(f"✨ Dein Geisttier ist: **{random.choice(tiere)}**")

@bot.tree.command(name="rune", description="ZwerBo erschafft eine Rune.")
async def rune_cmd(interaction: discord.Interaction):
    runen = [
        "🔥 Feuerrune – Mut und Energie",
        "🌙 Mondrune – Klarheit und Intuition",
        "🌑 Nebelrune – Wandel und Geheimnisse",
        "💧 Wasserrune – Heilung und Fluss",
        "✨ Lichtrune – Hoffnung und Wahrheit",
        "🌿 Erdrune – Stabilität und Wachstum"
    ]
    await interaction.response.send_message(f"🔮 Deine Rune ist: **{random.choice(runen)}**")

@bot.tree.command(name="orakel", description="ZwerBo spricht eine Prophezeiung.")
async def orakel(interaction: discord.Interaction):
    texte = [
        "✨ *Ein ruhiger Weg liegt vor dir…*",
        "🌙 *Heute wird Klarheit kommen.*",
        "🔥 *Etwas Mut wird gebraucht.*",
        "💧 *Lass los, was schwer ist.*",
        "🍃 *Ein kleiner Zufall bringt ein Lächeln.*"
    ]
    await interaction.response.send_message(random.choice(texte))

# -----------------------------
# COMMUNITY-TRIGGER (on_message)
# -----------------------------
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    text = message.content.lower()

    # -----------------------------------------
    # AVATAR TRIGGER – eigener Avatar
    # -----------------------------------------
    if "zeige mir meinen avatar" in text or "zeig mir meinen avatar" in text:
        user = message.author

        embed = discord.Embed(
            title=f"🖼️ Dein Avatar, {user.name}",
            description="✨ *Ein Spiegel deiner Energie…*",
            color=0x8A2BE2
        )

        embed.set_image(url=user.avatar.url if user.avatar else user.default_avatar.url)
        embed.set_footer(text="🌙 ZwerBo – Hüter der Elemente")

        await message.channel.send(embed=embed)
        return

    # -----------------------------------------
    # AVATAR TRIGGER – anderer User
    # -----------------------------------------
    if ("zeige mir user avatar" in text or "zeig mir user avatar" in text) and message.mentions:
        user = message.mentions[0]

        embed = discord.Embed(
            title=f"🖼️ Avatar von {user.name}",
            description="✨ *Ein Bild voller Persönlichkeit…*",
            color=0x8A2BE2
        )

        embed.set_image(url=user.avatar.url if user.avatar else user.default_avatar.url)
        embed.set_footer(text="🌙 ZwerBo – Hüter der Elemente")

        await message.channel.send(embed=embed)
        return

    # -----------------------------------------
    # BEGRÜSSUNGEN
    # -----------------------------------------
    if any(w in text for w in ["hallo", "hi", "hey", "moin", "servus"]):
        await message.channel.send("✨ *Ich grüße dich, Wanderer der Elemente.*")

    if "guten morgen" in text:
        await message.channel.send("🌅 *Ein neuer Tag erwacht…*")

    if "guten abend" in text:
        await message.channel.send("🌙 *Der Abend flüstert…*")

    if "gute nacht" in text:
        await message.channel.send("💤 *Schlafe gut.*")

    # -----------------------------------------
    # SNACKS
    # -----------------------------------------
    snacks = {
        "kaffee": "☕ *Ein Schluck Wärme für deine Seele.*",
        "kakao": "🍫 *Süß, warm und perfekt für ruhige Momente.*",
        "schokolade": "🍫 *Schokolade… die beste Art, Magie zu essen.*",
        "chips": "🍟 *Knuspern ist eine Form der Meditation.*",
        "kuchen": "🍰 *Kuchen ist Liebe in Scheiben.*",
        "tee": "🍵 *Tee beruhigt… außer man verschüttet ihn.*",
        "pizza": "🍕 *Pizza… die wahre Form der Magie.*",
        "bier": "🍺 *Möge es kalt sein und deine Sorgen warm vertreiben.*"
    }

    for wort, antwort in snacks.items():
        if wort in text:
            await message.channel.send(antwort)

    # -----------------------------------------
    # STIMMUNGEN
    # -----------------------------------------
    if "müde" in text:
        await message.channel.send("😴 *Ich spüre deine Müdigkeit… ruh dich kurz aus.*")

    if "langweilig" in text:
        await message.channel.send("🍃 *Langeweile ist nur ein schlafendes Abenteuer.*")

    if "traurig" in text:
        await message.channel.send("💙 *Ich sende dir ein wenig Licht. Du bist nicht allein.*")

    if "gestresst" in text:
        await message.channel.send("💧 *Atme tief. Die Elemente stehen hinter dir.*")

    if "freue mich" in text:
        await message.channel.send("✨ *Deine Freude leuchtet heller als jede Rune.*")

    # -----------------------------------------
    # ÜBER ZWERBO
    # -----------------------------------------
    if any(w in text for w in [
        "wer bist du", "erzähle von dir", "zwerbo erzähl", "zwerbo erzaehl", "zwerbo wer bist du"
    ]):
        antworten = [
            "✨ *Ich bin ZwerBo, Hüter der Elemente… klein, aber erstaunlich organisiert.*",
            "🌙 *Man nennt mich ZwerBo. Ich sortiere Chaos, beruhige Stürme und esse Kekse.*",
            "🔥 *Ich bin ZwerBo. Halb Magie, halb Geduld, halb Humor… ja, das sind drei Hälften.*",
            "💫 *Ich bin ein alter Runenhüter. Und trotzdem finde ich moderne Snacks faszinierend.*",
            "🍃 *ZwerBo, zu Diensten. Ich höre den Elementen zu… und manchmal auch dir.*"
        ]
        await message.channel.send(random.choice(antworten))
        return

    # -----------------------------------------
    # ALLGEMEINER NAME-TRIGGER
    # -----------------------------------------
    if "zwerbo" in text:
        if not any(w in text for w in ["erzähle von dir", "wer bist du"]):
            await message.channel.send("✨ *Ja? Ich lausche.*")

    # -----------------------------------------
    # WICHTIG: Slash-Commands weiter funktionieren lassen
    # -----------------------------------------
    await bot.process_commands(message)

# -----------------------------
# REACTIONS
# -----------------------------
@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    if reaction.message.author != bot.user:
        return
    if reaction.message.id in bereits_bedankt:
        return

    antworten = [
        f"✨ *Danke für das Zeichen, {user.display_name}.*",
        f"🌙 *Ich spüre deine Energie, {user.display_name}.*",
        f"💫 *Ein schönes Emoji.*",
    ]
    await reaction.message.channel.send(random.choice(antworten))
    bereits_bedankt.add(reaction.message.id)

# -----------------------------
# START
# -----------------------------
keep_alive()

TOKEN = os.getenv("TOKEN")
if TOKEN is None:
    print("❌ FEHLER: TOKEN nicht gesetzt! Bitte in Render → Environment eintragen.")
else:
    bot.run(TOKEN)
