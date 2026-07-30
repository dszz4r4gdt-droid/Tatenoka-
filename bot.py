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
# BOUTONS CANDIDATURE
# =====================

class ApplicationButtons(discord.ui.View):

    def __init__(self, applicant):
        super().__init__(timeout=None)
        self.applicant = applicant


    @discord.ui.button(
        label="✅ Accepter",
        style=discord.ButtonStyle.success
    )
    async def accept(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        await self.applicant.send(
            "⬛🟥 **TATENOKAI — CANDIDATURE ACCEPTÉE** 🟥⬛\n\n"
            "Votre candidature RP a été acceptée.\n"
            "Bienvenue au sein de Tatenokai."
        )

        await interaction.response.send_message(
            "✅ Candidature acceptée.",
            ephemeral=True
        )


    @discord.ui.button(
        label="❌ Refuser",
        style=discord.ButtonStyle.danger
    )
    async def refuse(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        await self.applicant.send(
            "⬛🟥 **TATENOKAI — CANDIDATURE REFUSÉE** 🟥⬛\n\n"
            "Votre candidature RP n'a pas été retenue."
        )

        await interaction.response.send_message(
            "❌ Candidature refusée.",
            ephemeral=True
        )


# =====================
# COMMANDES GENERALES
# =====================

@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong !")


@bot.command(name="commands")
async def commands_list(ctx):

    embed = discord.Embed(
        title="⬛🟥 𝐓𝐀𝐓𝐄𝐍𝐎𝐊𝐀𝐈 — COMMANDES 🟥⬛",
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
`!avatar`
`!userinfo`
`!serverinfo`

**🏯 CLAN**

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

    await ctx.send(
        f"🟥 {member} a été expulsé.\nRaison : {reason}"
    )


@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="Aucune raison"):

    await member.ban(reason=reason)

    await ctx.send(
        f"🟥 {member} a été banni.\nRaison : {reason}"
    )


@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, user_id:int):

    user = await bot.fetch_user(user_id)

    await ctx.guild.unban(user)

    await ctx.send(
        f"✅ {user} a été débanni."
    )


@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount:int):

    await ctx.channel.purge(limit=amount+1)

    msg = await ctx.send(
        f"🧹 {amount} messages supprimés."
    )

    await msg.delete(delay=5)


@bot.command()
@commands.has_permissions(manage_messages=True)
async def warn(ctx, member:discord.Member, *, reason="Aucune raison"):

    await ctx.send(
        f"⚠️ {member.mention} a reçu un avertissement.\n"
        f"Raison : {reason}"
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

    await ctx.send(
        f"🔇 {member} a été mute."
    )


@bot.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):

    role = discord.utils.get(
        ctx.guild.roles,
        name="Muted"
    )

    if role:
        await member.remove_roles(role)

    await ctx.send(
        f"🔊 {member} a été unmute."
    )


# =====================
# REGLEMENT TATENOKAI
# =====================

@bot.command()
async def reglement(ctx):

    embed = discord.Embed(
        title="⬛🟥 𝐓𝐀𝐓𝐄𝐍𝐎𝐊𝐀𝐈 🟥⬛\n「 𝐂𝐎𝐃𝐄 𝐃𝐔 𝐂𝐋𝐀𝐍 」",
        description="""

━━━━━━━━━━━━━━━━━━━━━━

🟥 **𝐈𝐃𝐄𝐍𝐓𝐈𝐓𝐄́ 𝐃𝐔 𝐂𝐋𝐀𝐍**

Rejoindre Tatenokai signifie porter son nom,
son symbole et son héritage.

Chaque membre représente le clan par ses actes,
son comportement et sa réputation.

**HONNEUR • DISCIPLINE • UNITÉ**

━━━━━━━━━━━━━━━━━━━━━━

⬜ **𝐂𝐎𝐌𝐏𝐎𝐑𝐓𝐄𝐌𝐄𝐍𝐓**

Chaque membre doit :

⚪ Respecter les membres du clan.
⚪ Respecter la hiérarchie.
⚪ Protéger l'image de Tatenokai.
⚪ Garder une attitude mature.

Interdit :

🔴 Toxicité.
🔴 Provocations inutiles.
🔴 Actions nuisant au clan.

━━━━━━━━━━━━━━━━━━━━━━

⚔️ **𝐑𝐏 𝐃𝐔 𝐂𝐋𝐀𝐍**

Lors des activités RP :

⬛ Respect de l'immersion.
⬛ Fair-play obligatoire.
⬛ Aucun metagaming.
⬛ Aucun powergaming.

La qualité du RP passe avant la victoire.

━━━━━━━━━━━━━━━━━━━━━━

⬛ **𝐇𝐑𝐏**

Les membres doivent :

⚪ Régler les conflits calmement.
⚪ Respecter les autres joueurs.
⚪ Protéger les informations internes.

━━━━━━━━━━━━━━━━━━━━━━

⚖️ **𝐒𝐀𝐍𝐂𝐓𝐈𝐎𝐍𝐒**

⬜ Avertissement

🟥 Suspension

⬛ Expulsion

━━━━━━━━━━━━━━━━━━━━━━

🩸 Porter Tatenokai est un privilège.

⬛🟥 𝐓𝐀𝐓𝐄𝐍𝐎𝐊𝐀𝐈 🟥⬛
        """,
        color=discord.Color.dark_red()
    )

    embed.set_footer(
        text="Tatenokai | Code du Clan"
    )

    await ctx.send(embed=embed)


