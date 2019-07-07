from music21 import *
from jsonLoader import *
from Parts.allParts import *
import copy

environment.set("musicxmlPath", r"C:\Program Files\MuseScore 3\bin\MuseScore3.exe")
#C:\ProgramData\Microsoft\Windows\Start Menu\Programs\TuxGuitar

def main():

    # Die einzelnen Songstück-Klassen

    knowledge = {}

    knowledge["partobjects"] = {}

    knowledge["musicparts"] = {}

    '''       "mood": 3,
             "compl": 2,
             "tempo": 2,'''
    knowledge["input"]= {

             "genre": "Punk"}
    print(knowledge["input"])
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
        print(string_part)
        if not str(string_part) in knowledge["partobjects"]:
            knowledge["partobjects"][str(string_part)] = copy.deepcopy(globals()[string_part](knowledge, str(string_part)))
            knowledge["partobjects"][string_part].generate()
        #else:
        #    print("Repeat")


    acc = []
    for part in knowledge["partobjects"]:
        print(part)
        #knowledge["partobjects"][part].generated_music.show()
        acc += [knowledge["partobjects"][part].generated_music.__deepcopy__()]
    print(acc)
    result = flatappend(acc)
    #result.show()
    #result.show("text")

    n = note.Note("A1", type='quarter')
    drumPart = stream.Part()
    drumPart.insert(0, instrument.BassDrum())

    #for _ in range(int(result.quarterLength)):
    while(drumPart.quarterLength<result.quarterLength):
        drumPart.append(n.__deepcopy__())
    #result.insert(0, drumPart)
    result.write('midi', "CombinedSong.mid")
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

def flatappend(partlist):
    part1 = stream.Part()
    part2 = stream.Part()
    count = 0
    for songpart in partlist:
        #songpart.show()
        for singlemeasure in songpart.getElementsByClass(stream.Part).stream():
             if (count % 2 == 0):
                 part1.append(singlemeasure.__deepcopy__())
             else:
                 part2.append(singlemeasure.__deepcopy__())
             count = count + 1
    combined = stream.Stream()
    combined.append(part1)
    combined.append(part2)
    return combined

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