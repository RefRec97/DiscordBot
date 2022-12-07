import logging
import inspect

import interactions
from bot_utils.authHandler import AuthHandler

class Authentication(interactions.Extension):
    def __init__(self, bot: interactions.Client):
        self.bot: interactions.Client = bot
        self._auth = AuthHandler.instance()
    
    @interactions.extension_command(
        name="auth",
        description="Authorisiert Nutzer auf Befehle",
        options = [
            interactions.Option(
                name="username",
                description="username des Nutzers",
                type=interactions.OptionType.STRING,
                required=True,
            ),
            interactions.Option(
                name="gruppe",
                description="rechtegruppe des Nutzers",
                type=interactions.OptionType.STRING,
                required=True,
            ),
        ],
    )
    async def auth(self, ctx: interactions.CommandContext, *,username, gruppe):
        #todo: add update logic
        try:
            if(AuthHandler.instance().check(ctx)):
                if self._auth.add(username, gruppe):
                    returnMsg = "Erfolgreich Authorisiert"
                else:
                    returnMsg = "Authorisiorung fehlgeschlagen"
                await ctx.send(returnMsg)
            else:
                await ctx.send("Keine Rechte diesen Befehl zu nutzen")
            return
        except Exception as e:
            template = "Fehler aufgetreten, bitte Reflexrecon melden: {0} . Arguments:\n{1!r}"
            message = template.format(type(e).__name__, e.args)
            await ctx.send(message)
            return
        

    @interactions.extension_command(
        name="deauth",
        description="Deauthorisiert Nutzer auf Befehle",
        options = [
            interactions.Option(
                name="username",
                description="username des Nutzers",
                type=interactions.OptionType.STRING,
                required=True,
            ),
            interactions.Option(
                name="gruppe",
                description="rechtegruppe des Nutzers",
                type=interactions.OptionType.STRING,
                required=True,
            ),
        ],
    )
    async def deauth(self, ctx: interactions.CommandContext, *,username, gruppe):
        try:
            if(AuthHandler.instance().check(ctx)):
                if self._auth.remove(username, gruppe):
                    returnMsg = "Erfolgreich Deauthorisiert"
                else:
                    returnMsg = "Authorisiorung fehlgeschlagen"
                await ctx.send(returnMsg)
            else:
                await ctx.send("Keine Rechte diesen Befehl zu nutzen")
            return
        except Exception as e:
            template = "Fehler aufgetreten, bitte Reflexrecon melden: {0} . Arguments:\n{1!r}"
            message = template.format(type(e).__name__, e.args)
            await ctx.send(message)
            return

    @interactions.extension_command(
        name="ban",
        description="Bannt Nutzer von dem Bot",
        options = [
            interactions.Option(
                name="username",
                description="username des Nutzers",
                type=interactions.OptionType.STRING,
                required=True,
            ),
        ],
    )
    async def ban(self, ctx: interactions.CommandContext, *,username):
        try:
            username = username.lower()
            if(AuthHandler.instance().check(ctx)):
                if self._auth.remove(username):
                    returnMsg = "Bonk!"
                else:
                    returnMsg = "Bonk hammer kaputt"
                await ctx.send(returnMsg)
            else:
                await ctx.send("Keine Rechte diesen Befehl zu nutzen")
            return
        except Exception as e:
            template = "Fehler aufgetreten, bitte Reflexrecon melden: {0} . Arguments:\n{1!r}"
            message = template.format(type(e).__name__, e.args)
            await ctx.send(message)
            return
        

    #@auth.error
    async def auth_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Fehler in den Argumenten!\nBsp.: !auth Sc0t#123,boom')
        elif isinstance(error, commands.CheckFailure):
            await ctx.send('Keine rechte diesen Befehl zu nutzen')
        else:
            logging.error(error)
            await ctx.send('ZOMFG ¯\_(ツ)_/¯')
    
    #@deauth.error
    async def deauth_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Spielername fehlt!\nBsp.: !deauth Sc0t#123,boom')
        elif isinstance(error, commands.CheckFailure):
            await ctx.send('Keine rechte diesen Befehl zu nutzen')
        else:
            logging.error(error)
            await ctx.send('ZOMFG ¯\_(ツ)_/¯')
    
    #@ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Spielername fehlt!\nBsp.: !ban Sc0t#123')
        elif isinstance(error, commands.CheckFailure):
            await ctx.send('Keine rechte diesen Befehl zu nutzen')
        else:
            logging.error(error)
            await ctx.send('ZOMFG ¯\_(ツ)_/¯')

def setup(bot: interactions.Client):
    Authentication(bot)
