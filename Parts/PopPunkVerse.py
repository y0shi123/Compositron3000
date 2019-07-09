import random as rn
from Parts.generic_part import generic_part
from music21 import *


# Ohne init in Generators
from Generators.PunkChords import PunkChords
from Generators.PunkMelody import PunkMelody


class PopPunkVerse(generic_part):

    def __init__(self, passedknowledge, name):
        super().__init__(passedknowledge, name)
        self.generated_music = None

    def generate(self):

        mystruct = self.knowledge["ChosenStruct"]
        mycompl = int(mystruct["compl"])
        mytempo = int(mystruct["tempo"])*30
        mytempo = max(mytempo, 60)
        print("Tempo: " + str(mytempo))
        mykey = mystruct["key"]
        self.key = mykey
        myscale = mystruct["scale"]
        mygenre = mystruct["genre"]

        chordGenerator = PunkChords()
        melodyGenerator = PunkMelody()

        length = 4
        if mycompl == 5:
            length == 8

        if mytempo >= 110:
            music_chords = chordGenerator.generate(self.key, mycompl, mytempo, myscale, mygenre="Punk", length = length)
        elif mytempo <= 70 or mygenre=="Acoustic" or mygenre=="Ballad":
            music_chords = chordGenerator.generate(self.key, mycompl, mytempo, myscale, mygenre="Acoustic", length = length)
        else:
            music_chords = chordGenerator.generate(self.key, mycompl, mytempo, myscale, mygenre="Rock", length = length)

        music_chords.write('midi', "JustTheChords.mid")

        melodyGenerator.chords_music = music_chords.__deepcopy__()


        music_melody = melodyGenerator.generate(mykey, mycompl, mytempo, myscale, mygenre="Solo", basenotelength=1, length=music_chords.quarterLength)
        music_melody.write('midi', "JustTheMelody.mid")

        for thisNote in music_chords.recurse().notes:  # .getElementsByClass(note.Note):
            #print(thisNote)
            thisNote.volume = volume.Volume(velocity=80)
        for thisNote in music_melody.recurse().notes:
            thisNote.volume = volume.Volume(velocity=50)

        music_combined = stream.Stream()
        music_combined.insert(0, music_melody.__deepcopy__())
        music_combined.insert(0, music_chords.__deepcopy__())
        music_combined = self.flatappend(music_combined, music_combined.__deepcopy__())
        self.generated_music = music_combined

