import random as rn
from music21 import *
from Generators.Chords_Util import *
#import Generators.Chords_Util

class PopChords:

    def __init__(self):
        self.chords_music = stream.Part()

    def generate(self, mykey, mycompl, mytempo, myscale, mygenre, singlechordlength=0.25):

        self.chords_music = stream.Part()
        self.chords_music.append(tempo.MetronomeMark(number=mytempo))

        pattern = self.generatePattern(length=4)
        #print(mykey + " " + myscale)
        mykeyobj = key.Key(mykey, myscale)

        if mycompl == 1 or mycompl == 2:
            pattern = pattern*2
            pattern += pattern
        elif mycompl == 3 or mycompl == 4:
            pattern = pattern + self.generatePattern()
            pattern += pattern
        elif mycompl == 5:
            pattern = pattern + self.generatePattern() + self.generatePattern() + self.generatePattern()
        #print("the pattern is: {} with length {} ".format(pattern, len(pattern)))
        if mygenre == "poppunk" or 40 <= mytempo:
            self.chords_music.append(Chords_Util.genChords(mykeyobj, pattern, 0.125,  self.generateBeat(0.125, 1, mygenre, mycompl),[0,2]))
        else:
            self.chords_music.append(Chords_Util.genChords(mykeyobj, pattern, 0.25, self.generateBeat(0.25, 1, mygenre,mycompl),[0,2,4]))
        return self.chords_music

    def generateBeat(self, singlechordlength, chordlength, mystyle, mycompl):
        if not(chordlength/singlechordlength).is_integer():
            print("Could not create beat, please have chordlength be a multilple of singlechordlength")
            raise NotImplementedError
        return self.generateGenericBeat(singlechordlength, chordlength, mystyle, mycompl)


    def generateGenericBeat(self, singlechordlength, chordlength, mystyle, mycompl):
        #print("generating generic beat")
        sum = 0
        beat = []
        maxlength = chordlength/singlechordlength
        while sum < maxlength:
            while(True):
                currentbeat = rn.choice([0,0, 0 , 0, 1, 1, 1, 1, 2, 2, 2, 2, 4, 4, 8])
                currentbeatvalue = 0
                if currentbeat == 0:
                    currentbeatvalue = 1
                else:
                    currentbeatvalue = currentbeat
                #print("the current sum is {}, the currentbeatvalue is {}, the current maxlength is{}".format(sum, currentbeatvalue, maxlength))
                if sum+currentbeatvalue <= maxlength:
                    beat += [int(currentbeat)]
                    sum  += currentbeatvalue
                    break
        #print("the beat is {}".format(beat))
        return beat

    '''
    def genChords(self, key, pattern, singlechordlength, beat):
        print(pattern)
        for basenote in pattern:
            for singlebeat in beat:
                if singlebeat == 0:
                    chord_music = note.Rest(duration=duration.Duration(singlechordlength))
                elif singlechordlength <= 0.125:
                    chord_music = self.getChord(key, basenote, singlechordlength*singlebeat, [0, 4])
                else:
                    chord_music = self.getChord(key, basenote, singlechordlength*singlebeat, [0, 2, 4])
                self.chords_music.append(chord_music.__deepcopy__())

    def getChord(self, key, basenote, singlechordlength, chordnotes):
        chord_music = stream.Part()
        mychord = chord.Chord(duration=duration.Duration(singlechordlength))
        mypitches = key.pitches
        for i in chordnotes:
               mychord.add(mypitches[(basenote+i)%len(mypitches)])
        return mychord'''


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
                break
            else:
                chords=[]
        return chords