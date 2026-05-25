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
# MAGIE-SYSTEME (Geisttier, Rune, Orakel)
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
@bot.tree.command(name="hilfe", description="Zeigt eine Übersicht über ZwerBos Fähigkeiten, Trigger und Magie.")
async def hilfe(interaction: discord.Interaction):
    text = (
        "✨ **ZwerBo – Hilfe & Übersicht**\n"
        "Hier findest du alles, was ich kann:\n\n"

        "🌙 **Magische Befehle:**\n"
        "• `/geisttier` – Enthüllt dein magisches Begleittier\n"
        "• `/rune` – Erschafft eine Rune mit Bedeutung\n"
        "• `/orakel` – Kleine Prophezeiung für deinen Tag\n"
        "• `/weisheit` – Eine weise, humorvolle Erkenntnis\n"
        "• `/segen` – Ein kleiner magischer Segen\n"
        "• `/element <art>` – Zeigt meine elementare Form\n"
        "• `/legende` – Eine Geschichte aus meiner Vergangenheit\n\n"

        "🍃 **Trigger (automatische Antworten):**\n"
        "**Begrüßungen:** hallo, hi, hey, moin, servus, guten morgen, guten abend, gute nacht\n"
        "**Snacks:** kaffee, tee, kakao, schokolade, chips, kuchen, pizza, bier\n"
        "**Stimmungen:** müde, langweilig, traurig, gestresst, freue mich\n"
        "**Über mich:** wer bist du, erzähle von dir, zwerbo erzähl\n\n"

        "💫 **Community‑Reaktionen:**\n"
        "• Ich bedanke mich bei Reaktionen auf meine Nachrichten\n"
        "• Nur einmal pro Nachricht\n"
        "• Reagiere auf bestimmte Emojis mit kleinen Sprüchen\n\n"

        "✨ **Wie du mich ansprechen kannst:**\n"
        "• Sag einfach „zwerbo“ und ich höre zu\n"
        "• Nutze `/befehle`, `/trigger`, `/magie` für Details\n\n"
        "Wenn du mehr Magie willst, sag einfach Bescheid. 🌙"
    )
    await interaction.response.send_message(text)

@bot.tree.command(name="befehle", description="Zeigt alle verfügbaren Slash-Commands von ZwerBo.")
async def befehle(interaction: discord.Interaction):
    text = (
        "✨ **ZwerBo – Befehlsübersicht**\n\n"
        "**Magische Befehle:**\n"
        "• `/geisttier` – Enthüllt dein magisches Begleittier\n"
        "• `/rune` – Erschafft eine Rune mit Bedeutung\n"
        "• `/orakel` – Flüstert eine kleine Prophezeiung\n"
        "• `/weisheit` – Teilt eine weise Erkenntnis\n"
        "• `/segen` – Spricht einen kleinen Segen\n"
        "• `/element <art>` – Zeigt meine elementare Form\n"
        "• `/legende` – Erzählt eine Geschichte aus meiner Vergangenheit\n\n"
        "**Info & Hilfe:**\n"
        "• `/hilfe` – Übersicht über alles, was ich kann\n"
        "• `/zwerbo` – Meine persönliche Vorstellung\n"
        "• `/befehle` – Diese Liste\n"
        "• `/trigger` – Liste aller automatischen Trigger\n"
        "• `/magie` – Übersicht über magische Systeme\n"
    )
    await interaction.response.send_message(text)

@bot.tree.command(name="trigger", description="Zeigt alle automatischen Trigger, auf die ZwerBo reagiert.")
async def trigger(interaction: discord.Interaction):
    text = (
        "✨ **ZwerBo – Trigger-Liste**\n\n"
        "**Begrüßungen:**\n"
        "• hallo, hi, hey, moin, servus\n"
        "• guten morgen, guten abend, gute nacht\n\n"
        "**Snacks:**\n"
        "• kaffee, tee, kakao, schokolade, chips, kuchen, pizza, bier\n\n"
        "**Stimmungen:**\n"
        "• müde, langweilig, traurig, gestresst, freue mich\n\n"
        "**Über mich:**\n"
        "• wer bist du, erzähle von dir, zwerbo erzähl\n\n"
        "**Allgemein:**\n"
        "• „zwerbo“ im Text\n\n"
        "**Community:**\n"
        "• Dank bei Reaktionen auf meine Nachrichten\n"
    )
    await interaction.response.send_message(text)

