import discord
from discord.ext import commands
import datetime
import os

# Extracting the TOKEN securely

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


# Intents are required to access certain features

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Creating the bot instance

bot = commands.Bot(command_prefix="lux$", intents=intents)

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
    print("Le bot est connecté.")


bot.run(token=TOKEN)