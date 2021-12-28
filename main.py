import os
from twitchio.ext import commands
import re

class Bot(commands.Bot):

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        super().__init__(token=os.environ['TMI_TOKEN'], prefix=os.environ['BOT_PREFIX'], initial_channels=[os.environ['CHANNEL']])
        self.osallistujat = []
        self.tulokset = []
        self.voittajat = []
        self.tulos = None
        self.isOpen = None

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

        # Waiting to catch  commands from new events and executing them
        await self.handle_commands(message)

    #Registering command for the bot
    @commands.command()
    async def aloita(self,ctx: commands.Context):
        #Checking if command was send by a moderator
        if ctx.author.is_mod or ctx.author.name == os.environ['CHANNEL']:
            #Opening bingo game for users
            self.isOpen = True
            #Clearing osallistujat dictionary for new round
            self.osallistujat = []
            #Clearing tulokset dictionary for new round
            self.tulokset = []
            #Clearing voittajat
            self.voittajat = []
            #Clearing tulos for new round
            self.tulos = None
            #Sending message to twitch chat 
            await ctx.send(f'@{ctx.author.name} -> Bingo aloitettu')
            #Printing newline to our console
            print('-----')

    #Registering command for the bot
    @commands.command()
    async def sulje(self,ctx: commands.Context):
        #Checking if command was send by a moderator
        if ctx.author.is_mod or ctx.author.name == os.environ['CHANNEL']:
            #Checking noone has closed bingo yet 
            if self.isOpen == True:
                #Sending confirmation to chat
                await ctx.send(f'@{ctx.author.name} osallistuminen suljettu')
                #Joining our dictionaries
                self.voittajat = dict(zip(self.osallistujat, self.tulokset))
                #Closing bingo participation
                self.isOpen = False
            else:
                #Sending message when bingo is already closed but someone sent command to close it.
                await ctx.send(f'@{ctx.author.name} -> Bingo on jo suljettu')

    #Registering command for the bot
    @commands.command()
    async def bingo(self,ctx: commands.Context):
        #Searching !bingo command from chat
        if re.search("!bingo", ctx.message.content):
            #Checking if bingo game is open for participants
            if self.isOpen == True:
                #Finding !bingo and removing it from chat message
                regex = r"!bingo "
                subst = ""
                result = re.sub(regex, subst, ctx.message.content)
                #Checking that bingo aswer was inside of range 0-30
                tulosregex = r"^((30)|([0-2]?[0-9]{1,1}))$"
                #If aswer was inside of 0-30 range and has !bingo command then
                if re.match(tulosregex,result):
                    #Sending confirmation to command author
                    await ctx.send(f'@{ctx.author.name} vastauksesi on rekisteröity!')
                    #Appending osallistujat dictionary by author name
                    self.osallistujat.append(ctx.author.name)
                    #Appending tulokset dictionary by author result
                    self.tulokset.append(result)
                else:
                    #When aswer was not in 0-30 range then send message to that author in twitch chat
                    await ctx.send(f'@{ctx.author.name} tuloksesi ei ole 0-30 alueen sisällä!')
            else:
                #If command was given when bingo game was not open for participation
                await ctx.send(f'@{ctx.author.name} -> Bingoon osallistuminen on tällä hetkellä suljettu')

    #Registering command for the bot
    @commands.command()
    async def tulos(self,ctx: commands.Context):
        #Checking if command was send by a moderator
        if ctx.author.is_mod or ctx.author.name == os.environ['CHANNEL']:
            #Searching for !tulos command in twitch chat and clearing up that message
            if re.search("!tulos", ctx.message.content):
                regex = r"!tulos "
                subst = ""
                result = re.sub(regex, subst, ctx.message.content)
                if re.match("^((30)|([0-2]?[0-9]{1,1}))$", result):
                    #Setting tulos variable so we can find our winners
                    self.tulos = result
                    dictionary = self.voittajat
                    if result in dictionary.values():
                        for self.osallistujat, self.tulokset in dictionary.items():
                            if self.tulos == None:
                                await ctx.send(f'@{ctx.author.name} -> Kierroksen tulosta ei ole vielä asetettu, moderaattorit asettakaa tulos käyttämällä !tulos komentoa.')
                            if self.tulokset == result:
                                await ctx.send(f'@{ctx.author.name} -> voittajia ovat {self.osallistujat}')
                                print(f'{ctx.author.name}: voittajia ovat {self.osallistujat}')
                    else:
                        await ctx.send(f'@{ctx.author.name} -> Ei voittajia!')
                        print(f'{ctx.author.name}: Ei voittajia!')
                else:
                    await ctx.send(f'@{ctx.author.name} -> Syötä oikea tulos')

    #Registering command for the bot
    @commands.command()
    async def listaa(self,ctx: commands.Context):
        #Checking if command was send by a moderator
        if ctx.author.is_mod or ctx.author.name == os.environ['CHANNEL']:
            #Joining our two dictionaries
            dictionary = self.voittajat
            tulos = self.tulos
            if tulos in dictionary.values():
                for self.osallistujat, self.tulokset in dictionary.items():
                    if self.tulos == None:
                        await ctx.send(f'@{ctx.author.name} -> Kierroksen tulosta ei ole vielä asetettu, moderaattorit asettakaa tulos käyttämällä !tulos komentoa.')
                    if self.tulokset == tulos:
                        await ctx.send(f'@{ctx.author.name} -> voittajia ovat {self.osallistujat}')
                        print(f'{ctx.author.name}: voittajia ovat {self.osallistujat}')
            else:
                await ctx.send(f'@{ctx.author.name} -> Ei voittajia!')
                print(f'{ctx.author.name}: Ei voittajia!')

if __name__ == '__main__':
    bot = Bot()
    bot.run()
