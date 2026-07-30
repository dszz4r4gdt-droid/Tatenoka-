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
# COMMANDES GENERALES
# =====================

@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong !")


@bot.command()
async def commands_list(ctx):
    embed = discord.Embed(
        title="📚 Commandes du bot",
        description="""
**🛡️ Modération**
`!kick @user raison`
`!ban @user raison`
`!unban ID`
`!clear nombre`
`!mute @user`
`!unmute @user`
`!warn @user raison`

**⚙️ Utilitaires**
`!ping`
`!userinfo`
`!avatar`
`!serverinfo`

**📜 Serveur**
`!reglement`

**ℹ️ Informations**
`!commands`
        """,
        color=discord.Color.blue()
    )

    await ctx.send(embed=embed)


# =====================
# MODERATION
# =====================

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="Aucune raison"):
    await member.kick(reason=reason)
    await ctx.send(f"👢 {member} a été expulsé.\nRaison : {reason}")


@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="Aucune raison"):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 {member} a été banni.\nRaison : {reason}")


@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, user_id: int):

    user = await bot.fetch_user(user_id)

    await ctx.guild.unban(user)

    await ctx.send(f"✅ {user} a été débanni.")


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

    await ctx.send(f"🔇 {member} a été mute.")


@bot.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):

    role = discord.utils.get(
        ctx.guild.roles,
        name="Muted"
    )

    if role:
        await member.remove_roles(role)

    await ctx.send(f"🔊 {member} a été unmute.")


@bot.command()
@commands.has_permissions(manage_messages=True)
async def warn(ctx, member: discord.Member, *, reason="Aucune raison"):

    await ctx.send(
        f"⚠️ {member.mention} a reçu un avertissement.\n"
        f"Raison : {reason}"
    )


# =====================
# REGLEMENT
# =====================

@bot.command()
async def reglement(ctx):

    embed = discord.Embed(
        title="📜 Règlement du serveur",
        description="""
**1 | Respect**
Respect obligatoire envers tous les membres.

**2 | Spam**
Le spam, flood et ping abusif sont interdits.

**3 | Contenu interdit**
Aucun contenu haineux, dangereux ou illégal.

**4 | Salons**
Utilisez chaque salon correctement.

**5 | Staff**
Les décisions du staff doivent être respectées.

**6 | Sanctions**
Le non-respect du règlement peut entraîner une sanction.
        """,
        color=discord.Color.gold()
    )

    embed.set_footer(
        text="Merci de respecter le règlement."
    )

    await ctx.send(embed=embed)


# =====================
# INFORMATIONS
# =====================

@bot.command()
async def userinfo(ctx, member: discord.Member = None):

    member = member or ctx.author

    embed = discord.Embed(
        title=f"👤 {member}",
        color=discord.Color.green()
    )

    embed.add_field(
        name="ID",
        value=member.id
    )

    embed.add_field(
        name="Compte créé",
        value=member.created_at.strftime("%d/%m/%Y")
    )

    await ctx.send(embed=embed)


@bot.command()
async def avatar(ctx, member: discord.Member = None):

    member = member or ctx.author

    await ctx.send(member.avatar.url)


@bot.command()
async def serverinfo(ctx):

    embed = discord.Embed(
        title=f"🏰 {ctx.guild.name}",
        color=discord.Color.purple()
    )

    embed.add_field(
        name="Membres",
        value=ctx.guild.member_count
    )

    embed.add_field(
        name="Serveur créé",
        value=ctx.guild.created_at.strftime("%d/%m/%Y")
    )

    await ctx.send(embed=embed)


bot.run(TOKEN)
