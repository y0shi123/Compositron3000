import random as rn
from music21 import *

class PopChords:

    def __init__(self):
        self.chords_music = stream.Part()

    def generate(self, mykey, mycompl, mytempo, myscale, mygenre):

        self.chords_music = stream.Part()
        self.chords_music.append(tempo.MetronomeMark(number=mytempo))

        pattern = self.generatePattern(length=4)
        print(mykey + " " + myscale)
        mykeyobj = key.Key(mykey, myscale)

        if mycompl == 1 or mycompl == 2:
            pattern = pattern*2
        elif mycompl == 3 or mycompl == 4:
            pattern = pattern + self.generatePattern()
        elif mycompl < 5 and mytempo < 40:
            pattern += pattern
        elif mycompl == 5:
            pattern = pattern + self.generatePattern() + self.generatePattern() + self.generatePattern()
        print(mycompl)
        if mygenre == "poppunk" or 40 <= mytempo:
            self.genChords(mykeyobj, pattern, 0.125, 1)
        else:
            self.genChords(mykeyobj, pattern, 0.25, 1)
        return self.chords_music

    def genChords(self, key, pattern, singlechordlength, chordlength):
        print(pattern)
        for basenote in pattern:
            repeat = int(chordlength/singlechordlength)
            if singlechordlength <= 0.125:
                chord_music = self.getChord(key, basenote, singlechordlength, [0,4])
            else:
                chord_music = self.getChord(key, basenote, singlechordlength, [0,2,4])
            for _ in range(repeat):
                self.chords_music.append(chord_music.__deepcopy__())


    def getChord(self, key, basenote, singlechordlength, chordnotes):
        chord_music = stream.Part()
        mychord = chord.Chord(duration=duration.Duration(singlechordlength))
        mypitches = key.pitches
        for i in chordnotes:
               mychord.add(mypitches[(basenote+i)%len(mypitches)])
        return mychord


    def generatePattern(self, length=4):
        chords = []
        while (True):
            currentchord = -1
            counter = 0
            while (counter < length):
                newchord = rn.choice([0, 3, 4, 5])
                if (newchord != currentchord):
                    chords += [newchord]
                    currentchord = newchord
                    counter += 1
            replaceChord = rn.choice(range(0, 3))
            replaceInterval = rn.choice([2, -2])
            chords[replaceChord] = (chords[replaceChord] + replaceInterval) % 7
            if (len(set(chords)) > 2):
                print(chords)
                break
        return chords