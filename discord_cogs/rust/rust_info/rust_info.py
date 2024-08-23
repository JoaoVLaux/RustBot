"""Documentação completa em: https://github.com/NapoII/Discord_Rust_Team_bot
-----------------------------------------------
Este COG é para incorporar informações de ajuda para Rust.
exemplo: códigos CCTV
------------------------------------------------
"""

from discord import app_commands

from util.__funktion__ import *
from util.__my_imge_path__ import *
img_url = my_image_url()
# obtém o caminho do diretório atual
current_dir = os.path.dirname(os.path.abspath(__file__))
bot_path = os.path.abspath(sys.argv[0])
bot_folder = os.path.dirname(bot_path)
# construa o caminho para o arquivo config.ini relativo ao diretório atual
config_dir = os.path.join(bot_folder, "config", "config.ini")

cctv_codes_json_dir = os.path.join(bot_folder, "config", "json", "cctv_codes.json")
price_list_json_dir = os.path.join(bot_folder, "config", "json", "price_list.json")
must_have_binds_json_dir = os.path.join(bot_folder, "config", "json", "must_have_binds.json")
json_rust_help_commands_data_dir = os.path.join(bot_folder, "config", "json", "rust_help_commands.json")

rust_help_commands_jason_data = read_json_file(json_rust_help_commands_data_dir)
rust_help_commands = [re.sub(r'\{[^}]*\}', '', entry["command"].replace("```", ""))
                      for entry in rust_help_commands_jason_data]

sec_to_delta = 6*60

guild_id = read_config(config_dir, "client", "guild_id")
if guild_id is None:
    guild_id = 1
guild_id = int(guild_id)

guild = discord.Object(id=guild_id)

rust_info_channel_id = read_config(config_dir, "channels", "rust_info_channel_id")
if rust_info_channel_id is None:
    rust_info_channel_id = 1
rust_info_channel_id = int(rust_info_channel_id)


