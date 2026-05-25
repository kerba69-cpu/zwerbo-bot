import os
import random
import discord
from discord.ext import commands

# -----------------------------
# DISCORD BOT BASIS
# -----------------------------
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

bot = commands.Bot(command_prefix="!", intents=intents)

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
# SLASH-COMMANDS – ZwerBo Persönlichkeit & Hilfe
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
# MAGIE-SYSTEME
# -----------------------------
def geisttier():
    tiere = [
        ("🌙 Mondwolf", "ruhig, wachsam und ein bisschen dramatisch"),
        ("🔥 Funkenfuchs", "schnell, mutig und leicht chaotisch"),
        ("🌑 Schattenkatze", "mysteriös, elegant und schwer zu fassen"),
        ("💧 Wassereule", "weise, ruhig und voller Tiefe"),
        ("✨ Kristallhirsch", "rein, stolz und voller alter Magie"),
        ("🍃 Windhase", "leichtfüßig, verspielt und frei")
    ]
    tier, bedeutung = random.choice(tiere)
    return f"{tier} – {bedeutung}"

@bot.tree.command(name="geisttier", description="ZwerBo enthüllt dein magisches Geisttier.")
async def geisttier_cmd(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"✨ *Ich lausche deiner Energie…*\nDein Geisttier ist: **{geisttier()}**"
    )

def rune():
    runen = [
        ("🔥 Feuerrune", "Mut, Energie und innere Stärke"),
        ("🌙 Mondrune", "Klarheit, Ruhe und Intuition"),
        ("🌑 Nebelrune", "Geheimnisse, Wandel und innere Tiefe"),
        ("💧 Wasserrune", "Heilung, Fluss und Anpassung"),
        ("✨ Lichtrune", "Hoffnung, Reinheit und Wahrheit"),
        ("🌿 Erdrune", "Stabilität, Wachstum und Geduld")
    ]
    r, bedeutung = random.choice(runen)
    return f"{r} – {bedeutung}"

@bot.tree.command(name="rune", description="ZwerBo erschafft eine magische Rune für dich.")
async def rune_cmd(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"🔮 *Die Elemente formen ein Zeichen…*\nDeine Rune ist: **{rune()}**"
    )

@bot.tree.command(name="orakel", description="ZwerBo spricht eine kleine Prophezeiung.")
async def orakel(interaction: discord.Interaction):
    prophezeiungen = [
        "✨ *Ein ruhiger Weg liegt vor dir… doch ein Funke könnte ihn erhellen.*",
        "🌙 *Heute wird Klarheit kommen – vielleicht leise, vielleicht überraschend.*",
        "🔥 *Etwas Mut wird gebraucht… aber du hast mehr davon, als du denkst.*",
        "💧 *Lass los, was schwer ist. Das Wasser trägt dich.*",
        "🍃 *Ein kleiner Zufall wird heute ein Lächeln bringen.*"
    ]
    await interaction.response.send_message(random.choice(prophezeiungen))

# -----------------------------
# HILFE-/INFO-COMMANDS
# -----------------------------
# (… unverändert …)

# -----------------------------
# COMMUNITY-SYSTEME (on_message)
# -----------------------------
# (… unverändert …)

# -----------------------------
# REACTIONS – Dank nur bei eigenen Nachrichten
# -----------------------------
# (… unverändert …)

# -----------------------------
# START
# -----------------------------
TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)
