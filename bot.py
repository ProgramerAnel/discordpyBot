 
from cProfile import label
from msilib.schema import ComboBox
import os  
import discord
from discord.ui import Modal, InputText, Select
from discord.ext.commands import Bot
import random
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('PREFIX_COMMAND')

bot = discord.Bot("!", intents=discord.Intents.all())
servers = [854253909177794593]

class MyModal(Modal):
    def __init__(self) -> None:
        super().__init__(title="Item sold Dialog")
        self.add_item(InputText(label="SKU",placeholder="#1234B"))
        self.add_item(
            InputText(
                label="Sold site",
                value="Poshmark" 
            )
        )
        self.add_item(
            InputText(
                label="Sold price",
                value="xxxx$" 
            )
        )
        self.add_item(
            InputText(
                label="Sold note",
                value="Description",style=discord.InputTextStyle.long 
            )
        )
    async def callback(self,interaction:discord.Interaction):
        val1 = self.children[0].value
        val2 = self.children[1].value
        await interaction.response.send_message(f"{val1} and {val2}")

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.command(quild_ids = servers, name="sale")
async def SaleDialog(ctx):
    modal = MyModal()
    await ctx.interaction.response.send_modal(modal)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    if message.content == '99!':
        response = random.choice(brooklyn_99_quotes)
        await message.channel.send(response)

bot.run(TOKEN)