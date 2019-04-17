import json

class JsonLoader:
    def __init__(self):
        json_data = open("json files\SongStructures.json").read()
        songstr = json.loads(json_data)
        self.SongStructures = songstr

        json_data = open("json files\PartsList.json").read()
        partslis = json.loads(json_data)
        self.PartsList = partslis

