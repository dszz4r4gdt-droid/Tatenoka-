import discord
from discord.ext import commands
import os

TOKEN = os.getenv("TOKEN")

STAFF_ID = 1192474010697605133

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)


@bot.event
async def on_ready():
    print(f"{bot.user} is online!")
    print("Commands:", [cmd.name for cmd in bot.commands])


# =====================
# COMMANDES GENERALES
# =====================

@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong !")


@bot.command(name="commands")
async def commands_list(ctx):

    embed = discord.Embed(
        title="⬛🟥 𝐓𝐀𝐓𝐄𝐍𝐎𝐊𝐀𝐈 | COMMANDES 🟥⬛",
        description="""
**🛡️ MODÉRATION**
`!kick @user raison`
`!ban @user raison`
`!unban ID`
`!clear nombre`
`!mute @user`
`!unmute @user`
`!warn @user raison`

**⚔️ UTILITAIRES**
`!ping`
`!userinfo`
`!avatar`
`!serverinfo`

**🏯 TATENOKAI**
`!reglement`
`!apply`
        """,
        color=discord.Color.dark_red()
    )

    await ctx.send(embed=embed)


# =====================
# MODERATION
# =====================

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="Aucune raison"):
    await member.kick(reason=reason)
    await ctx.send(f"🟥 {member} expulsé.\nRaison : {reason}")


@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="Aucune raison"):
    await member.ban(reason=reason)
    await ctx.send(f"🟥 {member} banni.\nRaison : {reason}")


@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, user_id:int):

    user = await bot.fetch_user(user_id)

    await ctx.guild.unban(user)

    await ctx.send(f"✅ {user} débanni.")


@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount:int):

    await ctx.channel.purge(limit=amount+1)

    await ctx.send(
        f"🧹 {amount} messages supprimés."
    )


@bot.command()
@commands.has_permissions(manage_messages=True)
async def warn(ctx, member:discord.Member, *, reason="Aucune raison"):

    await ctx.send(
        f"⚠️ {member.mention} averti.\nRaison : {reason}"
    )


@bot.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member:discord.Member):

    role = discord.utils.get(
        ctx.guild.roles,
        name="Muted"
    )

    if not role:
        role = await ctx.guild.create_role(
            name="Muted"
        )

    await member.add_roles(role)

    await ctx.send(
        f"🔇 {member} mute."
    )


@bot.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member:discord.Member):

    role = discord.utils.get(
        ctx.guild.roles,
        name="Muted"
    )

    if role:
        await member.remove_roles(role)

    await ctx.send(
        f"🔊 {member} unmute."
    )


# =====================
# REGLEMENT
# =====================

@bot.command()
async def reglement(ctx):

    embed = discord.Embed(
        title="⬛🟥 𝐓𝐀𝐓𝐄𝐍𝐎𝐊𝐀𝐈 🟥⬛\n𝐂𝐎𝐃𝐄 𝐃𝐔 𝐂𝐋𝐀𝐍",
        description="""

━━━━━━━━━━━━━━

🟥 **IDENTITÉ DU CLAN**

Rejoindre Tatenokai signifie représenter son nom et son héritage.

Chaque membre doit protéger l'image du clan.

**Honneur • Discipline • Unité**

━━━━━━━━━━━━━━

⬜ **COMPORTEMENT**

Respect obligatoire envers chaque membre.

Interdit :
🔴 Toxicité
🔴 Provocations inutiles
🔴 Actions nuisant au clan

━━━━━━━━━━━━━━

⚔️ **RP DU CLAN**

Les membres doivent :

⬛ Respecter l'immersion.
⬛ Jouer avec fair-play.
⬛ Éviter le metagaming.
⬛ Éviter le powergaming.

━━━━━━━━━━━━━━

⚖️ **SANCTIONS**

⬜ Avertissement

🟥 Suspension

⬛ Expulsion

━━━━━━━━━━━━━━

⬛🟥 TATENOKAI 🟥⬛
        """,
        color=discord.Color.dark_red()
    )

    await ctx.send(embed=embed)


# =====================
# CANDIDATURE RP
# =====================

@bot.command()
async def apply(ctx):

    user = ctx.author

    questions = [

"🟥 **1 | ORIGINE DE LA DÉCOUVERTE**\nComment avez-vous découvert Tatenokai ?",

"🟥 **2 | MOTIVATION D’INTÉGRATION**\nPourquoi souhaitez-vous rejoindre Tatenokai ?",

"🟥 **3 | IDENTITÉ DU PERSONNAGE**\nQuel est l’âge de votre personnage Gakuran ?",

"🟥 **4 | HISTOIRE DU PERSONNAGE**\nPrésentez le lore de votre personnage Gakuran.",

"🟥 **5 | ORIGINE DU PERSONNAGE**\nQuelle est l’origine de votre personnage Gakuran ?",

"🟥 **6 | ART DU COMBAT**\nQuel est le style de combat de votre personnage Gakuran ?"
    ]

    answers=[]

    await user.send(
        "⬛🟥 **DOSSIER D’ADMISSION RP TATENOKAI** 🟥⬛"
    )


    for q in questions:

        await user.send(q)

        msg = await bot.wait_for(
            "message",
            timeout=300,
            check=lambda m:m.author==user and isinstance(m.channel,discord.DMChannel)
        )

        answers.append(msg.content)


    staff = await bot.fetch_user(STAFF_ID)

    embed = discord.Embed(
        title="⬛🟥 Nouvelle candidature Tatenokai 🟥⬛",
        color=discord.Color.dark_red()
    )


    for i,a in enumerate(answers):

        embed.add_field(
            name=f"Réponse {i+1}",
            value=a,
            inline=False
        )


    await staff.send(embed=embed)

    await user.send(
        "✅ Votre candidature a été envoyée."
    )


# =====================

@bot.command()
async def avatar(ctx, member:discord.Member=None):

    member = member or ctx.author

    await ctx.send(member.avatar.url)


@bot.command()
async def serverinfo(ctx):

    await ctx.send(
        f"🏯 {ctx.guild.name}\n👥 {ctx.guild.member_count} membres"
    )


bot.run(TOKEN)
