from discord.ext import commands
import discord
import pandas as pd
import asyncio
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from config import EMAIL_PRESETS, EMAIL_SIGNATURES, stop_requested
from bot_ui import Confirmation, EmailSelection
import subprocess

# stop handler for sendemails process cancellation
async def handle_stop(ctx, message = None, file_path = None):
    if stop_requested:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
        stop_embed = discord.Embed(
            title = "Process stopped by user",
            description = message if message else "The process has been canceled",
            color = discord.Color.red(),
        )
        await ctx.send(embed = stop_embed)
        raise asyncio.CancelledError

# sendemails command
@commands.command(name = "sendemails")
async def send_emails(ctx):
    global stop_requested
    stop_requested = False

    # select sender email from preset options
    embed = discord.Embed(title = "Select a Sender Email",
                          description = "",
                          color = discord.Color.blue())
    view = EmailSelection(ctx)
    await ctx.send(embed = embed, view = view)

    while not view.selected_email:
        await handle_stop(ctx, "Email selection has been canceled")
        await asyncio.sleep(1)

    if not view.selected_email:
        cancel_embed = discord.Embed(
            title = "Timeout, run the command again",
            description = "",
            color = discord.Color.red(),
        )
        await ctx.send(embed = cancel_embed)
        return

    await handle_stop(ctx)

    # retrieve selected email, password, and signature
    email_address = view.selected_email
    email_password = EMAIL_PRESETS[email_address]
    email_signature = EMAIL_SIGNATURES[email_address]

    # user csv upload
    embed = discord.Embed(
        title = "Upload the CSV file containing the usernames and email addresses",
        description = "",
        color = discord.Color.blue())
    await ctx.send(embed = embed)

    while True:
        await handle_stop(ctx, "File upload has been canceled")
        try:
            message = await commands.wait_for(
                "message",
                check = lambda m: m.author == ctx.author and len(m.attachments) > 0,
                timeout = 1.0
            )
            break
        except asyncio.TimeoutError:
            continue

    attachment = message.attachments[0]
    await attachment.save(attachment.filename)
    file_path = attachment.filename

    # parse csv
    try:
        df = pd.read_csv(file_path, header = None)
        usernames = df.iloc[:, 0].dropna().tolist()
        email_addresses = df.iloc[:, 1].dropna().tolist()
    except pd.errors.ParserError:
        error_embed = discord.Embed(
            title = "CSV Parsing Error",
            description = "Error parsing the CSV file, make sure the first column is usernames and the second column is emails",
            color = discord.Color.red())
        await ctx.send(embed = error_embed)
        os.remove(file_path)
        return

    # validate email addresses
    invalid_emails = []
    valid_email_addresses = []
    valid_usernames = []
    for username, email in zip(usernames, email_addresses):
        await handle_stop(ctx, file_path = file_path)
        if re.match(r'^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$', email):
            valid_email_addresses.append(email)
            valid_usernames.append(username)
        else:
            invalid_emails.append(email)

    email_addresses = valid_email_addresses
    usernames = valid_usernames
    total_emails = len(email_addresses)

    await handle_stop(ctx, file_path = file_path)

    # ask for and extract email subject
    embed = discord.Embed(title = "Enter the subject for the email",
                          description = "",
                          color = discord.Color.blue())
    await ctx.send(embed = embed)

    try:
        subject_msg = await commands.wait_for("message",
                                      check = lambda m: m.author == ctx.author,
                                      timeout = 60.0)
        subject = subject_msg.content
        if subject == "!stop":
            stop_embed = discord.Embed(title = "Process stopped by user",
                                   description = "Email subject input canceled",
                                   color = discord.Color.red())
            await ctx.send(embed = stop_embed)
            os.remove(file_path)
            return
    except asyncio.TimeoutError:
        timeout_embed = discord.Embed(title = "Timeout, run the command again",
                                      description = "",
                                      color = discord.Color.red())
        await ctx.send(embed = timeout_embed)
        os.remove(file_path)
        return

    # ask for and extract email body
    embed = discord.Embed(
        title = "Enter the body of the email",
        description = "Use **text** for bold text, *text* for italic text, and red(text)/blue(text)/etc for colored text",
        color = discord.Color.blue())
    await ctx.send(embed = embed)
    
    try:
        body_msg = await commands.wait_for("message",
                                      check = lambda m: m.author == ctx.author,
                                      timeout = 60.0)
        body = body_msg.content
        if body == "!stop":
            stop_embed = discord.Embed(title = "Process stopped by user",
                                   description = "Email body input canceled",
                                   color = discord.Color.red())
            await ctx.send(embed = stop_embed)
            os.remove(file_path)
            return
    except asyncio.TimeoutError:
        timeout_embed = discord.Embed(title = "Timeout, run the command again",
                                      description = "",
                                      color = discord.Color.red())
        await ctx.send(embed = timeout_embed)
        os.remove(file_path)
        return

    # format body to allow for bold, italic, colored text, line breaks, add signature
    body_html = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', body)
    body_html = re.sub(r'\*(.*?)\*', r'<i>\1</i>', body_html)
    body_html = body_html.replace('\n', '<br>')
    body_html += f"<br><br>{email_signature}"
    color_mapping = {
        "red": "Red",
        "orange": "Orange",
        "yellow": "Yellow",
        "green": "Green",
        "blue": "Blue",
        "purple": "Purple",
        "brown": "Brown",
        "grey": "Grey"
    }
    def replace_color(match):
        color = match.group(1)
        return f'<span style = "color:{color_mapping[color]};">{match.group(2)}</span>'
    pattern = r'(' + '|'.join(color_mapping.keys()) + r')\((.*?)\)'
    body_html = re.sub(pattern, replace_color, body_html)

    await handle_stop(ctx, file_path = file_path)

    # generating html screenshot of email body
    print(body_html)
    html_file = "test.html"
    body_formatted = f"""
                    <html>
                        <body>
                            {body_html}
                        </body>
                    </html>
                    """
    with open(html_file, "w", encoding = "utf-8") as file:
        file.write(body_formatted)
    subprocess.run([r"C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe", html_file, "email_preview.png"], check = True)
    file = discord.File("email_preview.png", filename = "email_preview.png")
    embed.set_image(url = f"attachment://email_preview.png")
        
    # confirmation
    embed = discord.Embed(title = "Confirm Email Sending",
                          description = f"**Sender Email:** {email_address}\n"
                          f"**Subject:** {subject} [@username]\n"
                          f"**Total Emails to Send:** {total_emails}",
                          color = discord.Color.green())
    view = Confirmation(ctx, total_emails)
    await ctx.send(embed = embed, view = view, file = file)
    if os.path.exists(html_file):
            os.remove(html_file)
    if os.path.exists("email_preview.png"):    
        os.remove("email_preview.png")
    
    await view.wait()
    await handle_stop(ctx, file_path = file_path)
    if not view.confirmed:
        cancel_embed = discord.Embed(title = "Email sending canceled",
                                     description = "",
                                     color = discord.Color.red())
        await ctx.send(embed = cancel_embed)
        os.remove(file_path)
        return

    if os.path.exists("email_preview.png"):    
        os.remove("email_preview.png")
    
    # sending emails yipeeee!!!
    sent_count = 0
    total_time = total_emails * 10
    estimated_minutes = (total_time // 60) + (1 if total_time % 60 > 0 else 0)
    loading_message = await ctx.send(embed = discord.Embed(
        title = "Sending Emails",
        description = f"Estimated time left: {estimated_minutes} minute(s)",
        color = discord.Color.blue()))

    start_time = asyncio.get_running_loop().time()
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(email_address, email_password)

        try:
            while sent_count < total_emails:
                for username, email in zip(valid_usernames, valid_email_addresses):
                    await handle_stop(ctx, file_path = file_path)
                    msg = MIMEMultipart()
                    msg["From"] = email_address
                    msg["To"] = email
                    msg["Subject"] = f"{subject} [@{username}]"
                    msg.attach(MIMEText(body_html, "html"))
                    server.send_message(msg)
                    sent_count += 1

                    # eta for remaining emails
                    elapsed_time = asyncio.get_running_loop().time() - start_time
                    remaining_time = max(total_time - elapsed_time, 0)
                    remaining_minutes = int(remaining_time // 60) + (
                        1 if remaining_time % 60 > 0 else 0)
                    await loading_message.edit(embed = discord.Embed(
                        title = "Sending Emails",
                        description = f"Estimated time left: {remaining_minutes} minute(s)",
                        color = discord.Color.blue()))

                    # 10 sec delay between emails to avoid being flagged as spam
                    await asyncio.sleep(10)

        except asyncio.CancelledError:
            stop_embed = discord.Embed(
                title = "Process stopped by user",
                description = "Email sending has been canceled",
                color = discord.Color.red(),
            )
            await ctx.send(embed = stop_embed)
            return
        except smtplib.SMTPException as e:
            error_embed = discord.Embed(
                title = "SMTP Error",
                description = f"An error occurred while sending emails: {str(e)}",
                color = discord.Color.red(),
            )
            await ctx.send(embed = error_embed)
            return
        finally:
            await loading_message.delete()

    # summary output
    summary_message = (f"**Sender Email:** {email_address}\n"
                       f"**Emails Sent:** {sent_count} of {total_emails}\n")
    complete_embed = discord.Embed(title = "Emails sent! Here's a summary:",
                                   description = summary_message,
                                   color = discord.Color.green())

    if invalid_emails:
        summary_message += f"**Invalid Emails Skipped:** {', '.join(invalid_emails)}\n"
    await ctx.send(embed = complete_embed)

    # delete the csv file from server
    try:
        os.remove(file_path)
    except Exception as e:
        error_embed = discord.Embed(title = "Failed to delete the CSV file",
                                    description = f"{e}",
                                    color = discord.Color.red())
        os.remove(file_path)
        await ctx.send(embed = error_embed)