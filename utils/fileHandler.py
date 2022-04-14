import os
import json
import logging
from datetime import date
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from utils.singleton import Singleton
from utils.myData import MyData

@Singleton
class FileHandler:
    def __init__(self):
        load_dotenv()
        logging.info("FileHandler created")
        self._path = "files/"
        self._fileEnding = ".json"
        self._currentData = MyData({})
        self._historyData = MyData({})
        self._planetData = MyData()
        self._sitesToParse = 10          #each site has 100 Player
        self._lastUpdate = "N/A"
        self._historyFileNames = self._path + "historyFileNames" + self._fileEnding
        self._planetDataFile = self._path + "planetData" + self._fileEnding

    def getCurrentData(self):
        currentFileName = self._getCurrentFileName()

        if os.path.exists(currentFileName):
            logging.info("FileHandler: File Found, skipping scraping")
            self._currentData: MyData = self._readFile(currentFileName)
            self._lastUpdate =  date.today().strftime("%d_%m_%Y")
        else:
            self._currentData = self._scrape()
        
        return self._currentData

    def getHistoryData(self):
        historyFileNames: MyData = self._readFile(self._historyFileNames)

        try:
            if historyFileNames.valid:
                for file in historyFileNames.data["filenames"]:
                    day = self._readFile(self._path + file + self._fileEnding)
                    if day.valid:
                        for userName in day.data:
                            day.data[userName]["timestamp"] = file
                            if userName in self._historyData.data:
                                self._historyData.data[userName].append(day.data[userName])
                            else:
                                self._historyData.data[userName] = [day.data[userName]]
            self._historyData.valid = True
        except:
            self._historyData.valid = False
            logging.error("FileHandler: Failed to read/parse History Files")
       
        return self._historyData

    def getLastUpdate(self):
        return self._lastUpdate

    def getPlanetData(self):
        planetData: MyData = self._readFile(self._planetDataFile)

        if planetData.valid:
            self._planetData = planetData
        
        return self._planetData

    def setPlanetData(self, data: dict):
        self._planetData = data
        return self._writeFile(self._planetDataFile, data)

    def _getCurrentFileName(self):
        today = date.today()
        return self._path + today.strftime("%d_%m_%Y") + self._fileEnding

    def _readFile(self, filePath):
        myData = MyData()

        try:
            with open(filePath, encoding='utf-8' ) as file:
                myData.data = json.load(file)
                myData.valid = True
        except:
            myData.valid = False
            logging.error(f"FileHandler: Failed to open file {filePath}")
        
        return myData

    def _writeFile(self, filePath: str, data: dict):
        logging.info(f"FileHandler: Saving data to file {filePath}")
        try:
            with open(filePath, 'w') as file:
                file.write(json.dumps(data))
        except:
            logging.error(f"FileHandler: Failed to save data to file: {filePath}")
            return False
        return True

    def _scrape(self):
        """ToDo: Move in seperate File"""
        logging.info("FileHandler: Start Scraping Pr0game ...")
        
        myData = MyData()

        playerPosAndId = []
        try:
            with requests.Session() as session:
                self._login(session)
                playerPosAndId = self._parseStatisticSite(session)
                myData.data = self._parsePlayerCards(session, playerPosAndId)
                myData.valid= True
        except:
            myData.valid = False
            logging.error("FileHandler: Failed scrape Pr0game")
        
        if(myData.valid):
            self._writeFile(self._getCurrentFileName(), myData.data)
            self._lastUpdate = date.today().strftime("%d_%m_%Y")
            
        return myData

    def _parsePlayerCards(self, session, playerPosAndId):
        data = {}
        idx = 0
        for pos,id in playerPosAndId:
            if int(idx)%100 == 0:
                 logging.info(f"FileHandler: Parsing Playercard {idx+1} of {100* self._sitesToParse}")
            idx += 1

            url = 'https://pr0game.com/game.php?page=playerCard&id=1000]https://pr0game.com/game.php?page=playerCard&id={}'.format(str(id))
            r = session.get(url)
            soup = BeautifulSoup(r.text, "html.parser")

            table = soup.find('table')
            name = str(table.findChildren("tr" , recursive=False)[1].findChildren("td" , recursive=False)[1]).split(">")[1].split("<")[0].strip().lower()
            data[name] = { "platz": pos}
            data[name]["planets"] = []
            
            for tr in table.findChildren("tr" , recursive=False)[1:10]:
                try:
                    tds = tr.findChildren("td" , recursive=False)
                    keyName = str(tds[0]).split(">")[1].split("<")[0].strip().lower()
                    value = str(tds[1]).split(">")[1].split("<")[0].strip().lower()

                    if(keyName == "heimatplanet"):
                        value = str(tds[1]).split(">")[2].split("<")[0]

                    if(keyName == "allianz"):
                        value = str(tds[1]).split(">")[2].split("<")[0]

                    if(keyName):
                        data[name][keyName] = value
                except:
                    pass
        return data

    def _parseStatisticSite(self, session):
        playerPosAndId = []
        playerPos = 1

        for site in range(0, self._sitesToParse):
            logging.info(f"FileHandler: Site {site+1} of {self._sitesToParse} ...")
            payload = {
                "who": 1,
                "type" : "1",
                "range": "{}01".format(site)
            }
            r = session.post("https://pr0game.com/game.php?page=statistics", data=payload)
            soup = BeautifulSoup(r.text, "html.parser")

            table = soup.find_all("table",{"class":"table519"})[1]
            for tr in table.findChildren("tr" , recursive=False)[1:]:
                td = tr.findChildren("td" , recursive=False)[1]
                id = str(td).split('(')[1].split(',')[0]
                playerPosAndId.append((playerPos,id))
                playerPos+=1
            
        return playerPosAndId

    def _login(self,session):
        logging.info("FileHandler: Logging in ...")
        
        payload = {
            "uni": 1,
            "username" : os.getenv("PLAYERNAME"),
            "password": os.getenv("PASSWORD")
        }
        session.post('https://pr0game.com/index.php?page=login', data=payload)