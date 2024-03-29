from bot_utils.singleton import Singleton
from bot_utils.db import DataBase


@Singleton
class AuthHandler:
    def __init__(self):
        self._groups: list = []
        self._db = DataBase()
        self._adminrights = ['admin']
        self._modrights = ['admin', 'mod']
        self._userrights = ['admin', 'mod', 'user']
        self._openrights = ['admin', 'mod', 'user', 'open']
        self._admincommands = []
        self._modcommands = ['auth', 'addUpdate', 'deauth', 'ban']
        self._usercommands = [
            'stats', 'allianz_position', 'moon_data', 'moon_add', 'moon_delete', 'moon_update', 'moon_phalanx_update', 
            'moons_in_range', 'planet_add', 'planet_delete', 'playerlink']

    #def addBot(self, bot: commands.bot):
    #    self._bot = bot

    def check(self, ctx):
        author = str(ctx.user.username).lower()
        author += '#' + ctx.user.discriminator
        command = str(ctx.data.name).lower()
        role = self._db.check_auth(author)

        #check for groups
        if command in self._modcommands:
            if role in self._modrights:
                return True
        elif command in self._usercommands:
            if role in self._userrights:
                return True
            else:
                return False
        else:
            if role in self._openrights:
                return True
            else:
                return False
    
    def add(self, user: str, field: str):
        if field in self._userrights:
            self._db.add_auth(user, field)
            return True
        else:
            return False

    def update(self, user: str, field: str):
        if field in self._userrights:
            self._db.update_auth(user, field)
            return True
        else:
            return False

    def remove(self, user: str):
        self._db.delete_auth(user)

        #todo: check if successful deauth
        return True