class Rust_Info(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="rust")
    async def send_info(self, ctx: commands.Context, first: str, second: str | None = None):
        rust_info_channel = self.bot.get_channel(rust_info_channel_id)
        display_avatar = ctx.author.display_avatar

        delt_msg_str = delt_str_time(sec_to_delta)

        if first.lower() in ["help", "info", "i"]:
            icon_url = img_url.rust.team_logo
            thumbnail_url = img_url.piktogramm.i
            embed = discord.Embed(title="#rust-info", color=0x8080ff)
            embed.set_author(name=f"@{ctx.author}", icon_url=f"{display_avatar}")
            embed.set_thumbnail(url=thumbnail_url)

            json_rust_help_commands_data = read_json_file(json_rust_help_commands_data_dir)

            # Número máximo de campos por embed
            max_fields_per_embed = 25

            # Contador de campos
            field_count = 0

            # Lista para armazenar embeds
            embeds_list = []

            for item in json_rust_help_commands_data:
                if field_count < max_fields_per_embed:
                    command = item["command"]
                    description = item["description"]
                    embed.add_field(name=command, value=description, inline=False)
                    field_count += 1
                else:
                    # Reinicia o contador de campos
                    field_count = 0
                    # Adiciona o embed atual à lista
                    embeds_list.append(embed)
                    # Cria um novo embed para o próximo conjunto de campos
                    embed = discord.Embed(title="#rust-info", color=0x8080ff)
                    embed.set_author(name=f"@{ctx.author}", icon_url=f"{display_avatar}")
                    embed.set_thumbnail(url=thumbnail_url)
                    # Adiciona o campo atual ao novo embed
                    embed.add_field(name=command, value=description, inline=True)
                    # Incrementa o contador de campos para o novo embed
                    field_count += 1

            # Adiciona o último embed à lista
            embeds_list.append(embed)

            await rust_info_channel.send(embeds=embeds_list, delete_after=(sec_to_delta))

        if first.lower() == "raid":
            embed = discord.Embed(title="Calculadora de Raid",
                    url="",
                    description=f"[Use a tabela e a calculadora]\n\n{delt_msg_str}")
            embed.set_author(name=f"@{ctx.author}", icon_url=f"{display_avatar}")
            embed.set_image(url=img_url.rust.raid_card)
            await rust_info_channel.send(embed=embed, delete_after=(sec_to_delta))

        if first.lower() in ["cctv", "code"]:

            embed = discord.Embed(title="Códigos CCTV",
                url="",
                description=f"[Use CCTV para obter as câmeras]\n{delt_msg_str}")
            embed.set_author(name=f"@{ctx.author}", icon_url=f"{display_avatar}")
            embed.set_image(url=img_url.rust.cctv_card)
            embed.set_thumbnail(url=img_url.rust.cctv)
            cctv_codes_json = read_json_file(cctv_codes_json_dir)
            for moment in cctv_codes_json:
                moment_name = moment
                code_list = cctv_codes_json[moment]
                code_str = ""
                for num in code_list:
                    code = code_list[num]
                    code_str += f"`{code}`\n"

                embed.add_field(name=f"**{moment_name}**",
                    value=f"{code_str}",
                    inline=False)

            await rust_info_channel.send(embed=embed, delete_after=(sec_to_delta))

        if first.lower() in ["pager", "transmiter", "code"]:
                
            embed = discord.Embed(title="Pager / Frequência", url="")
            embed.set_author(name=f"@{ctx.author}", icon_url=f"{display_avatar}")
            embed.set_thumbnail(url=img_url.rust.pager)
            embed.set_image(url=img_url.rust.cctv_card)
            embed.add_field(name="Pequeno Oil Rig", value="`4765`", inline=True)
            embed.add_field(name="Grande Oil Rig", value="`4768`", inline=True)
            embed.add_field(name="Excavadora Gigante", value="`4777`", inline=True)
            await rust_info_channel.send(embed=embed, delete_after=(sec_to_delta))


        if first.lower() in ["cost", "price", "preis", "pricelist"]:

            embed = discord.Embed(title="Lista de Preços",
                url="",
            description=f"\n{delt_msg_str}")
            embed.set_thumbnail(url=img_url.rust.scrape)
            embed.set_image(url=img_url.rust.rust_collection)
            embed.set_author(name=f"@{ctx.author}", icon_url=f"{display_avatar}")

            price_list_json = read_json_file(price_list_json_dir)
            for moment in price_list_json:
                moment_name = moment
                list_ = price_list_json[moment]
                price_str = ""
                for item in list_:
                    price = list_[item]
                    price_str += f"{item} - `{price}`\n"

                embed.add_field(name=f"{moment_name}",
                                value=f"{price_str}", inline=False)

            await rust_info_channel.send(embed=embed, delete_after=(sec_to_delta))

        if first.lower() in ["fert", "fertiliser"]:
            url = r""
            text_link = f"\n"
            if second is None:
                embed = discord.Embed(title="Calculadora de Fertilizante", url=url, description=f"{text_link}`2` Fertilizante rende `3` Scrap\n\n{delt_msg_str}", color=0x0000ff)
                embed.set_author(name=f"@{ctx.author}", icon_url=f"{display_avatar}")
                embed.set_thumbnail(url=img_url.rust.fertilizer)
                embed.set_image(url=img_url.rust.diesel_card)

                
                await rust_info_channel.send(embed=embed, delete_after=(sec_to_delta))

            else:
                fert_menge = int(second)
                fert_sel_min = 2
                fert_sell_Scrap = 3
                sell_Scrap_sum = int(fert_menge * (fert_sell_Scrap / fert_sel_min))
                embed = discord.Embed(title="Calculadora de Fertilizante", url=url,
                    description=f"{text_link}`{fert_menge}` Fertilizante rende `{sell_Scrap_sum}` Scrap\n\n{delt_msg_str}", color=0x0000ff)
                embed.set_author(name=f"@{ctx.author}", icon_url=f"{display_avatar}")
                embed.set_thumbnail(url=img_url.rust.fertilizer)
                embed.set_image(url=img_url.rust.diesel_card)

                await rust_info_channel.send(embed=embed, delete_after=(sec_to_delta))

    @commands.command(name="rust_help")
    async def rust_help(self, ctx: commands.Context):
        embed = discord.Embed(title="Comandos de Ajuda Rust", description="Veja os comandos disponíveis para Rust", color=0x00ff00)
        embed.set_author(name=f"@{ctx.author}", icon_url=f"{ctx.author.display_avatar}")
        for command in rust_help_commands:
            embed.add_field(name=command, value=f"Uso: `/rust {command.lower()}`", inline=False)
        await ctx.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Rust_Info(bot))
