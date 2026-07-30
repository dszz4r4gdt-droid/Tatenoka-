import discord
from discord.ext import commands
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


@bot.event
async def on_ready():
    print(f"{bot.user} is online!")
    print("Commands:", [cmd.name for cmd in bot.commands])


# TEST
@bot.command()
async def ping(ctx):
    await ctx.send("Pong !")


# AIDE
@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="Commandes du bot",
        description="""
**Modération**
!kick @user raison
!ban @user raison
!unban ID
!clear nombre
!mute @user
!unmute @user
!warn @user raison

**Utilitaires**
!ping
!userinfo @user
!avatar @user
!serverinfo

**Serveur**
!reglement
        """,
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)


# KICK
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="Aucune raison"):
    await member.kick(reason=reason)
    await ctx.send(f"✅ {member} a été expulsé. Raison : {reason}")


# BAN
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="Aucune raison"):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 {member} a été banni. Raison : {reason}")


# UNBAN
@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, user_id: int):
    user = await bot.fetch_user(user_id)
    await ctx.guild.unban(user)
    await ctx.send(f"✅ {user} a été débanni.")


# CLEAR
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"🧹 {amount} messages supprimés.")


# MUTE
@bot.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")

    if role is None:
        role = await ctx.guild.create_role(name="Muted")

    await member.add_roles(role)
    await ctx.send(f"🔇 {member} est mute.")


# UNMUTE
@bot.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")

    if role:
        await member.remove_roles(role)

    await ctx.send(f"🔊 {member} est unmute.")


# WARN
@bot.command()
@commands.has_permissions(manage_messages=True)
async def warn(ctx, member: discord.Member, *, reason="Aucune raison"):
    await ctx.send(
        f"⚠️ {member.mention} a reçu un avertissement.\nRaison : {reason}"
    )


# REGLEMENT
@bot.command()
async def reglement(ctx):

    embed = discord.Embed(
        title="📜 Règlement du serveur",
        description="""
**1. Respect**
Respectez tous les membres.

**2. Aucun spam**
Le spam, flood et ping abusif sont interdits.

**3. Aucun contenu interdit**
Pas d'insultes graves, haine ou contenu dangereux.

**4. Utilisation des salons**
Utilisez chaque salon correctement.

**5. Équipe du serveur**
Les décisions du staff doivent être respectées.
        """,
        color=discord.Color.gold()
    )

    embed.set_footer(text="Merci de respecter le règlement.")

    await ctx.send(embed=embed)


# USER INFO
@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author

    embed = discord.Embed(
        title=f"Informations de {member}",
        color=discord.Color.green()
    )

    embed.add_field(name="ID", value=member.id)
    embed.add_field(name="Compte créé", value=member.created_at)

    embed.set_thumbnail(url=member.avatar.url)

    await ctx.send(embed=embed)


# AVATAR
@bot.command()
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    await ctx.send(member.avatar.url)


# SERVER INFO
@bot.command()
async def serverinfo(ctx):

    embed = discord.Embed(
        title=ctx.guild.name,
        color=discord.Color.purple()
    )

    embed.add_field(
        name="Membres",
        value=ctx.guild.member_count
    )

    embed.add_field(
        name="Créé le",
        value=ctx.guild.created_at
    )

    await ctx.send(embed=embed)


bot.run(TOKEN)
