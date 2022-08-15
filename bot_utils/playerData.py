import logging

from bot_utils.singleton import Singleton


@Singleton
class PlayerData:
    def __init__(self):
        a = 1
    
    def build_chart_dict(self, data):
        result: dict = {}
        result = {"date": [], "platz": [], "gesamt": [], "gebäude":[], "forschung": [], "flotte": [], "defensive": []}
        for day in data:
            result["platz"].append(day[0])
            result["gesamt"].append(day[1])
            result["gebäude"].append(day[2])
            result["forschung"].append(day[3])
            result["flotte"].append(day[4])
            result["date"].append(str(day[5])[:-9])
            result["defensive"].append(day[6])
        return result

    def build_history_dict(self, data):
        row: dict = {}
        
        result = []
        for day in data:
            row = {"date": str(day[4])[:-9], "platz": day[0], "gesamt": day[1], "gebäude": day[2], "flotte": day[3]}
            result.append(row)
        return result