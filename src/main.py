import discord
from discord import File, Intents
from discord.ext import commands, tasks
from discord import app_commands
import datetime
from easy_pil import Editor, load_image_async, Font
from dotenv import load_dotenv
import os
import asyncio

# Extracting the TOKEN securely

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Variables for better teminal logs (ANSI)

RESET = "\033[0m"
BOLD = "\033[1m"
GRAY = "\033[90m"
BLUE = "\033[34m"
PURPLE = "\033[35m"
GREEN = "\033[32m"
YELLOW = "\033[33m"

current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Creating the bot instance

bot = commands.Bot(command_prefix="lux$", intents=discord.Intents.all())

@bot.event # online bot
async def on_ready():
    """
    This event triggers when the bot is ready and has connected to Discord.
    """
    # Get in a specific LOG channel
    log_channel = bot.get_channel(1109456096407601182)
    embed_online=discord.Embed(
        title="Log Utahime",
        description=f"Le bot est en ligne en tant que {bot.user} (ID : {bot.user.id}).",
        color=0xFF5733,
        timestamp=datetime.datetime.now()
        )
#    await log_channel.send(embed=embed_online)
    print(f"{BOLD}{GRAY}{current_time}{RESET} {BOLD}{BLUE}ON_READY{RESET} Bot is ready.")
    try:
        synced_commands = await bot.tree.sync()
        print(f"Synced {len(synced_commands)} commands.")
    except Exception as e:
        print("An error with syncing application commands has occured : ", e)


@bot.event # welcome message
async def on_member_join(member):
    """
    This event sends a message to welcome a new member
    """
    #image
    bg_width = 735 # image dimensions
    bg_height = 305 # image dimensions
    profile_size = (150, 150) # avatar dimensions

    x = (bg_width - profile_size[0]) // 2 # coordinates calcul
    y = (bg_height - profile_size[1]) // 2 # coordinates calcul

    base_path = os.getcwd()  # Use the current working directory
    image_path = os.path.join(base_path, 'src', "Assets", "welcome-back.jpg")

    try:
        background = Editor(image_path)
    except FileNotFoundError:
        print(f"Image not found at path: {image_path}")
        return
    
    profile_image = await load_image_async(str(member.avatar.url))
    profile = Editor(profile_image).resize((150, 150)).circle_image()
    poppins = Font.poppins(size=50, variant="bold")
    poppins_small = Font.poppins(size=50, variant="light")
    background.paste(profile, (x, y))
    background.ellipse((x, y), 150, 150, outline="white", stroke_width=5)
    
    file = File(fp=background.image_bytes, filename="pic1.jpg")
    #channels
    log_channel = bot.get_channel(1109456096407601182)
    channel = bot.get_channel(1108062993574535190)
    #embeds
    if channel is not None:
        embed_welcome=discord.Embed(
            title="Bienvenue {} !".format(member),
            description="Bienvenue à toi le frérot {} ! Je t'invite à aller lire le règlement du serveur, ensuite tu pourras discuter aves les  gens. Fais toi plaisir gros !".format(member.mention),
            color=0xFF5733,
            timestamp=datetime.datetime.now()
        )
        embed_log_welcome=discord.Embed(
            title="Log Nouveau Membre",
            description="{} vient de rejoindre le serveur.".format(member.mention),
            color=0xFF5733,
            timestamp=datetime.datetime.now()
        )
        embed_welcome.set_image(url="attachment://pic1.jpg") # attach the image to the embed
        # sending msgs and adding roles
        await channel.send(embed=embed_welcome, file=file) # sends the welcome message
        await log_channel.send(embed=embed_log_welcome) # sends the log
        role = member.guild.get_role(1108352863425544292)
        if role is not None:
            await member.add_roles(role) # adds member's role
        print(f"{member} a rejoins")
    else:
        print("Channel not found")

# -------- MODERATION --------

@bot.tree.command(name="ban", description="Bannir un utilisateur pour une durée indéterminée. Ne pas confondre avec la commande /tribunal.")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, utilisateur: discord.Member, raison: str, durée: int = None):
    log_channel = bot.get_channel(1109456096407601182)
    # Embeds
    ban_time_embed = discord.Embed( # Embed if duration
        title="{} bannni.".format(utilisateur),
        description=f"Pour une durée de {durée} minutes, l'utilisateur {utilisateur} vient d'être banni par {interaction.user} pour : {raison}",
        color=0xFF2333,
        timestamp=datetime.datetime.now()
    )

    ban_embed = discord.Embed( # Embed if no duration
        title="{} banni.".format(utilisateur),
        description=f"Pour une durée indéterminée, l'utilisateur {utilisateur} vient d'être banni par {interaction.user} pour : {raison}",
        color=0xFF2333,
        timestamp=datetime.datetime.now()
    )

    perm_embed = discord.Embed( # Embed if no permissions
        title="Erreur de permissions.",
        description=f"Impossible de bannir {utilisateur}, je n'ai pas les permissions.",
        color=0xFF2333,
        timestamp=datetime.datetime.now()
    )

    error_embed = discord.Embed( # Embed if other error
        title="Erreur inconnue",
        description=f"Une erreur s'est produite lors de la tentative de bannissement.",
        color=0xFF2333,
        timestamp=datetime.datetime.now()
    )

    ban_log = discord.Embed( # Log embed
        title="Ban Log",
        description=f"Auteur : {interaction.user};\nUtilisateur : {utilisateur};\nRaison : {raison};\Durée : {durée}.",
        color=0xFF2333,
        timestamp=datetime.datetime.now()
    )       
    # ------
    try:
        await utilisateur.ban(reason=raison)
        if durée:
            await interaction.response.send_message(embed=ban_time_embed)
            await log_channel.send(ban_log)
            await asyncio.sleep(durée * 60)
            await utilisateur.unban(reason="Fin du temps de bannissement entré.")
            print('{} banned'.format(utilisateur))
        else:
            await interaction.response.send_message(embed=ban_embed)
    except discord.Forbidden:
        await interaction.response.send_message(embed=perm_embed)
    except discord.HTTPException:
        await interaction.response.send_message(error_embed)

