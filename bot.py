import discord
from discord.ext import commands
import os

TOKEN = os.getenv("TOKEN")

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
# COMMANDES
# =====================

@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong !")


@bot.command(name="commands")
async def commands_list(ctx):
    embed = discord.Embed(
        title="⬛🟥 𝐆𝐀𝐊𝐔𝐑𝐀𝐍 | Commandes 🟥⬛",
        description="""
**🛡️ Modération**
`!kick @user raison`
`!ban @user raison`
`!unban ID`
`!clear nombre`
`!mute @user`
`!unmute @user`
`!warn @user raison`

**⚔️ Utilitaires**
`!ping`
`!userinfo`
`!avatar`
`!serverinfo`

**📜 Clan**
`!reglement`
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
    await ctx.send(f"🟥 {member} a été expulsé.\nRaison : {reason}")


@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="Aucune raison"):
    await member.ban(reason=reason)
    await ctx.send(f"🟥 {member} a été banni.\nRaison : {reason}")


@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, user_id: int):
    user = await bot.fetch_user(user_id)
    await ctx.guild.unban(user)
    await ctx.send(f"⬜ {user} a été débanni.")


@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    msg = await ctx.send(f"🧹 {amount} messages supprimés.")
    await msg.delete(delay=5)


@bot.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member):

    role = discord.utils.get(
        ctx.guild.roles,
        name="Muted"
    )

    if role is None:
        role = await ctx.guild.create_role(
            name="Muted"
        )

    await member.add_roles(role)

    await ctx.send(f"🔇 {member} est mute.")


@bot.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):

    role = discord.utils.get(
        ctx.guild.roles,
        name="Muted"
    )

    if role:
        await member.remove_roles(role)

    await ctx.send(f"🔊 {member} est unmute.")


@bot.command()
@commands.has_permissions(manage_messages=True)
async def warn(ctx, member: discord.Member, *, reason="Aucune raison"):

    await ctx.send(
        f"⚠️ {member.mention} a reçu un avertissement.\n"
        f"Raison : {reason}"
    )


# =====================
# REGLEMENT GAKURAN
# =====================

@bot.command()
async def reglement(ctx):

    embed = discord.Embed(
        title="⬛🟥 𝐆𝐀𝐊𝐔𝐑𝐀𝐍 🟥⬛\n「 𝐂𝐎𝐃𝐄 𝐃𝐔 𝐂𝐋𝐀𝐍 」",
        description="""

━━━━━━━━━━━━━━━━━━━━━━

🟥 **𝐈𝐃𝐄𝐍𝐓𝐈𝐓𝐄́ 𝐃𝐔 𝐂𝐋𝐀𝐍**

Rejoindre Gakuran signifie porter son nom, son symbole et son héritage.

Chaque membre représente le clan à travers son comportement, ses actes et sa réputation.

**Loyauté • Discipline • Respect**

━━━━━━━━━━━━━━━━━━━━━━

⬜ **𝐂𝐎𝐌𝐏𝐎𝐑𝐓𝐄𝐌𝐄𝐍𝐓**

Chaque membre doit :

⚪ Respecter les membres.
⚪ Respecter la hiérarchie.
⚪ Protéger l'image du clan.
⚪ Participer aux activités.

Interdit :

🔴 Toxicité.
🔴 Provocations inutiles.
🔴 Actions nuisant au clan.

━━━━━━━━━━━━━━━━━━━━━━

🟥 **𝐇𝐈𝐄́𝐑𝐀𝐑𝐂𝐇𝐈𝐄**

La hiérarchie maintient l'ordre.

Les membres doivent :

⬛ Respecter les responsables.
⬛ Suivre les directives.
⬛ Accepter les décisions.

━━━━━━━━━━━━━━━━━━━━━━

⚔️ **𝐑𝐏 𝐃𝐔 𝐂𝐋𝐀𝐍**

Lors des activités RP :

⚪ Fair-play obligatoire.
⚪ Respect de l'immersion.
⚪ Aucun metagaming.
⚪ Aucun powergaming.

La qualité du RP passe avant la victoire.

━━━━━━━━━━━━━━━━━━━━━━

⬛ **𝐇𝐑𝐏**

Les membres doivent :

⚪ Rester respectueux.
⚪ Régler les conflits calmement.
⚪ Garder les informations internes.

━━━━━━━━━━━━━━━━━━━━━━

⚖️ **𝐒𝐀𝐍𝐂𝐓𝐈𝐎𝐍𝐒**

⬜ Avertissement

🟥 Suspension

⬛ Retrait de grade

🟥 Expulsion

━━━━━━━━━━━━━━━━━━━━━━

🩸 « Porter Gakuran est un privilège. »

⬛🟥 𝐇𝐎𝐍𝐍𝐄𝐔𝐑 • 𝐃𝐈𝐒𝐂𝐈𝐏𝐋𝐈𝐍𝐄 • 𝐔𝐍𝐈𝐓𝐄́ 🟥⬛

        """,
        color=discord.Color.dark_red()
    )

    embed.set_footer(
        text="Gakuran | Code du Clan"
    )

    await ctx.send(embed=embed)


# =====================
# INFOS
# =====================

@bot.command()
async def avatar(ctx, member: discord.Member = None):

    member = member or ctx.author
    await ctx.send(member.avatar.url)


@bot.command()
async def userinfo(ctx, member: discord.Member = None):

    member = member or ctx.author

    embed = discord.Embed(
        title=f"👤 {member}",
        color=discord.Color.dark_red()
    )

    embed.add_field(
        name="ID",
        value=member.id
    )

    await ctx.send(embed=embed)


@bot.command()
async def serverinfo(ctx):

    embed = discord.Embed(
        title=f"⬛ {ctx.guild.name}",
        color=discord.Color.dark_red()
    )

    embed.add_field(
        name="Membres",
        value=ctx.guild.member_count
    )

    await ctx.send(embed=embed)


bot.run(TOKEN)
