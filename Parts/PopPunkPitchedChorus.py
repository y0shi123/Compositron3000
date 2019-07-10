import random as rn
from Parts.generic_part import generic_part
from music21 import *

# Ohne init in Generators
from Generators.PunkChords import PunkChords
from Generators.PunkMelody import PunkMelody


class PopPunkPitchedChorus(generic_part):

    def __init__(self, passedknowledge, name):
        super().__init__(passedknowledge, name)
        self.generated_music = None

    def generate(self):

        mystruct = self.knowledge["ChosenStruct"]
        mycompl = int(mystruct["compl"])
        mytempo = int(mystruct["tempo"]) * 30
        mytempo = max(mytempo, 60)
        print("Tempo: " + str(mytempo))
        mykey = mystruct["key"]
        self.key = mykey
        myscale = mystruct["scale"]
        mygenre = mystruct["genre"]

        copychorus = None
        for part in self.knowledge["partobjects"]:
            if "PopPunkChorus" in self.knowledge["partobjects"][part].name:
                copychorus = self.knowledge["partobjects"][part].generated_music.__deepcopy__()

        for elem in copychorus.flat.getElementsByClass(["Chord", "Note"]):
            for pitch in elem.pitches:
                #pitch.octave = pitch.implicitOctave+1
                pitch.transpose(3, inPlace=True)
        copychorus.show('text')
        self.generated_music = copychorus
