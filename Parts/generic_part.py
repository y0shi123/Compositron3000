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
        #print("I am writing Music right now!")

    def whoareyou(self):
        print("I am: {}".format(self.name))

    def flatappend(self, *args):
        part1 = stream.Part()
        part2 = stream.Part()
        count = 0
        for songpart in args:
            for singlemeasure in songpart.getElementsByClass(stream.Part):
                if (count % 2 == 0):
                    part1.append(singlemeasure.__deepcopy__())
                else:
                    part2.append(singlemeasure.__deepcopy__())
                count = count + 1
        combined = stream.Stream()
        combined.append(part1.flat)
        combined.append(part2.flat)
        '''part1.show('text')
        part1.flat.show('text')
        #part1.show()
        part2.show('text')
        #part2.show()'''
        #print("Merged Streams:")
        #combined.show('text')
        #combined.show()
        return combined