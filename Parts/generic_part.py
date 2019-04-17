from music21 import *
import random as rn

class generic_part:

    def __init__(self, passedknowledge, passedname):
        self.name = passedname
        self.knowledge = passedknowledge

    def generate(self):
        mypart = stream.Stream()
        if "scale" in self.knowledge["chosenStruct"].keys():
            mykey = key.Key(self.knowledge["chosenStruct"]["key"],self.knowledge["chosenStruct"]["scale"])
        else:
            mykey = key.Key(self.knowledge["chosenStruct"]["key"])
        for i in range(4):
            mypart.append(note.Note(mykey.pitches[rn.randint(0,7)]))
        self.knowledge["musicparts"][self.name] = mypart
        print("I am writing Music right now!")

    def whoareyou(self):
        print("I am: {}".format(self.name))