from discord.ext import commands
import discord
from config import stop_requested

# stop command
@commands.command(name = "stop")
async def stop(ctx):
    global stop_requested
    stop_requested = True
    embed = discord.Embed(title = "Process stopped by user", description = "", color = discord.Color.red())
    await ctx.send(embed = embed)