import discord
from discord.ext import commands
from config import DISCORD_TOKEN, intents
from bot_commands.sendemails import send_emails
from bot_commands.stop import stop

# command prefix
bot = commands.Bot(command_prefix = "!", intents = intents)

bot.add_command(send_emails)
bot.add_command(stop)

@bot.event
async def on_ready():
    print(f"{bot.user} is up n running chief, email away!")

bot.run(DISCORD_TOKEN)