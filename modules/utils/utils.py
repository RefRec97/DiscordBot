import re
import os
import logging
import interactions
from interactions.ext.get import get

from utils.authHandler import AuthHandler

class Utils(interactions.Extension):
    def __init__(self, bot: interactions.Client):
        #self.bot = bot
        self.bot: interactions.Client = bot

    @interactions.extension_command(
        name="link",
        description="Erzeugt ein Link der die Position <g>:<s> in der Galaxyansicht führt",
        options = [
            interactions.Option(
                name="position",
                description="gala_sys",
                type=interactions.OptionType.STRING,
                required=True,
            ),
        ],
    )
    async def link(self, ctx: interactions.CommandContext, position: str):
        position = position.lower()
        try:
            result = re.search("^(\d):(\d{1,3})$",position)
            galaxy = result.group(1)
            system = result.group(2)
        except:
            await ctx.send('Position konnte nicht geparst werden\nz.B.: !link 1:1')
            return
        if AuthHandler.instance().check(ctx.author):
            await ctx.send(f'https://pr0game.com/game.php?page=galaxy&galaxy={galaxy}&system={system}')
        else:
            await ctx.send('not authorized')

    @interactions.extension_command(
        name="features",
        description="Zeigt geplante Features"
    )
    async def features(self, ctx: interactions.CommandContext):
        featureList: list = [
            "```"
            "Monde:",
            "   - Speichern von sensor Phalanx lvl",
            "       - Überprüfen ob man in Reichweite ist",
            "Wachstum:",
            "   - prozentualer wachstum wie unnamed statisik anzeigen",
            "     als Listenform und auf einzelne Spieler",
            "Differenz:",
            "   - Spieler miteinander vergleichen",
            "     als Chart und gegenüberstellung wie !stats",
            "   - Vll auch rel. Startpunkt einstellbar. Aka",
            "     Start ist bei beiden Spieler bei 5k",
            "Points:",
            "   - Reimplementieren",
            "```"
        ]
        await ctx.send("\n".join(featureList))
   
    #@commands.Cog.listener(name='on_command')
    @interactions.extension_listener(name='on_command')
    async def log(self, ctx: interactions.CommandContext):
        if ctx.guild_id:
            server = await ctx.get_guild() #ctx.guild_id._snowflake
        else:
            server = "private"
        #ctx.get_guild
        user = str(ctx.user.username)
        command = str(ctx.data.name)
        args = []
        options = ctx.data.options
        if options:
            for option in options:
                args.append(option.value)
        
        channel = await get(self.bot, interactions.Channel, channel_id=987732014692171827)
        
        returnStr = "```{},{},{},{}```".format(server,user,command, args)
        await channel.send(returnStr)

def setup(bot: interactions.Client):
    #bot.add_cog(Utils(bot))
    Utils(bot)

