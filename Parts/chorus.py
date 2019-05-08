import random as rn
from Parts.generic_part import generic_part
from music21 import *

# Ohne init in Generators
from Generators.SkaChords import SkaChords
from Generators.PopChords import PopChords
from Generators.PopMelody import PopMelody

# Mit init in Generators. In der init werden
# dann die beiden Module importiert
#import Generators



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

        if mygenre == "ska":
            chordGenerator = SkaChords()
        else:
            chordGenerator = PopChords()
        music_chords = chordGenerator.generate(mykey, mycompl, mytempo, myscale, mygenre)
        #music_chords.show()
        melodyGenerator = PopMelody()
        music_melody = melodyGenerator.generate()
        print(music_melody.quarterLength)
        music_melody.show()
        music_melody.append(note.Note("c3", duration=duration.Duration(2)))
        print(music_melody.quarterLength)
        music_melody.show()
        '''music_complete = stream.Stream()
        music_complete.append(music_melody)
        music_complete.append(music_chords)
        music_complete.show()'''
