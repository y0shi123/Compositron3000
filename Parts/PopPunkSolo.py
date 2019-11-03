import random as rn
from Parts.generic_part import generic_part
from music21 import *


# Ohne init in Generators
from Generators.PunkChords import PunkChords
from Generators.PunkMelody import PunkMelody


class PopPunkSolo(generic_part):

    def __init__(self, passedknowledge, name):
        super().__init__(passedknowledge, name)
        self.generated_music = None

    def generate(self):

        mystruct = self.knowledge["ChosenStruct"]
        mymood = int(mystruct["mood"])
        mycompl = int(mystruct["compl"])
        mytempo = int(mystruct["tempo"])*30
        mytempo = max(mytempo, 60)
        print("Tempo: " + str(mytempo))
        mykey = mystruct["key"]
        self.key = mykey
        myscale = mystruct["scale"]
        mygenre = mystruct["genre"]

        copychords = None
        for part in self.knowledge["partobjects"]:
            if "PopPunkChorus" in self.knowledge["partobjects"][part].name:
                copychords = self.knowledge["partobjects"][part].generated_music.__deepcopy__()
                copychords = list(copychords.getElementsByClass(["Part"]))[1].__deepcopy__()
        #copychords.show()

        melodyGenerator = PunkMelody()

        length = 4

        melodyGenerator.chords_music = copychords.__deepcopy__()
        #melodyGenerator.chords_music.show()
        music_melody = melodyGenerator.generate(mykey, mycompl, mytempo, myscale, mymood=mymood, mygenre="Solo", basenotelength=0.5, length=copychords.quarterLength)

        for thisNote in copychords.recurse().notes:  # .getElementsByClass(note.Note):
            thisNote.volume = volume.Volume(velocity=80)
        for thisNote in music_melody.recurse().notes:
            thisNote.volume = volume.Volume(velocity=50)

        music_combined = stream.Stream()
        music_combined.insert(0, music_melody.__deepcopy__())
        music_combined.insert(0, copychords.__deepcopy__())
        self.generated_music = music_combined

