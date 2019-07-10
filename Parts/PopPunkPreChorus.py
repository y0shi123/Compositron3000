import random as rn
from Parts.generic_part import generic_part
from music21 import *


# Ohne init in Generators
from Generators.PunkChords import PunkChords
from Generators.PunkMelody import PunkMelody
from Generators.SkaChords import SkaChords



class PopPunkPreChorus(generic_part):

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
        #self.key = mykey
        myscale = mystruct["scale"]
        mygenre = mystruct["genre"]

        chordGenerator = PunkChords()
        melodyGenerator = PunkMelody()

        length = 4

        if mytempo >= 110:
            music_chords = chordGenerator.generate(mykey, mycompl, mytempo, myscale, mygenre="Punk", length = length)
        elif mytempo <= 70 or mygenre=="Acoustic" or mygenre=="Ballad":
            music_chords = chordGenerator.generate(mykey, mycompl, mytempo, myscale, mygenre="Acoustic", length = length)
        else:
            music_chords = chordGenerator.generate(mykey, mycompl, mytempo, myscale, mygenre="Rock", length = length)

        melodyGenerator.chords_music = music_chords.__deepcopy__()

        music_melody = stream.Part()
        mykeyobj = key.Key(mykey, myscale)
        treble = clef.TrebleClef()
        music_melody.insert(0, mykeyobj.__deepcopy__())
        music_melody.insert(0, treble)
        music_melody.insert(0, tempo.MetronomeMark(number=mytempo))
        music_melody.insert(0, note.Rest(duration=duration.Duration(music_chords.quarterLength)))

        for thisNote in music_chords.recurse().notes:  # .getElementsByClass(note.Note):
            thisNote.volume = volume.Volume(velocity=80)

        music_combined = stream.Stream()
        music_combined.insert(0, music_melody.__deepcopy__())
        music_combined.insert(0, music_chords.__deepcopy__())
        self.generated_music = music_combined


if __name__== "__main__":
    blubb = PopPunkPreChorus()
    blubb.generate()
    blubb.generated_music.show()