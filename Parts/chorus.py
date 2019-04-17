from Parts.generic_part import  *
from Generators.PopChords import *
import random as rn

class Chorus(generic_part):

    def __init__(self, passedknowledge, name):
        super().__init__(passedknowledge, name)
        #print("This is the {}".format(name))

    def generate(self):
        #{'mood': '3', 'compl': '1', 'tempo': '2', 'parts': 'Chorus, Chorus', 'genre': 'pop', 'key': 'C', 'scale': 'dorian'}

        mystruct = self.knowledge["ChosenStruct"]
        mycompl = int(mystruct["compl"])
        mytempo = int(mystruct["tempo"])*10 + rn.randint(-5,5)
        mykey = mystruct["key"]
        myscale = mystruct["scale"]
        mygenre = mystruct["genre"]

        chordGenerator = PopChords()
        chordGenerator.generate(mykey, mycompl, mytempo, myscale, mygenre).show()