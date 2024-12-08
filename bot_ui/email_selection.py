import discord
from config import EMAIL_PRESETS

# dropdown for selecting a sender email
class EmailSelection(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout = 60)
        self.ctx = ctx
        self.selected_email = None

    @discord.ui.select(
        placeholder = "-",
        options=[
            discord.SelectOption(label = email, description = "") for email in EMAIL_PRESETS.keys()
        ],
    )
    async def select_email(self, interaction: discord.Interaction, select: discord.ui.Select):
        if interaction.user == self.ctx.author:
            self.selected_email = select.values[0]
            await interaction.response.send_message(f"Selected email: {self.selected_email}", ephemeral = True)
            self.stop()
        else:
            await interaction.response.send_message("You are not authorized to select this email", ephemeral = True)
