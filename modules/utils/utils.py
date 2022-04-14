from discord.ext import commands
from utils.fileHandler import FileHandler
import re
import logging

class Utils(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        self.FileHandler = FileHandler.instance()
        self.lastUpdate = "N/A"
    
    @commands.command(usage="<g>:<s>",
                      brief="Erzeugt ein Link auf die Position",
                      help="Erzeugt ein Link der die Position <g>:<s> in der Galaxyansicht führt")
    async def link(self, ctx: commands.context, position: str):
        position = position.lower()
        try:
            result = re.search("^(\d):(\d{1,3})$",position)
            galaxy = result.group(1)
            system = result.group(2)
        except:
            await ctx.send('Poisiton konnte nicht geparst werden\nz.B.: !link 1:1')
            return
        
        await ctx.send(f'https://pr0game.com/game.php?page=galaxy&galaxy={galaxy}&system={system}')

    @link.error
    async def link_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Fehlendes Argument!\nBsp.: !link 1:1')
        else:
            logging.error(error)
            await ctx.send('ZOMFG ¯\_(ツ)_/¯')


def setup(bot: commands.Bot):
    bot.add_cog(Utils(bot))
