from discord.ext import commands
from utils.fileHandler import FileHandler

class Status(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        self.FileHandler = FileHandler.instance()
        self.lastUpdate = "N/A"
    
    @commands.command()
    async def test(self, ctx: commands.context):
        """Antwortet mit \"Test Bestanden\" (Verbindungstest)"""
        await ctx.send('Test bestanden')

    @commands.command()
    async def status(self, ctx: commands.context):
        """Stand des Datensatzes"""
        await ctx.send(f"Letztes Update: {self.FileHandler.getLastUpdate()}")
    


def setup(bot: commands.Bot):
    bot.add_cog(Status(bot))