@tasks.loop(seconds=60)
async def unban_task(user: discord.User, guild: discord.Guild):
    await guild.unban(user, reason="Fin de la durée de bannissement.")


@bot.tree.command(name="kick", description="Kick un utilisateur. Il pourra revenir avec une invitation.")
@app_commands.checks.has_permissions(ban_members=True)
async def kick(interaction: discord.Interaction, utilisateur: discord.Member, raison: str):
    log_channel = bot.get_channel(1109456096407601182)
    # Embeds
    kick_embed = discord.Embed( # Embed kick
        title="{} banni.".format(utilisateur),
        description=f"L'utilisateur {utilisateur} vient d'être kick par {interaction.user} pour : {raison}. Il pourra revenir avec une invitation.",
        color=0xFF2333,
        timestamp=datetime.datetime.now()
    )

    perm_embed = discord.Embed( # Embed if no permissions
        title="Erreur de permissions.",
        description=f"Impossible de kick {utilisateur}, je n'ai pas les permissions.",
        color=0xFF2333,
        timestamp=datetime.datetime.now()
    )

    error_embed = discord.Embed( # Embed if other error
        title="Erreur inconnue",
        description=f"Une erreur s'est produite lors de la tentative de kick.",
        color=0xFF2333,
        timestamp=datetime.datetime.now()
    )    

    kick_log = discord.Embed( # Log embed
        title="Kick Log",
        description=f"Auteur : {interaction.user};\nUtilisateur : {utilisateur};\nRaison : {raison}.",
        color=0xFF2333,
        timestamp=datetime.datetime.now()
    )
    # ------
    try:
        await utilisateur.kick(reason=raison)
        await interaction.response.send_message(embed=kick_embed)
        await log_channel.send(embed=kick_log)
        print('{} kicked.'.format(utilisateur))
    except discord.Forbidden:
        await interaction.response.send_message(perm_embed)
    except discord.HTTPException:
        await interaction.response.send_message(error_embed)

@bot.tree.command(name="mute", description="Mute un utilisateur pendant un certain temps.")
@app_commands.checks.has_permissions(mute_members=True)
async def mute(interaction: discord.Interaction, utilisateur: discord.Member, raison: str, durée: int):
    # Embeds
    timeout_time_embed = discord.Embed(
        title="Utilisateur Muté",
        description=f"L'utilisateur {utilisateur.mention} a été muté par {interaction.user.mention} pour {durée} minute(s).",
        color=0xFF2333,
        timestamp=datetime.datetime.now()
    )
    timeout_time_embed.add_field(name="Raison", value=raison, inline=False)
    timeout_time_embed.set_footer(text=f"Demandé par {interaction.user}", icon_url=interaction.user.avatar.url)


    timeout_log_embed = discord.Embed(
        title="Mute Log",
        color=0xFF2333,
        timestamp=datetime.datetime.now()
    )
    timeout_log_embed.add_field(name="Auteur", value=interaction.user.mention, inline=True)
    timeout_log_embed.add_field(name="Utilisateur", value=utilisateur.mention, inline=True)
    timeout_log_embed.add_field(name="Durée", value=f"{durée} minute(s)", inline=True)
    timeout_log_embed.add_field(name="Raison", value=raison, inline=False)
    timeout_log_embed.set_footer(text="Mute Log", icon_url=interaction.guild.icon.url if interaction.guild.icon else None)

    # ------
    log_channel = bot.get_channel(1109456096407601182)
    timeout_duration = datetime.timedelta(minutes = durée)
    try:
        await utilisateur.timeout(timeout_duration)
        await interaction.response.send_message(embed=timeout_time_embed)
        await log_channel.send(embed=timeout_log_embed)
        print(f"{BOLD}{GRAY}{current_time}{RESET} {BOLD}{YELLOW}MUTE{RESET} {PURPLE}{utilisateur}{RESET} muted by {PURPLE}{interaction.user}{RESET} Duration: {durée} Reason: {raison}")
        await asyncio.sleep(durée * 60)
        await utilisateur.timeout(None)
        print("{} unmuted.".format(utilisateur))
    except discord.Forbidden:
        await interaction.response.send_message('test perm')
    except discord.HTTPException as e:
        await interaction.response.send_message('test autre erreur ', e)

bot.run(token=TOKEN)