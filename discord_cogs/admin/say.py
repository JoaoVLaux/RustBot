from discord import app_commands, ui, Interaction
import discord
from discord.ext import commands
from util.__funktion__ import *

import os
import sys

# Get the current directory of the script file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the absolute path of the script itself
bot_path = os.path.abspath(sys.argv[0])

# Get the directory containing the script
bot_folder = os.path.dirname(bot_path)

# Construct the path to the config.ini file relative to the current directory
config_dir = os.path.join(bot_folder, "config", "config.ini")

# Read the guild_id from the config.ini file
guild_id = int(read_config(config_dir, "client", "guild_id"))

# Create a discord Object representing the guild using the obtained guild_id
guild = discord.Object(id=guild_id)

class bot_say(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        """
        Constructor for the BotSay cog.
        """
        self.bot = bot

    @app_commands.command(name="say", description="Envia uma embed para um canal de destino")
    async def Bot_send_modal(self, interaction: Interaction):
        """
        Sends a modal input to the user.
        """
        await interaction.response.send_modal(modal_input_say(self.bot))

class modal_input_say(ui.Modal, title="/say"):
    """
    Custom modal input class for sending an embed to a specified channel.
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()

    say_channel_id = ui.TextInput(
        label="Channel ID para mandar:",
        style=discord.TextStyle.short,
        placeholder="Channel ID",
        required=True,
        max_length=None
    )
    
    say_title = ui.TextInput(
        label="Embed Title:",
        style=discord.TextStyle.short,
        placeholder="Embed title",
        required=True, 
        max_length=None
    )
    
    say_text = ui.TextInput(
        label="Embed Texto:",
        style=discord.TextStyle.long,
        placeholder="Texto",
        required=True,
        max_length=None
    )

    async def on_submit(self, interaction: Interaction):
        """
        Callback method triggered when the user submits the modal form.
        """
        guild = interaction.guild
        embed = discord.Embed(title=" ", color=0xffffff)
        embed.set_author(name=guild)
        embed.add_field(name=self.say_title.value, value=self.say_text.value, inline=True)

        # Add emojis to the embed
        emoji1 = "👍"  # Replace with your first emoji
        embed.add_field(name="Reaja com:", value=f"{emoji1} para confirmar", inline=False)

        view = Confirm_say()

        # Sends the initial embed and waits for the user to confirm or cancel
        await interaction.response.send_message(embed=embed, ephemeral=True, view=view)
        await view.wait()

        if view.value is None:
            print(f'Timed out...')
        elif view.value:
            print(f'Confirmado...')
            say_channel_id = int(self.say_channel_id.value)
            channel = self.bot.get_channel(say_channel_id)
            if channel:
                # Send the embed to the specified channel and add reaction after sending
                sent_message = await channel.send(embed=embed)
                await sent_message.add_reaction(emoji1)
            else:
                await interaction.followup.send("Não consegui encontrar o canal. Verifique o ID do canal.", ephemeral=True)
        else:
            print(f'Cancelado...')

class Confirm_say(discord.ui.View):
    """
    Custom view class for confirming or cancelling an action.
    """
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label='Confirmar', style=discord.ButtonStyle.green)
    async def confirm(self, interaction: Interaction, button: discord.ui.Button):
        """
        Sets the value to True and stops the View from listening to more input.
        """
        await interaction.response.send_message('Confirmando', ephemeral=True)
        self.value = True
        self.stop()

    @discord.ui.button(label='Cancelar', style=discord.ButtonStyle.grey)
    async def cancel(self, interaction: Interaction, button: discord.ui.Button):
        """
        Sets the value to False and stops the View from listening to more input.
        """
        await interaction.response.send_message('Cancelando', ephemeral=True)
        self.value = False
        self.stop()

class ReactionRole(commands.Cog):
    """
    Custom cog for handling reaction roles.
    """
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        """
        Assigns a role to a user when they react with a specific emoji.
        """
        if user.bot:
            return
        
        # Define the emoji-role mapping
        emoji_role_mapping = {
            "👍":"【RECRUTA】",  
        }

        role_name = emoji_role_mapping.get(reaction.emoji)
        if role_name:
            role = discord.utils.get(user.guild.roles, name=role_name)
            if role:
                await user.add_roles(role)

class RemoveRoleModal(ui.Modal, title="/remove_recruta"):
    """
    Custom modal input class for removing the '【RECRUTA】' role from users who reacted to a specified message.
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()

    message_id = ui.TextInput(
        label="Message ID:",
        style=discord.TextStyle.short,
        placeholder="ID da mensagem",
        required=True,
        max_length=None
    )

    async def on_submit(self, interaction: Interaction):
        """
        Callback method triggered when the user submits the modal form.
        """
        # Define the role name as '【RECRUTA】'
        role_name = "【RECRUTA】"
        
        # Get the message by its ID
        channel = interaction.channel
        try:
            message = await channel.fetch_message(int(self.message_id.value))
        except discord.NotFound:
            await interaction.response.send_message("Mensagem não encontrada. Verifique o ID.", ephemeral=True)
            return

        # Get the role object by its name
        role = discord.utils.get(interaction.guild.roles, name=role_name)
        if not role:
            await interaction.response.send_message(f"A role '{role_name}' não foi encontrada. Verifique se ela existe.", ephemeral=True)
            return

        # Create an embed to confirm the action
        embed = discord.Embed(title="Remover Role", color=0xff0000)
        embed.add_field(name="Mensagem ID", value=self.message_id.value, inline=True)
        embed.add_field(name="Role", value=role_name, inline=True)
        embed.set_footer(text="Reaja com 👍 para confirmar ou 👎 para cancelar.")

        # Send confirmation message with buttons
        view = Confirm_say()
        await interaction.response.send_message(embed=embed, ephemeral=True, view=view)
        await view.wait()

        if view.value is None:
            print(f'Timed out...')
        elif view.value:
            print(f'Confirmado...')
            # Iterate over all reactions on the message
            for reaction in message.reactions:
                async for user in reaction.users():
                    if user.bot:
                        continue
                    await user.remove_roles(role)

            await interaction.followup.send(f"Removi a role '{role_name}' de todos que reagiram à mensagem `{self.message_id.value}`.", ephemeral=True)
        else:
            print(f'Cancelado...')


async def setup(bot: commands.Bot):
    """
    Setup function for adding the bot_say, ReactionRole, and RemoveRoleByReaction cogs to the Discord bot.
    """
    await bot.add_cog(bot_say(bot), guild=discord.Object(guild_id))
    await bot.add_cog(ReactionRole(bot))
