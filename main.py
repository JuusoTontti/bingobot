import os
from twitchio.ext import commands
import re

class Bot(commands.Bot):

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        super().__init__(token=os.environ['TMI_TOKEN'], prefix=os.environ['BOT_PREFIX'], initial_channels=[os.environ['CHANNEL']])
        self.osallistujat = []
        self.tulokset = []
        self.tulos = None
        self.isOpen = None

    async def event_ready(self):
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print('Bot loaded and ready')

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot..
        # For now we just want to ignore them...
        if message.echo:
            return
        # Waiting to catch  commands from new events and executing them
        await self.handle_commands(message)

    @commands.command()
    async def aloita(self,ctx: commands.Context):
        if ctx.author.is_mod or ctx.author.name == os.environ['CHANNEL']:
            self.isOpen = True
            self.osallistujat = []
            self.tulokset = []
            self.tulos = None
            await ctx.send(f"@{ctx.author.name} -> Bingo aloitettu")
        else:
           await ctx.send("@" + ctx.author.name + " -> Sinulla ei ole oikeuksia tähän komentoon.")
    
    @commands.command()
    async def sulje(self,ctx: commands.Context):
        if ctx.author.is_mod or ctx.author.name == os.environ['CHANNEL']:
            self.isOpen = False
            await ctx.send(f'@{ctx.author.name} osallistuminen suljettu')
        else:
            await ctx.send("@" + ctx.author.name + " -> Sinulla ei ole oikeuksia tähän komentoon.")

    @commands.command()
    async def bingo(self,ctx: commands.Context):
        if re.search("!bingo", ctx.message.content):
            if self.isOpen == True:
                regex = r"!bingo "
                subst = ""
                result = re.sub(regex, subst, ctx.message.content)
                tulosregex = r"^((30)|([0-2]?[0-9]{1,1}))$"
                if re.match(tulosregex,result):
                    await ctx.send(f'{ctx.author.name} vastauksesi on rekisteröity!')
                    self.osallistujat.append(ctx.author.name)
                    self.tulokset.append(result)
                else:
                    await ctx.send(f'@{ctx.author.name} tuloksesi ei ole 0-30 alueen sisällä!')
            else:
                await ctx.send(f'@{ctx.author.name} -> Bingo osallistuminen on tällä hetkellä suljettu')

    @commands.command()
    async def tulos(self,ctx: commands.Context):
        if re.search("!tulos", ctx.message.content):
             regex = r"!tulos "
             subst = ""
             result = re.sub(regex, subst, ctx.message.content)
             await ctx.send(f'{ctx.author.name} tulos asetettu nyt voit listaa voittajat käyttämällä !listaa')
             self.tulos = result
        else:
                await ctx.send(f'@{ctx.author.name} -> Sinulla ei ole oikeuksia tähän komentoon.')

    @commands.command()
    async def listaa(self,ctx: commands.Context):
        if ctx.author.is_mod or ctx.author.name == os.environ['CHANNEL']:
            dictionary = dict(zip(self.osallistujat, self.tulokset))
            tulos = self.tulos
            if tulos in dictionary.values():
                for self.osallistujat, self.tulokset in dictionary.items():
                    if self.tulos == None:
                        await ctx.send(f'{ctx.author.name} -> Kierroksen tulosta ei ole vielä asetettu, moderaattorit asettakaa tulos käyttämällä !tulos komentoa.')
                    if self.tulokset == tulos:
                        await ctx.send(f'@{ctx.author.name} -> voittajia ovat {self.osallistujat}')
            else:
                await ctx.send(f'@{ctx.author.name} Ei voittajia!')
        else:
            await ctx.send("@" + ctx.author.name + " -> Sinulla ei ole oikeuksia tähän komentoon.")

bot = Bot()
bot.run()
