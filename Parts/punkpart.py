import random as rn
from Parts.generic_part import generic_part
from music21 import *


# Ohne init in Generators
from Generators.PunkChords import PunkChords
from Generators.PunkMelody import PunkMelody
from Generators.SkaChords import SkaChords



class PunkPart(generic_part):

    def __init__(self, passedknowledge, name):
        super().__init__(passedknowledge, name)


    def generate(self):
        #{'mood': '3', 'compl': '1', 'tempo': '2', 'parts': 'Chorus, Chorus', 'genre': 'pop', 'key': 'C', 'scale': 'dorian'}

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

        music_chords = chordGenerator.generate(self.key, mycompl, mytempo, myscale, mygenre)
        melodyGenerator.chords_music = music_chords.__deepcopy__()

        music_chords.write('midi', "JustChords.mid")

        #melodyGenerator.melody_music.insert(0, key.Key(mykey))
        print(music_chords.quarterLength)
        music_melody = melodyGenerator.generate(mykey, mycompl, mytempo, myscale, mygenre, basenotelength=0.5, length=music_chords.quarterLength)

        music_melody.write('midi', "JustTheMelody.mid")

        music_combined = stream.Stream()
        music_combined.insert(0, music_melody.__deepcopy__())
        music_combined.insert(0, music_chords.__deepcopy__())

        #music_chords.show()

        music_combined.write('midi', "PunkPart.mid")

        '''
        music_chords2 = chordGenerator.generate(mykey, mycompl, mytempo, myscale, mygenre)
        for thisNote in music_chords2.recurse().notes:  # .getElementsByClass(note.Note):
            thisNote.volume = volume.Volume(velocity=45)

        music_melody2 = melodyGenerator.generate(mykey, mycompl, mytempo, myscale, mygenre, length=music_chords2.quarterLength, basenotelength=rn.choice([0.125, 0.25]))
        for thisNote in music_melody2.recurse().notes:
            thisNote.volume = volume.Volume(velocity=80)


        music_combined2 = stream.Stream()
        music_combined2.insert(0, music_melody2)
        music_combined2.insert(0, music_chords2)

        music_total = stream.Stream()
        chordacc = stream.Part()
        melodyacc = stream.Part()
        count = 0
        for songpart in [music_combined, music_combined2, music_combined.__deepcopy__()]:
            for singlemeasure in songpart.getElementsByClass(stream.Part).stream():
                print(singlemeasure)
                if (count % 2 == 0):
                    chordacc.append(singlemeasure.__deepcopy__())
                else:
                    melodyacc.append(singlemeasure.__deepcopy__())
                count = count + 1
        music_total.append(chordacc)
        music_total.append(melodyacc)
        music_total.show()'''


if __name__== "__main__":
    blubb = PunkPart()
    blubb.generate()