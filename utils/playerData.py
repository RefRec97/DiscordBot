import logging

from utils.singleton import Singleton
from utils.myData import MyData
from utils.fileHandler import FileHandler


@Singleton
class PlayerData:
    def __init__(self):
        self._fileHandler = FileHandler.instance()
        self._userData = {}
        self._historyData = {}
        self._planetData = {}
        self._allianzData = {}
        self._userNames = []

        self.updateData()
    
    def updateData(self):
        logging.info("PlayerData: Updating data")
        #_updateUserData needs to be first
        self._updateUserData()
        self._updateHistoryData()
        self._updatePlanetData()

    def getUserDataReference(self):
        return self._userData
    
    def getUserNamesReference(self):
        return self._userNames

    def getHistoryDataReference(self):
        return self._historyData

    def getAllianzDataReference(self):
        return self._allianzData

    def addPlanet(self, position, username):
        #savePlanetData on currentClass
        if not position in self._planetData[username]:
            self._planetData[username].append(position)

            result = self._fileHandler.setPlanetData(self._planetData)
        else:
            result = False
        
        return result

    def delPlanet(self, position, username):
        if position in self._planetData[username]:
            self._planetData[username].remove(position)
            result = self._fileHandler.setPlanetData(self._planetData)
        else:
            result = False
        
        return result

    def _updateUserData(self):
        myData: MyData = self._fileHandler.getCurrentData()
        if(myData.valid):
            self._userData = myData.data
            self._setupUserNames()
            self._setupAllianzData()
        else:
            logging.warning("PlayerData: Invalid userData to update")
    
    def _setupUserNames(self):
        for user in self._userData:
            self._userNames.append(user)
    
    def _updateHistoryData(self):
        historyData: MyData = self._fileHandler.getHistoryData()
        
        if historyData.valid:
            self._historyData = historyData.data
        else:
            logging.warning("PlayerData: Invalid historyData to update")
        
        self._insertDiffDataToUser()
    
    def _insertDiffDataToUser(self):
        for user in self._historyData:
            userData = self._historyData[user][0]
            for element in userData:
                data = str(userData[element]).replace(".","")
                if data.isnumeric():
                    try:
                        currentData = str(self._historyData[user][-1][element]).replace(".","")
                        lastData = str(self._historyData[user][-2][element]).replace(".","")
                        self._userData[user]["diff_"+element] = "{:+g}".format(int(currentData) - int(lastData))
                    except:
                        #No history Data
                        if user in self._userData:
                            self._userData[user]["diff_"+ element] = "N/A"

    def _updatePlanetData(self):
        myData: MyData = self._fileHandler.getPlanetData()
        if myData.valid:
            self._planetData = myData.data
        else:
            logging.warning("PlayerData: Invalid userData to update")
        
        self._insertPlanetDataToUsers()
    
    def _insertPlanetDataToUsers(self):
        for user in self._userData:
            if user in self._planetData:
                self._userData[user]["planets"] = self._planetData[user]
    
    def _setupAllianzData(self):
        fullAllianzData: dict = self._getAllAllianzMember(self._userData)
        self._allianzData: dict = self._getAllTopAllianzMembers(fullAllianzData)

    def _getAllAllianzMember(self, userdata: dict):
        fullAllianzData = {}
        for user in userdata:
            name: str = userdata[user]["allianz"].lower().strip()
            if name in fullAllianzData:
                fullAllianzData[name].append(userdata[user])
            else:
                fullAllianzData[name] = [userdata[user]]
        
        return fullAllianzData
    
    def _getAllTopAllianzMembers(self, fullAllianzData: dict):
        topAllianzUsers = {}
        for allianzName in fullAllianzData:
            allianzUsers: list = fullAllianzData[allianzName]
            
            #sort users by rank and keep only top 10
            topAllianzUsers[allianzName] = sorted(allianzUsers,key=lambda d: d['platz'])[:10]
        
        return topAllianzUsers
