from music21 import *
from jsonLoader import *
from Parts.allParts import *

environment.set("musicxmlPath", r"C:\Program Files\MuseScore 3\bin\MuseScore3.exe")
#C:\ProgramData\Microsoft\Windows\Start Menu\Programs\TuxGuitar

def main():

    # Die einzelnen Songstück-Klassen

    knowledge = {}

    knowledge["partobjects"] = {}

    knowledge["musicparts"] = {}

    knowledge["input"]= {
             "mood": 3,
             "compl": 4,
             "tempo": 3,
             "genre": "ska"}

    knowledge["ChosenStruct"] = searchStructures(knowledge["input"])

    if knowledge["ChosenStruct"] is None:
        print("No Matching Song Structure could be found")
        exit(0)

    print("The generated song will have the following properties:")
    print(knowledge["ChosenStruct"])

    x = searchParts(knowledge["ChosenStruct"]["parts"])

    if (x is not True):
        print("Missing Part: ")
        print(x)
        exit(0)


    for string_part in knowledge["ChosenStruct"]["parts"].split(", "):
        if not str(string_part) in knowledge["partobjects"]:
            knowledge["partobjects"][str(string_part)] = globals()[string_part](knowledge, str(string_part))
            knowledge["partobjects"][string_part].generate()

    print("Success")


def searchStructures(userInput):

    myJsonLoader = JsonLoader()
    foundentry = True

    for entry in myJsonLoader.SongStructures:
        foundentry = True
        for a in entry:
            if a in userInput and not str(entry[a]) == str(userInput[a]):
                foundentry = False
        if foundentry:
            return entry

def searchParts(partList):

    myJsonloader = JsonLoader()

    for part in partList.split(", "):
        fountpart = False
        for entry in myJsonloader.PartsList["Available"].split(", "):
            if str(entry) == str(part):
                fountpart = True
                break
        if not fountpart:
            return part
    return True

if __name__== "__main__":
    main()