import discord

# confirmation for emails
class Confirmation(discord.ui.View):
    def __init__(self, ctx, total_emails):
        super().__init__(timeout = 60)
        self.ctx = ctx
        self.total_emails = total_emails
        self.confirmed = False

    # confirm button
    @discord.ui.button(label = "Confirm", style = discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.ctx.author:
            self.confirmed = True
            await interaction.response.send_message("Confirmed! Sending emails...", ephemeral = True)
            self.stop()
        else:
            await interaction.response.send_message("Not confirmed", ephemeral = True)

    # cancel button
    @discord.ui.button(label = "Cancel", style = discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.ctx.author:
            await interaction.response.send_message("Canceled! Run the command again", ephemeral = True)
            self.stop()
        else:
            await interaction.response.send_message("Not canceled", ephemeral = True)