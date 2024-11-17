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
    await ctx.send("Enter the sender email address:")
    if stop_requested:
        return
    try:
        email_msg = await bot.wait_for('message', check = lambda m: m.author == ctx.author, timeout = 20.0)
    except asyncio.TimeoutError:
        await ctx.send("Timed out waiting for your response, run the command again")
        return
    if stop_requested:
        return
    email_address = email_msg.content

    await ctx.send("Enter the password:")
    if stop_requested:
        return
    try:
        password_msg = await bot.wait_for('message', check = lambda m: m.author == ctx.author, timeout = 20.0)
        await password_msg.delete()
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
        message = await bot.wait_for('message', check = check_file, timeout = 20.0)
    except asyncio.TimeoutError:
        await ctx.send("Timed out waiting for your response, run the command again")
        return
    if stop_requested:
        return
    attachment = message.attachments[0]
    
    # csv download to server
    await attachment.save(attachment.filename)
    file_path = attachment.filename
    
    email_addresses = []
    usernames = []
    try:
        df = pd.read_csv(attachment.filename, header = None)
        usernames = df.iloc[:, 0].dropna().tolist()
        email_addresses = df.iloc[:, 1].dropna().tolist()
    except pd.errors.ParserError:
        await ctx.send("Error parsing the CSV file, check the format and try again")
        return

    # validate email addresses
    invalid_emails = []
    valid_email_addresses = []
    valid_usernames = []
    for username, email in zip(usernames, email_addresses):
        if re.match(r'^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$', email):
            valid_email_addresses.append(email)
            valid_usernames.append(username)
        else:
            invalid_emails.append(email)

    email_addresses = valid_email_addresses
    usernames = valid_usernames
    total_emails = len(email_addresses)

    # ask for and extract email subject
    await ctx.send("Enter the subject of the email:")
    if stop_requested:
        return
    try:
        subject_msg = await bot.wait_for('message', check = lambda m: m.author == ctx.author, timeout = 20.0)
    except asyncio.TimeoutError:
        await ctx.send("Timed out waiting for your response, run the command again")
        return
    if stop_requested:
        return
    subject = subject_msg.content

    # ask for and extract email body
    await ctx.send("Enter the body of the email: (use **bold** for bold text)")
    if stop_requested:
        return
    try:
        body_msg = await bot.wait_for('message', check = lambda m: m.author == ctx.author, timeout = 20.0)
    except asyncio.TimeoutError:
        await ctx.send("Timed out waiting for your response, run the command again")
        return
    if stop_requested:
        return
    body = body_msg.content

    # format body to allow for bold and line breaks
    body_html = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', body)
    body_html = body_html.replace('\n', '<br>')

    # sending emails yipeeee!!!
    sent_count = 0
    loading_message = await ctx.send("Sending emails...")
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(email_address, email_password)

        while sent_count < total_emails:
            for username, email in zip(usernames, email_addresses):
                if stop_requested:
                    return
                msg = MIMEMultipart()
                msg['From'] = email_address
                msg['To'] = email
                msg['Subject'] = f"{subject} [@{username}]"
                msg.attach(MIMEText(body_html, 'html'))
                server.send_message(msg)
                sent_count += 1
                # 5 sec delay between emails to avoid being flagged as spam
                await asyncio.sleep(10)

    await loading_message.delete()

    # summary output
    summary_message = (
        f"Summary:\n"
        f"- Email address used: {email_address}\n"
        f"- Emails sent: {sent_count} of {total_emails}\n"
    )
    if invalid_emails:
        summary_message += f"- Invalid emails skipped: {', '.join(invalid_emails)}\n"
    await ctx.send(summary_message)

    # delete the csv file from server
    try:
        import os
        os.remove(file_path)
    except Exception as e:
        await ctx.send(f"Failed to delete the CSV file: {str(e)}")
    
@bot.command(name = 'stop')
async def stop(ctx):
    global stop_requested
    stop_requested = True
    await ctx.send("Process stopped by user")

bot.run(DISCORD_TOKEN)
