import discord

# bot token
DISCORD_TOKEN = "insert your discord bot token here"

# bot intents
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True
intents.members = True

# stop command state
stop_requested = False

# preset sender email addresses and passwords
EMAIL_PRESETS = {
    "email1@gmail.com": "password1",
    "email2@gmail.com": "password2",
}

# preset sender email signatures
EMAIL_SIGNATURES = {
    "email1@gmail.com": """
<br>
<span style="color: #ababab;">--</span><br>
<span style="color: #ababab;">John Smith | Marketing Manager</span><br>
<span style="color: #ababab;">Example Corp</span><br>
<a href="https://www.example.com" style="color: #002cee;">https://www.example.com</a><br>
<img src="link:example_logo" alt="Example-Logo" width="150">
""",
    "email2@gmail.com": """
<br>
<span style="color: #ababab;">--</span><br>
<span style="color: #ababab;">Jane Doe | Marketing Manager</span><br>
<span style="color: #ababab;">Example Corp</span><br>
<a href="https://www.example.com" style="color: #002cee;">https://www.example.com</a><br>
<img src="link:example_logo" alt="Example-Logo" width="150">
""",
}
