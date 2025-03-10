
# **AutoEmailBot**

### What is AutoEmailBot?
AutoEmailBot is a Discord bot designed to automate outreach emails for [OVG! Media](https://www.ovgmedia.com/). The bot sends outreach emails to social media content creators, inviting them to collaborate with OVG! Media for paid song promotions and creative partnerships, streamlining communication.

### How does AutoEmailBot work?
AutoEmailBot takes in a CSV file with two columns: one for usernames and the other for email addresses. Using this information, it personalizes and sends outreach emails to the respective content creators. The bot uses various features to make this process efficient, such as email validation, email confirmation, and support for different sender addresses.

### Features
- **Sender Email Address Presets**: Users can select from a list of preset email accounts to send emails from

- **CSV File Parsing**: The bot takes user-uploaded CSV files containing usernames and email addresses, parses the content, and sends emails using the information

- **Email Validation**: The bot regex validates email addresses before attempting to send them

- **Delay Between Emails**: There is a 10 second delay between sending emails to prevent the sender address from being flagged for spam

- **Stop Command**: The stop command (`!stop`) allows the user to cancel the process at any time

- **Dynamic ETA**: During the email sending, a message will provide constant updates on the estimated time remaining

- **HTML Email Formatting**: Users can format email bodies with bold, italic, colored text, and line breaks and the bot automatically appends the selected sender's signature

- **HTML Generated Email Preview**: The bot generates a visual preview of the email body as an image for final confirmation

- **Invalid Email Handling**: Invalid emails are skipped, and a list of these emails is included in the summary report

### Dependencies
- **discord.py**

- **pandas**

- **wkhtmltoimage**

### How to Use AutoEmailBot
1. **Create and Invite a Discord Bot**: Create a Discord bot in the Discord Developer Portal to use to host the script, and invite the bot to a Discord server

2. **Update the Code for Your Use**: In config.py, replace the placeholder `DISCORD_TOKEN` with your bot token, and modify the `EMAIL_PRESETS` and `EMAIL_SIGNATURES` dictionaries to include your sender email credentials and signatures
	- *Note*: Regular email address passwords will not work for this script, you must create an app password to bypass two-factor authentication to ensure the bot functions properly. More information can be found [here](https://support.google.com/accounts/answer/185833?hl=en)

3. **Install Dependencies**: The Discord Python Library and pandas can be installed by running `pip install discord.py pandas` in terminal. wkhtmltoimage will need to be installed via their website [https://wkhtmltopdf.org/](https://wkhtmltopdf.org/)

4. **Run the Script**: Use an IDE/CDE to run the script, turning the bot on

5. **Run the Command**: `!sendemails` is the command to run the bot

6. **Select Sender Email**: Choose a sender email account from the preset options

7. **Upload CSV File**: Upload a CSV file containing usernames and email addresses

8. **Enter Email Subject and Body**: Provide a subject line and email body

9. **Confirmation Dialog**: Confirm the emails to be sent
