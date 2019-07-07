import random as rn
from Parts.generic_part import generic_part
from music21 import *


# Ohne init in Generators
from Generators.PunkChords import PunkChords
from Generators.PunkMelody import PunkMelody
from Generators.SkaChords import SkaChords



class PopPunkChorus(generic_part):

    def __init__(self, passedknowledge, name):
        super().__init__(passedknowledge, name)
        self.generated_music = None

    def generate(self):


        mystruct = self.knowledge["ChosenStruct"]
        mycompl = int(mystruct["compl"])
        mytempo = int(mystruct["tempo"])*30
        print("Tempo: " + str(mytempo))
        mykey = mystruct["key"]
        self.key = mykey
        myscale = mystruct["scale"]
        mygenre = mystruct["genre"]

        chordGenerator = PunkChords()
        melodyGenerator = PunkMelody()

        length = 4
        #if mycompl == 5:
        #    length == 8

        if mytempo >= 4:
            music_chords = chordGenerator.generate(self.key, mycompl, mytempo, myscale, mygenre="Punk", length = length)
        elif mytempo == 1 or mygenre=="Acoustic" or mygenre=="Ballad":
            music_chords = chordGenerator.generate(self.key, mycompl, mytempo, myscale, mygenre="Acoustic", length = length)
        else:
            music_chords = chordGenerator.generate(self.key, mycompl, mytempo, myscale, mygenre="Rock", length = length)

        melodyGenerator.chords_music = music_chords.__deepcopy__()


        music_melody = melodyGenerator.generate(mykey, mycompl, mytempo, myscale, mygenre="Blink", basenotelength=0.5, length=music_chords.quarterLength)

        for thisNote in music_chords.recurse().notes:  # .getElementsByClass(note.Note):
            print(thisNote)
            thisNote.volume = volume.Volume(velocity=80)
        for thisNote in music_melody.recurse().notes:
            thisNote.volume = volume.Volume(velocity=60)

        music_combined = stream.Stream()
        music_combined.insert(0, music_melody.__deepcopy__())
        music_combined.insert(0, music_chords.__deepcopy__())
        self.generated_music = music_combined


if __name__== "__main__":
    blubb = PopPunkChorus()
    blubb.generate()