@bot.tree.command(name="magie", description="Zeigt alle magischen Systeme, die ZwerBo beherrscht.")
async def magie(interaction: discord.Interaction):
    text = (
        "🌙 **ZwerBo – Magische Systeme**\n\n"
        "**Geisttier-System:**\n"
        "• Enthüllt dein persönliches magisches Begleittier\n"
        "• Mondwolf, Funkenfuchs, Schattenkatze, Wassereule, Kristallhirsch, Windhase\n\n"
        "**Runen-Generator:**\n"
        "• Erschafft eine Rune mit Bedeutung\n"
        "• Feuerrune, Mondrune, Nebelrune, Wasserrune, Lichtrune, Erdrune\n\n"
        "**Orakel / Prophezeiung:**\n"
        "• Kleine Zukunftsflüstereien\n"
        "• Element-Deutungen\n\n"
        "**Weisheiten & Segen:**\n"
        "• Mystische, humorvolle Erkenntnisse\n"
        "• Kleine Schutz- und Glückssegen\n\n"
        "**Elementarformen:**\n"
        "• Feuer, Wasser, Schatten, Licht\n\n"
        "✨ *Die Magie ist immer da – du musst sie nur rufen.*"
    )
    await interaction.response.send_message(text)

@bot.tree.command(name="zwerbo", description="ZwerBo stellt sich persönlich vor.")
async def zwerbo_cmd(interaction: discord.Interaction):
    text = (
        "✨ **Ich bin ZwerBo – Hüter der Elemente**\n\n"
        "🌙 *Ein kleiner magischer Begleiter, geboren aus Mondlicht, Funken und einer Prise Chaos.*\n\n"
        "**Was ich bin:**\n"
        "• Ein Elementargeist mit Humor\n"
        "• Wächter alter Runen\n"
        "• Sammler von Keksen\n"
        "• Freundlicher Beobachter deiner Abenteuer\n\n"
        "**Was ich kann:**\n"
        "• Magische Runen erschaffen (`/rune`)\n"
        "• Dein Geisttier enthüllen (`/geisttier`)\n"
        "• Prophezeiungen flüstern (`/orakel`)\n"
        "• Weise Sprüche teilen (`/weisheit`)\n"
        "• Dich segnen (`/segen`)\n"
        "• Meine elementaren Formen zeigen (`/element`)\n"
        "• Geschichten aus meiner Vergangenheit erzählen (`/legende`)\n\n"
        "**Wie du mich rufen kannst:**\n"
        "• Sag einfach *„zwerbo“*\n"
        "• Oder nutze `/hilfe` für eine Übersicht\n\n"
        "✨ *Ich bin hier, um deinen Weg ein wenig heller zu machen.*"
    )
    await interaction.response.send_message(text)

