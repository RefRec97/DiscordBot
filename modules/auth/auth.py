import logging
from discord.ext import commands

from utils.auth import AuthHandler

class Authentication(commands.Cog):
    def __init__(self, bot: commands.bot):
        self._bot: commands.bot = bot
        self._auth = AuthHandler.instance()
    
    @commands.check(AuthHandler.instance().check)
    @commands.command()
    async def auth(self, ctx: commands.context, username: str, field: str):
        """Authorisiert Nutzer auf befehle"""
        username = username.lower()
        field = field.lower()

        if self._auth.add(username, field):
            returnMsg = "Erfolgreich Authorisiert"
        else:
            returnMsg = "Authorisiorung fehlgeschlagen"

        await ctx.send(returnMsg)

    @commands.check(AuthHandler.instance().check)
    @commands.command()
    async def deauth(self, ctx: commands.context, username: str, field: str):
        """Deauthorisiert Nutzer auf befehle"""
        username = username.lower()
        field = field.lower()

        if self._auth.remove(username, field):
            returnMsg = "Erfolgreich Deauthorisiert"
        else:
            returnMsg = "Deauthorisiorung fehlgeschlagen"

        await ctx.send(returnMsg)

    @commands.check(AuthHandler.instance().check)
    @commands.command()
    async def ban(self, ctx: commands.context, username: str):
        """Deauthorisiert Nutzer auf den Bot"""
        username = username.lower()
       
        if self._auth.remove(username, "all"):
            returnMsg = "Bonk!"
        else:
            returnMsg = "Bonk hammer kaputt"

        await ctx.send(returnMsg)

    @auth.error
    async def auth_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Fehler in den Argumenten!\nBsp.: !auth Sc0t boom')
        elif isinstance(error, commands.CheckFailure):
            await ctx.send('Keine rechte diesen Befehl zu nutzen')
        else:
            logging.error(error)
            await ctx.send('ZOMFG ¯\_(ツ)_/¯')
    
    @deauth.error
    async def deauth_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Spielername fehlt!\nBsp.: !deauth Sc0t boom')
        elif isinstance(error, commands.CheckFailure):
            await ctx.send('Keine rechte diesen Befehl zu nutzen')
        else:
            logging.error(error)
            await ctx.send('ZOMFG ¯\_(ツ)_/¯')
    
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Spielername fehlt!\nBsp.: !ban Sc0t')
        elif isinstance(error, commands.CheckFailure):
            await ctx.send('Keine rechte diesen Befehl zu nutzen')
        else:
            logging.error(error)
            await ctx.send('ZOMFG ¯\_(ツ)_/¯')

def setup(bot: commands.Bot):
    bot.add_cog(Authentication(bot))
