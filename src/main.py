import discord
from discord import File
from discord.ext import commands
import datetime
from easy_pil import Editor, load_image_async, Font
from dotenv import load_dotenv
import os

# Extracting the TOKEN securely

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


# Intents are required to access certain features

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Creating the bot instance

bot = commands.Bot(command_prefix="$", intents=intents)

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
    await log_channel.send(embed=embed_online)
    print("Le bot est connecté.")


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

    background = Editor("Assets\\welcome-back.jpg")
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

bot.run(token=TOKEN)