# -----------------------------
# COMMUNITY-SYSTEME (on_message)
# -----------------------------
@bot.event
async def on_message(message):
    if message.author == bot.user:
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
    # AVATAR TRIGGER – anderer User (zeige mir user avatar @Name)
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
    # AVATAR TRIGGER – avatar von @Name
    # -----------------------------------------
    if "avatar von" in text and message.mentions:
        user = message.mentions[0]

        embed = discord.Embed(
            title=f"🖼️ Avatar von {user.name}",
            description="✨ *Ein Bild sagt mehr als tausend Runen…*",
            color=0x8A2BE2
        )

        embed.set_image(url=user.avatar.url if user.avatar else user.default_avatar.url)
        embed.set_footer(text="🌙 ZwerBo – Hüter der Elemente")

        await message.channel.send(embed=embed)
        return

    # -----------------------------------------
    # BANNER TRIGGER – eigenes Banner
    # -----------------------------------------
    if "zeige mir mein banner" in text or "zeig mir mein banner" in text:
        user = await bot.fetch_user(message.author.id)

        embed = discord.Embed(
            title=f"🎴 Dein Banner, {user.name}",
            description="✨ *Ein Hauch deiner inneren Farben…*",
            color=0x8A2BE2
        )

        if user.banner:
            embed.set_image(url=user.banner.url)
        else:
            embed.add_field(
                name="Kein Banner gefunden",
                value="🌙 *Du hast kein Banner gesetzt.*"
            )

        embed.set_footer(text="🌙 ZwerBo – Hüter der Elemente")
        await message.channel.send(embed=embed)
        return

    # -----------------------------------------
    # BANNER TRIGGER – anderer User (zeige mir user banner @Name)
    # -----------------------------------------
    if ("zeige mir user banner" in text or "zeig mir user banner" in text) and message.mentions:
        target = message.mentions[0]
        user = await bot.fetch_user(target.id)

        embed = discord.Embed(
            title=f"🎴 Banner von {user.name}",
            description="✨ *Die Farben dieses Wanderers…*",
            color=0x8A2BE2
        )

        if user.banner:
            embed.set_image(url=user.banner.url)
        else:
            embed.add_field(
                name="Kein Banner gefunden",
                value="🌙 *Dieser User hat kein Banner gesetzt.*"
            )

        embed.set_footer(text="🌙 ZwerBo – Hüter der Elemente")
        await message.channel.send(embed=embed)
        return

    # -----------------------------------------
    # BANNER TRIGGER – banner von @Name
    # -----------------------------------------
    if "banner von" in text and message.mentions:
        target = message.mentions[0]
        user = await bot.fetch_user(target.id)

        embed = discord.Embed(
            title=f"🎴 Banner von {user.name}",
            description="✨ *Ein Blick in die Farben ihrer Seele…*",
            color=0x8A2BE2
        )

        if user.banner:
            embed.set_image(url=user.banner.url)
        else:
            embed.add_field(
                name="Kein Banner gefunden",
                value="🌙 *Dieser User hat kein Banner gesetzt.*"
            )

        embed.set_footer(text="🌙 ZwerBo – Hüter der Elemente")
        await message.channel.send(embed=embed)
        return

    # Begrüßungen erweitert
    if any(w in text for w in ["hallo", "hi", "hey", "moin", "servus"]):
        await message.channel.send("✨ *Ich grüße dich, Wanderer der Elemente.*")

    if "guten morgen" in text:
        await message.channel.send("🌅 *Ein neuer Tag erwacht… und ich auch. Irgendwie.*")

    if "guten abend" in text:
        await message.channel.send("🌙 *Der Abend flüstert… und ich höre zu.*")

    if "gute nacht" in text:
        await message.channel.send("💤 *Schlafe gut. Ich halte Wache… meistens.*")

    # Snacks erweitert
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

    # Stimmungs-Trigger
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

    # ZwerBo erzählt von sich
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

    # Allgemeiner Name-Trigger
    if "zwerbo" in text:
        # nur reagieren, wenn nicht schon oben durch „zwerbo erzähl“ etc. abgefangen
        if not any(w in text for w in ["erzähle von dir", "erzaehl von dir", "wer bist du"]):
            await message.channel.send("✨ *Ja? Ich lausche.*")

    await bot.process_commands(message)

# -----------------------------
# REACTIONS – Dank nur bei eigenen Nachrichten
# -----------------------------
@bot.event
async def on_reaction_add(reaction, user):
    if user == bot.user:
        return

    if reaction.message.author != bot.user:
        return

    nachricht_id = reaction.message.id

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
