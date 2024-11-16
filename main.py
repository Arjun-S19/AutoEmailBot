import discord
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from discord.ext import commands
import asyncio
import re

# bot token
DISCORD_TOKEN = "insert discord bot token here"

# command prefix
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True
intents.members = True  
bot = commands.Bot(command_prefix = "!", intents = intents)

stop_requested = False

@bot.event
async def on_ready():
    print(f'{bot.user} is up n running chief, email away!')

# email command
@bot.command(name = 'sendemails')
async def send_emails(ctx):
    global stop_requested
    stop_requested = False

    # ask for email and password for the sender account
    await ctx.send("Enter the email address you want to use to send the emails:")
    if stop_requested:
        return
    try:
        email_msg = await bot.wait_for('message', check = lambda m: m.author == ctx.author, timeout = 10.0)
    except asyncio.TimeoutError:
        await ctx.send("Timed out waiting for your response, run the command again")
        return
    if stop_requested:
        return
    email_address = email_msg.content

    await ctx.send("Enter the password for the email address:")
    if stop_requested:
        return
    try:
        password_msg = await bot.wait_for('message', check = lambda m: m.author == ctx.author, timeout = 10.0)
    except asyncio.TimeoutError:
        await ctx.send("Timed out waiting for your response, run the command again")
        return
    if stop_requested:
        return
    email_password = password_msg.content

    # user csv upload
    await ctx.send("Upload the CSV file containing the email addresses")
    if stop_requested:
        return

    def check_file(message):
        return message.author == ctx.author and len(message.attachments) > 0

    try:
        message = await bot.wait_for('message', check = check_file, timeout = 10.0)
    except asyncio.TimeoutError:
        await ctx.send("Timed out waiting for your response, run the command again")
        return
    if stop_requested:
        return
    attachment = message.attachments[0]
    
    # csv download to server
    await attachment.save(attachment.filename)
    
    email_addresses = []
    try:
        df = pd.read_csv(attachment.filename, header = None)
        # case 1: no header row
        if "@" not in str(df.iloc[0, 0]):
            email_addresses = df.iloc[1:, 0].dropna().tolist()
        # case 2: has header row
        else:
            email_addresses = df.iloc[:, 0].dropna().tolist()
    except pd.errors.ParserError:
        await ctx.send("Error parsing the CSV file, check the format and try again")
        return

    # validate email addresses
    invalid_emails = []
    valid_email_addresses = []
    for email in email_addresses:
        if re.match(r'^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$', email):
            valid_email_addresses.append(email)
        else:
            invalid_emails.append(email)

    email_addresses = valid_email_addresses
    total_emails = len(email_addresses)

    # ask for and extract email subject
    await ctx.send("Enter the subject of the email:")
    if stop_requested:
        return
    try:
        subject_msg = await bot.wait_for('message', check = lambda m: m.author == ctx.author, timeout = 10.0)
    except asyncio.TimeoutError:
        await ctx.send("Timed out waiting for your response, run the command again")
        return
    if stop_requested:
        return
    subject = subject_msg.content

    # ask for and extract email body
    await ctx.send("Enter the body of the email:")
    if stop_requested:
        return
    try:
        body_msg = await bot.wait_for('message', check = lambda m: m.author == ctx.author, timeout = 10.0)
    except asyncio.TimeoutError:
        await ctx.send("Timed out waiting for your response, run the command again")
        return
    if stop_requested:
        return
    body = body_msg.content

    # sending emails yipeeee!!!
    sent_count = 0
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(email_address, email_password)

        for email in email_addresses:
            # 5 sec delay in between emails to avoid being flagged as spam
            if stop_requested:
                return
            await asyncio.sleep(5)
            msg = MIMEMultipart()
            msg['From'] = email_address
            msg['To'] = email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            server.send_message(msg)
            sent_count += 1

    await ctx.send(f"Emails successfully sent to {sent_count} of {total_emails} recipients!")
    
    # output invalid emails if any
    if invalid_emails:
        await ctx.send(f"The following email addresses were invalid and skipped: {', '.join(invalid_emails)}")

@bot.command(name = 'stop')
async def stop(ctx):
    global stop_requested
    stop_requested = True
    await ctx.send("Process stopped by user")

bot.run(DISCORD_TOKEN)
