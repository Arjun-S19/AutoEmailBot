
# **AutoEmailBot**

### What is AutoEmailBot?
AutoEmailBot is a Discord bot designed to automate outreach emails for [OVG! Media](https://www.ovgmedia.com/). The bot sends outreach emails to social media content creators, inviting them to collaborate with OVG! Media for paid song promotions and creative partnerships. It is an internal tool that streamlines communication efforts.

### How does AutoEmailBot work?
AutoEmailBot takes in a CSV file with two columns: one for usernames and the other for email addresses. Using this information, it personalizes and sends outreach emails to the respective content creators. The bot uses various features to make this process efficient, such as email validation, email confirmation, and support for different sender addresses.

### Features
- **Email Personalization**: The bot personalizes each email by appending the username of the recipient to the subject line

- **Sender Email Address Presets**: Users can select from a list of preset email accounts to send emails from

- **CSV File Parsing**: The bot takes user-uploaded CSV files containing usernames and email addresses, parses the content, and sends emails using the information

- **Email Validation**: The bot regex validates email addresses before attempting to send them

- **Email Sending Confirmation**: A confirmation dialog is created at the end to minimize the risk of email errors

- **Delay Between Emails**: There is a 10 second delay between sending emails to prevent the sender address from being flagged for spam

- **Stop Command**: The stop command (`!stop`) allows the user to cancel the process at any time

- **Email Sending ETA**: During the email sending, a message will provide constant updates on the estimated time remaining

### Libraries Used
- **discord.py**: Used for building the Discord bot and interacting with Discord's API to create the commands and bot GUI

- **pandas**: Used for parsing information from CSV files

- **smtplib**: Used for sending emails through SMTP, connecting to Gmail's SMTP server

- **email.mime**: Used to format emails with HTML

- **asyncio**: Used for asynchronous operations, such as awaiting user input and delaying email sending

### How to Use AutoEmailBot
1. **Create and Invite a Discord Bot**: Create a Discord bot in the Discord Developer Portal to use to host the script, and invite the bot to a Discord server

2. **Update the Code for Your Use**: Replace the placeholder in `DISCORD_TOKEN` with your bot token, and modify the `EMAIL_PRESETS` and `EMAIL_SIGNATURES` dictionaries to include your sender email credentials and signatures
	- *Note*: Regular email address passwords will not work for this script. You must create an app password to bypass two-factor authentication to ensure the bot functions properly. More information can be found [here](https://support.google.com/accounts/answer/185833?hl=en).

3. **Run the Script**: Use an IDE/CDE to run the script, turning the bot on

4. **Run the Command**: `!sendemails` is the command to run the bot

5. **Select Sender Email**: Choose a sender email account from the preset options

6. **Upload CSV File**: Upload a CSV file containing usernames and email addresses

7. **Enter Email Subject and Body**: Provide a subject line and email body

8. **Confirmation Dialog**: Confirm the emails to be sent
