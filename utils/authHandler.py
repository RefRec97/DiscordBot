import logging

from utils.singleton import Singleton
from utils.fileHandler import FileHandler
from utils.myData import MyData


@Singleton
class AuthHandler:
    def __init__(self):
        self._fileHandler: FileHandler = FileHandler.instance()
        self._authData: dict = {}

        self._normal = [
            "allianz",
            "planet",
            "chart",
            "history",
            "stats",
            "status",
            "test",
            "link"
        ]
        self._poll = [
            "allianz",
            "planet",
            "boom",
            "chart",
            "history",
            "stats",
            "status",
            "test",
            "link"
        ]

        self._setup()
    
    def check(self, ctx):
        author = str(ctx.author).lower()
        return author in self._authData[str(ctx.command)] or\
               author in self._authData["op"]
    
    def add(self, user: str , fields: str):
        if fields == "normal":
            for command in self._normal:
                if not user in self._authData[command]:
                    self._authData[command].append(user)
        elif fields == "poll":
            for command in self._poll:
                if not user in self._authData[command]:
                    self._authData[command].append(user)
        elif fields in self._authData:
            if not user in self._authData[fields]:
                self._authData[fields].append(user)
        
        return self._fileHandler.setAuthData(self._authData)
    
    def remove(self, user: str , fields: str):
        if fields == "normal":
            for command in self._normal:
                if user in self._authData[command]:
                    self._authData[command].remove(user)
        elif fields == "poll":
            for command in self._poll:
                if user in self._authData[command]:
                    self._authData[command].append(user)
        elif fields == "all":
            for command in self._authData:
                if user in self._authData[command]:
                    self._authData[command].remove(user)
        elif fields in self._authData:
            if user in self._authData[fields]:
                self._authData[fields].remove(user)
        
        return self._fileHandler.setAuthData(self._authData)

    def _setup(self):
        myData: MyData = self._fileHandler.getAuthData()
        if(myData.valid):
            self._authData = myData.data
        else:
            logging.warning("Auth: Invalid authData to update")
        