from discord.ext import commands
import logging
import db as Database
from singleton import Singleton

@Singleton
class AuthHandler:
    def __init__(self):
        self._bot: commands.bot = None
        self._groups: list = []
        self._db = Database.db()
        self._adminrights = ['admin']
        self._modrights = ['admin', 'mod']
        self._userrights = ['admin', 'mod', 'user']
        self._admincommands = []
        self._modcommands = ['auth', 'addUpdate']
    
    def addBot(self, bot: commands.bot):
        self._bot = bot

    def check(self, ctx):
        author = str(ctx.author).lower()
        
        #author = "n0sleep#9106"
        command = str(ctx.command).lower()
        role = self._db.check_auth(author)

        #check for groups
        if command == "auth":
            if role in self._modrights:
                return True
        else:
            if role in self._userrights:
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