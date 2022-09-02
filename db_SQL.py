 
from cProfile import label
from msilib.schema import ComboBox
import os  
import discord
from discord.ui import Modal, InputText, Select
from discord.ext.commands import Bot
import random
import datetime
from dotenv import load_dotenv
from db_SQL import DBSQL
load_dotenv()
myDB = DBSQL()

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
        _sku = self.children[0].value
        _site = self.children[1].value
        _price = self.children[2].value
        _note = self.children[3].value

        myDB.execute("UPDATE sellduct.DBO.ACTIVE_ITEMS SET sold_price = ?, Active = 0, sold_site = ?, SOLD_DATE = getdate(),SOLD_NOTE = ? WHERE SKU = ? ", _price,
                    _site, _note, _sku)

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

    if '/check' in message.content:
        sku = message.content.split('/check')[1].replace('#','').replace(' ','')
        await getSqlData(sku,message)

async def getSqlData(sku, message):
    mySQLData = myDB.execute_and_fetch('select Mercari_price,POSHMARK_PRICE,Title,Price,isnull(Active,0) Active,ActiveEtsy,ActivePoshmark,activemercari,POSHMARK_LINK,MERCARI_LINK,SPECIFICS_JSON,ebay_id,(select top 1 PICTURE_PATH from ACTIVE_ITEMS_PICTURES where ACTIVE_ITEMS_PICTURES.ACTIVE_ITEMS_ID = ACTIVE_ITEMS.ID) IMG from Active_Items where SKU = ?', sku) 
    for Mercari_price,POSHMARK_PRICE,Title,Price,Active,ActiveEtsy,ActivePoshmark,activemercari,POSHMARK_LINK,MERCARI_LINK,SPECIFICS_JSON,ebay_id,IMG in mySQLData:
        myTitle = Title
        myEbayID = ebay_id

        specifics = SPECIFICS_JSON.replace("|}", '').replace('{', '')
        specifics = specifics.split('|')
        output = ''
        for spec in specifics:
            output += spec.split(':')[0] + ":" + spec.split(':')[1] + '\n'

        if Active == 1:
            _state = "@AVAILABLE"
            _img = 'https://png.pngtree.com/png-clipart/20201029/ourlarge/pngtree-circle-clipart-bright-green-circle-png-image_2382005.jpg'
        else:
            _state = "@UNAVAILABLE"
            _img = 'https://m.media-amazon.com/images/I/21TPpHn1xRL.jpg'
 
    embMsg = discord.Embed(title=myTitle, 
        description=output, 
        color=0x0099ff,
        url=f"https://www.ebay.com/itm/{myEbayID}",
        )
    embMsg.set_author(name=_state,url=_img,icon_url=_img)
    # embedVar.set_author(_state, _img, 'https://discord.js.org')
    embMsg.set_thumbnail(url=IMG)

    embMsg.add_field(name="Price [Ebay]", value=Price, inline=True)
    embMsg.add_field(name="Price [Poshmark]", value=POSHMARK_PRICE, inline=True)
    embMsg.add_field(name="Price [Mercari]", value=Mercari_price, inline=True)
    embMsg.timestamp = datetime.datetime.utcnow()
    embMsg.set_footer(text='Bot by programerAnel@gmail.com',icon_url= 'https://i.imgur.com/wSTFkRM.png')

    await message.channel.send(embed=embMsg)

bot.run(TOKEN)