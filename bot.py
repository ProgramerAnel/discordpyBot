
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
                placeholder="Poshmark" 
            )
        )
        self.add_item(
            InputText(
                label="Sold price",
                placeholder="xxxx$" 
            )
        )
        self.add_item(
            InputText(
                label="Sold note",
                placeholder="Note",style=discord.InputTextStyle.long 
            )
        )
    async def callback(self,interaction:discord.Interaction):
        _sku = self.children[0].value
        _site = self.children[1].value
        _price = self.children[2].value
        _note = self.children[3].value
        print(f'Sold request for sku {_sku}')
        sql = '''SELECT
            CASE WHEN Active = 1 THEN 1 Else 0 End AS ActiveEbay,
            CASE WHEN Active = 1 then 'https://www.ebay.com/itm/' + cast(ebay_id as nvarchar ) else null end as EbayLink,
            CASE WHEN ActiveEtsy  = 1 THEN 1 Else 0 End AS ActiveEtsy ,
            CASE WHEN ActiveEtsy  = 1 then 'https://www.etsy.com/listing/' + cast(ETSY_ID as nvarchar ) else null end as EtsyLink,
            CASE WHEN ActivePoshmark  = 1 THEN 1 Else 0 End AS ActivePoshmark ,
            CASE WHEN ActivePoshmark  = 1 then POSHMARK_LINK else null end as PoshmarkLink,
            CASE WHEN activemercari  = 1 THEN 1 Else 0 End AS ActiveMercari ,
            CASE WHEN activemercari  = 1 then MERCARI_LINK else null end as MercariLink,
            ID, Title,(select top 1 PICTURE_PATH from sellduct.dbo.ACTIVE_ITEMS_PICTURES where ACTIVE_ITEMS_PICTURES.ACTIVE_ITEMS_ID = ACTIVE_ITEMS.ID) IMG
        FROM sellduct.dbo.ACTIVE_ITEMS where sku = ?'''
        
        myData = myDB.execute_and_fetch(sql,_sku)
        for ActiveEbay,EbayLink,ActiveEtsy,EtsyLink,ActivePoshmark,PoshmarkLink,ActiveMercari,MercariLink,ID,Title,IMG in myData:
 
            embMsg=discord.Embed(title=f"#{_sku} Sold for {_price}$ on {_site}", url=EbayLink, description=Title, color=0xe71212)
  
            embMsg.add_field(name="Poshmark", value=PoshmarkLink, inline=False)
            embMsg.add_field(name="Etsy", value=EtsyLink, inline=False)
            embMsg.add_field(name="Ebay", value=EbayLink, inline=False)
            embMsg.add_field(name="Mercari", value=MercariLink, inline=False) 
            embMsg.timestamp = datetime.datetime.utcnow()
            embMsg.set_footer(text='Bot by programerAnel@gmail.com',icon_url= 'https://i.imgur.com/wSTFkRM.png')
            # embMsg.set_thumbnail(url=IMG)
            # if ActiveEbay==1:
            #     myDB.execute("INSERT INTO sellduct.dbo.QUEUE(ACTIVE_ITEMS_ID,SITE,TYPER)VALUES('?','Ebay','End')",ID)
            # if ActiveEtsy==1:
            #     myDB.execute("INSERT INTO sellduct.dbo.QUEUE(ACTIVE_ITEMS_ID,SITE,TYPER)VALUES('?','Etsy','End')",ID)
            # if ActivePoshmark:
            #     myDB.execute("INSERT INTO sellduct.dbo.QUEUE(ACTIVE_ITEMS_ID,SITE,TYPER)VALUES('?','Poshmark','End')",ID)
            # if ActiveMercari:
            #     myDB.execute("INSERT INTO sellduct.dbo.QUEUE(ACTIVE_ITEMS_ID,SITE,TYPER)VALUES('?','Mercari','End')",ID)


        # myDB.execute("UPDATE sellduct.DBO.ACTIVE_ITEMS SET sold_price = ?, Active = 0, sold_site = ?, SOLD_DATE = getdate(),SOLD_NOTE = ? WHERE SKU = ? ", _price,
        #             _site, _note, _sku)

        await interaction.response.send_message(embed=embMsg)

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
        print(f'Check request for sku {sku}')
async def getSqlData(sku, message):
    mySQLData = myDB.execute_and_fetch('select Mercari_price,POSHMARK_PRICE,Title,Price,isnull(Active,0) Active,ActiveEtsy,ActivePoshmark,activemercari,POSHMARK_LINK,MERCARI_LINK,SPECIFICS_JSON,ebay_id,(select top 1 PICTURE_PATH from sellduct.dbo.ACTIVE_ITEMS_PICTURES where ACTIVE_ITEMS_PICTURES.ACTIVE_ITEMS_ID = ACTIVE_ITEMS.ID) IMG from sellduct.dbo.Active_Items where SKU = ?', sku) 
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
    # embMsg.set_thumbnail(url=IMG)

    embMsg.add_field(name="Price [Ebay]", value=Price, inline=True)
    embMsg.add_field(name="Price [Poshmark]", value=POSHMARK_PRICE, inline=True)
    embMsg.add_field(name="Price [Mercari]", value=Mercari_price, inline=True)
    embMsg.timestamp = datetime.datetime.utcnow()
    embMsg.set_footer(text='Bot by programerAnel@gmail.com',icon_url= 'https://i.imgur.com/wSTFkRM.png')

    await message.channel.send(embed=embMsg)

bot.run(TOKEN)