# =====================
# CANDIDATURE RP
# =====================

@bot.command()
async def apply(ctx):

    user = ctx.author

    questions = [

        "🟥 **1 | ORIGINE DE LA DÉCOUVERTE**\n\nComment avez-vous découvert Tatenokai ?",

        "🟥 **2 | MOTIVATION D’INTÉGRATION**\n\nPourquoi souhaitez-vous rejoindre Tatenokai ?\nExpliquez vos motivations.",

        "🟥 **3 | IDENTITÉ DU PERSONNAGE**\n\nQuel est l’âge de votre personnage Gakuran ?",

        "🟥 **4 | HISTOIRE DU PERSONNAGE**\n\nPrésentez le lore de votre personnage Gakuran.\n(Décrivez son passé, son parcours et les événements importants de sa vie.)",

        "🟥 **5 | ORIGINE DU PERSONNAGE**\n\nQuelle est l’origine de votre personnage Gakuran ?\n(Pays, famille, clan ou milieu.)",

        "🟥 **6 | ART DU COMBAT**\n\nQuel est le style de combat de votre personnage Gakuran ?\n(Décrivez ses techniques et ses spécialités.)"
    ]


    answers = []


    try:

        await user.send(
            "⬛🟥 **𝐓𝐀𝐓𝐄𝐍𝐎𝐊𝐀𝐈 — 𝐃𝐎𝐒𝐒𝐈𝐄𝐑 𝐃’𝐀𝐃𝐌𝐈𝐒𝐒𝐈𝐎𝐍 𝐑𝐏** 🟥⬛\n\n"
            "Répondez sérieusement à chaque question."
        )


        for question in questions:

            await user.send(question)

            response = await bot.wait_for(
                "message",
                timeout=300,
                check=lambda m:
                m.author == user and isinstance(m.channel, discord.DMChannel)
            )

            answers.append(response.content)



        staff = await bot.fetch_user(STAFF_ID)


        embed = discord.Embed(
            title="⬛🟥 Nouvelle candidature Tatenokai 🟥⬛",
            description=f"Candidat : {user}\nID : `{user.id}`",
            color=discord.Color.dark_red()
        )


        for i, answer in enumerate(answers):

            embed.add_field(
                name=f"Réponse {i+1}",
                value=answer[:1024],
                inline=False
            )


        await staff.send(
            embed=embed,
            view=ApplicationButtons(user)
        )


        await user.send(
            "✅ Votre candidature a été envoyée au haut commandement."
        )


    except Exception:

        await user.send(
            "❌ Votre candidature a expiré ou une erreur est survenue."
        )


# =====================
# INFORMATIONS
# =====================

@bot.command()
async def avatar(ctx, member: discord.Member = None):

    member = member or ctx.author

    await ctx.send(
        member.avatar.url
    )


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
        title=f"🏯 {ctx.guild.name}",
        color=discord.Color.dark_red()
    )

    embed.add_field(
        name="Membres",
        value=ctx.guild.member_count
    )

    await ctx.send(embed=embed)



bot.run(TOKEN)
    )
