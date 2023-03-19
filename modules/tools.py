import re
import interactions
from interactions.ext.get import get
from bot_utils.authHandler import AuthHandler
from bot_utils.db import DataBase

from bot_utils.authHandler import AuthHandler

class Tools(interactions.Extension):
    def __init__(self, bot: interactions.Client):
        self.bot: interactions.Client = bot
        self._db = DataBase()

    @interactions.extension_command(name="link",
        description="Erzeugt ein Link der die Position <g>:<s> in der Galaxyansicht führt",
        options=[
            interactions.Option(
                name="position",
                description="gala_sys",
                type=interactions.OptionType.STRING,
                required=True,
            ),
        ],
    )
    async def link(self, ctx: interactions.CommandContext, position: str):
        try:
            position = position.lower()
            result = re.search("^(\d):(\d{1,3})$", position)
            galaxy = result.group(1)
            system = result.group(2)
        except:
            await ctx.send('Position konnte nicht geparst werden\nz.B.: !link 1:1')
            return
        #if AuthHandler.instance().check(ctx.author):
        await ctx.send(f'https://pr0game.com/game.php?page=galaxy&galaxy={galaxy}&system={system}')
        #else:
        #    await ctx.send('not authorized')

    @interactions.extension_command(name="playerlink",
        description="Erzeugt Links auf die Positionen eines Spielers in der Galaxyansicht führt",
        options=[
            interactions.Option(
                name="username",
                description="name des Spielers",
                type=interactions.OptionType.STRING,
                required=True,
            ),
        ],
    )
    async def playerlink(self, ctx: interactions.CommandContext, username: str):
        try:
            username = username.lower()
            ctx.defer()
            if(AuthHandler.instance().check(ctx) == False):
                await ctx.send("Keine Rechte diesen Befehl zu nutzen")
                return
            if not self._db.check_player(username):
                await ctx.send("Nutzer nicht gefunden")
                return
            planets = self._db.get_playerplanets_raw(username)
            result = ""
            for planet in planets:
                result +=(f'https://pr0game.com/game.php?page=galaxy&galaxy={planet["galaxy"]}&system={planet["system"]}')
                result += "\n"
        except Exception as e:
            template = "Fehler aufgetreten, bitte Reflexrecon melden: {0} . Arguments:\n{1!r}"
            message = template.format(type(e).__name__, e.args)
            await ctx.send(message)
            return
        await ctx.send(result)
        return
        


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


    @interactions.extension_listener(name='on_command')
    async def log(self, ctx: interactions.CommandContext):
        if ctx.guild_id:
            server = await ctx.get_guild()
        else:
            server = "private"

        user = str(ctx.user.username)
        command = str(ctx.data.name)
        args = []
        options = ctx.data.options
        if options:
            for option in options:
                args.append(option.value)

        channel = await get(self.bot, interactions.Channel, channel_id=987732014692171827)

        returnStr = "```{},{},{},{}```".format(server.name, user, command, args)
        await channel.send(returnStr)

def setup(bot: interactions.Client):
    Tools(bot)

