import os
import asyncio
from twitchio.ext import commands

class Bot(commands.Bot):

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        super().__init__(token=os.environ['TMI_TOKEN'], prefix=os.environ['BOT_PREFIX'], initial_channels=[os.environ['CHANNEL']])
        try:
            with open('banlist.txt','r') as f:
                self.data = [(line.strip()) for line in f.readlines()]
        except FileNotFoundError:
            self.data = []
        self.tulokset = {}
        self.voittajat = ""
        self.osallistujat = None
        self.tulos = None
        self.isOpen = False
        self.ilmoitusBingoaloitettu = 'Bingo aloitettu'
        self.ilmoitusBingoauki = 'Bingo on jo auki...'
        self.ilmoitusBingosuljettu = 'Bingo suljettu'
        self.ilmoitusBingotyhmä = 'Bingo on jo suljettu tyhmä'
        self.ilmoitusBingomyöhässä = 'Myöhässä KEKW'
        self.ilmoitusBingonumerotallennettu = 'VoteYea'
        #Experimental autopay: change False -> True below if you want to enable autopay feature on bot startup
        self.autopayStatus = False
        #Prize for winning in bingo
        self.autoPayprize = 5000

    # We are logged in and ready to chat and use commands...
    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print('Bot loaded and ready')

    #Doing some error handling to not flood cmd when command is not registered to this bot.
    async def event_command_error(self,ctx: commands.Context,error: Exception):
        #If command in chat isn't registered to this bot, ignore command.
        if isinstance(error,commands.CommandNotFound):
            return

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot..
        # For now we just want to ignore them...
        if message.echo:
            return

        # Waiting to catch commands from new events and executing them
        await self.handle_commands(message)

    #Registering command for the bot
    @commands.command()
    async def aloita(self,ctx: commands.Context):
        #Checking if command was send by a moderator
        if ctx.author.is_mod or ctx.author.name == os.environ['CHANNEL']:
            if self.isOpen == False:
                #Opening bingo game for users
                self.isOpen = True
                #Clearing tulos for new round
                self.tulos = None
                #Sending message to twitch chat 
                await ctx.send(f'@{ctx.author.name} -> {self.ilmoitusBingoaloitettu}')
                #Clearing tulokset dictionary
                self.tulokset = {}
                #Clearing voittajat string
                self.voittajat = ""
                #Printing newline to our console
                print('-----')
            else:
                #Someone tried to open bingo even it was already open
                await ctx.send(f'@{ctx.author.name} -> {self.ilmoitusBingoauki}')

    @commands.command()
    async def sulje(self,ctx: commands.Context):
        if ctx.author.is_mod or ctx.author.name == os.environ['CHANNEL']:
            if self.isOpen == True:
                self.isOpen = False
                await ctx.send(f'@{ctx.author.name} {self.ilmoitusBingosuljettu}')
            else:
                await ctx.send(f'@{ctx.author.name} {self.ilmoitusBingotyhmä}')

    #Registering command for the bot
    @commands.command()
    async def bingo(self,ctx: commands.Context, tulos: int) -> None:
        if ctx.author.name in self.data:
            print(f'{ctx.author.name} yritti väkisin osallistua bingoon')
        else:
            if self.isOpen == True:
                if 0 <= tulos <= 30:
                    tulokset = self.tulokset
                    tulokset[ctx.author.name] = tulos
                    tulokset = self.tulokset
                    await ctx.send(f'@{ctx.author.name} {self.ilmoitusBingonumerotallennettu}')
                else:
                    await ctx.send(f'@{ctx.author.name} tuloksesi ei ole 0-30 alueen sisällä!')
            else:
                await ctx.send(f'@{ctx.author.name} -> {self.ilmoitusBingomyöhässä}')

    #Registering command for the bot
    @commands.command()
    async def tulos(self,ctx: commands.Context, tulos: int ) -> None:
        if ctx.author.is_mod or ctx.author.name == os.environ['CHANNEL']:
            if self.isOpen == True:
                await ctx.send(f'@{ctx.author.name} Sulje ensin bingo pälli')
            if self.isOpen == False:
                if 0 <= tulos <= 30:
                    for k, v in sorted(self.tulokset.items(),key=lambda x: x[1]):
                        print(f'{k}:{v}')
                        if tulos == v:
                            self.voittajat += k + ", "
                    if self.voittajat == "":
                        print(f'Kierroksen tulos on {tulos}')
                        print(f'Ei voittajia')
                        await ctx.send(f'Ei voittajia')
                    else:
                        print(f'Kierroksen tulos on {tulos}')
                        print(f'Voittajia ovat: {self.voittajat}')
                        await ctx.send(f'Voittajia ovat: {self.voittajat}')
                        if self.autopayStatus == True:
                            for k, v in sorted(self.tulokset.items(),key=lambda x: x[1]):
                                if tulos == v:
                                    await asyncio.sleep(2)
                                    await ctx.send(f'!s {k} {self.autoPayprize}')
                else:
                    await ctx.send(f'{ctx.author.name} syöttämäsi tulos ei ole 0-30 alueen sisällä')

    #Registering command for the bot
    @commands.command()
    async def työttömyys(self,ctx: commands.Context, autopayStatus: str) -> None:
        #Checking if command was send by a moderator
        if ctx.author.is_mod or ctx.author.name == os.environ['CHANNEL']:
            if autopayStatus == 'on':
                self.autopayStatus = True
                await ctx.send(f'Hydyllä on apupyörät käytössä')
            if autopayStatus == 'off':
                self.autopayStatus = False
                await ctx.send(f'Hydy oppi ajamaan polkupyörällä')

    #Registering command for the bot
    @commands.command()
    async def ignore(self,ctx: commands.Context, result: str):
        #Checking if command was send by a moderator
        if ctx.author.is_mod or ctx.author.name == os.environ['CHANNEL']:
            self.data.append(result)
            with open('banlist.txt','w') as f:
                for item in self.data:
                    f.write('%s\n' % item)

if __name__ == '__main__':
    bot = Bot()
    bot.run()
