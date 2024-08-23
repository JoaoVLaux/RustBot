from discord import app_commands, ui, Interaction
import discord
from discord.ext import commands
from util.__funktion__ import *

import os
import sys

# Defina o ID do canal aqui
CHANNEL_ID = 1247981897942827023  # Substitua pelo ID do canal desejado

# Configurações do bot
current_dir = os.path.dirname(os.path.abspath(__file__))
bot_path = os.path.abspath(sys.argv[0])
bot_folder = os.path.dirname(bot_path)
config_dir = os.path.join(bot_folder, "config", "config.ini")
guild_id = int(read_config(config_dir, "client", "guild_id"))
guild = discord.Object(id=guild_id)

class RemoveRoleModal(ui.Modal, title="/remove_recruta"):
    """
    Modal para inserir o ID da mensagem para remover a role '【RECRUTA】' de quem reagiu.
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
        role_name = "【RECRUTA】"

        # Busque a mensagem pelo ID e no canal especificado
        channel = self.bot.get_channel(CHANNEL_ID)
        try:
            message = await channel.fetch_message(int(self.message_id.value))
        except discord.NotFound:
            await interaction.response.send_message("Mensagem não encontrada. Verifique o ID.", ephemeral=True)
            return

        role = discord.utils.get(interaction.guild.roles, name=role_name)
        if not role:
            await interaction.response.send_message(f"A role '{role_name}' não foi encontrada. Verifique se ela existe.", ephemeral=True)
            return

        embed = discord.Embed(title="Remover Role", color=0xff0000)
        embed.add_field(name="Mensagem ID", value=self.message_id.value, inline=True)
        embed.add_field(name="Role", value=role_name, inline=True)
        embed.set_footer(text="Reaja com 👍 para confirmar ou 👎 para cancelar.")

        view = Confirm_say()
        await interaction.response.send_message(embed=embed, ephemeral=True, view=view)
        await view.wait()

        if view.value is None:
            print('Timed out...')
        elif view.value:
            print('Confirmado...')
            for reaction in message.reactions:
                async for user in reaction.users():
                    if user.bot:
                        continue
                    await user.remove_roles(role)

            await interaction.followup.send(f"Removi a role '{role_name}' de todos que reagiram à mensagem `{self.message_id.value}`.", ephemeral=True)
        else:
            print('Cancelado...')

class Confirm_say(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label='Confirmar', style=discord.ButtonStyle.green)
    async def confirm(self, interaction: Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Confirmando', ephemeral=True)
        self.value = True
        self.stop()

    @discord.ui.button(label='Cancelar', style=discord.ButtonStyle.grey)
    async def cancel(self, interaction: Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Cancelando', ephemeral=True)
        self.value = False
        self.stop()

class RemoveRoleByReaction(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="remove_recruta", description="Remove a '【RECRUTA】' role de usuários que reagiram a uma mensagem específica.")
    async def remove_recruta_modal(self, interaction: Interaction):
        await interaction.response.send_modal(RemoveRoleModal(self.bot))

async def setup(bot: commands.Bot):
    await bot.add_cog(RemoveRoleByReaction(bot), guild=discord.Object(guild_id))
