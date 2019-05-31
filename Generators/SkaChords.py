import random as rn
from music21 import *
from Generators.Chords_Util import *


class SkaChords:

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
            pattern += pattern
        elif mycompl == 3 or mycompl == 4:
            pattern = pattern + self.generatePattern()
            pattern += pattern
        elif mycompl == 5:
            pattern = pattern + self.generatePattern() + self.generatePattern() + self.generatePattern()
        print("the pattern is: {} with length {} ".format(pattern, len(pattern)))
        if mygenre == "poppunk" or 35 <= mytempo:
            Chords_Util.genChords(mykeyobj, self.chords_music, pattern, 0.125, self.generateBeat(0.125, 1, mygenre, mycompl), [0, 4])
        else:
            Chords_Util.genChords(mykeyobj, self.chords_music, pattern, 0.25, self.generateBeat(0.125, 1, mygenre, mycompl), [0, 2, 4])
        return self.chords_music


    def generateBeat(self, singlechordlength, chordlength, mystyle, mycompl):
        if not(chordlength/singlechordlength).is_integer():
            print("Could not create beat, please have chordlength be a multilple of singlechordlength")
            raise NotImplementedError
        return self.generateSkaBeat(singlechordlength, chordlength, mystyle, mycompl)


    def generateSkaBeat(self, singlechordlength, chordlength, mystyle, mycompl):
        print("generating ska beat")
        sum = 0
        beat = []
        maxlength = chordlength/singlechordlength
        current = 0
        while sum < maxlength:
            if current == 0:
                beat += [0]
                current = 1
            elif current == 1:
                beat += [1]
                current = rn.choice([0,0,0,1])
            sum += 1
        print("the beat is {}".format(beat))
        return beat

    '''def getChord(self, key, basenote, singlechordlength, chordnotes):
        chord_music = stream.Part()
        mychord = chord.Chord(duration=duration.Duration(singlechordlength))
        mypitches = key.pitches
        for i in chordnotes:
               mychord.add(mypitches[(basenote+i)%len(mypitches)])
        return mychord

    def genChords(self, key, pattern, singlechordlength, beat):
            print(pattern)
            for basenote in pattern:
                for singlebeat in beat:
                    if singlebeat == 0:
                        chord_music = note.Rest(duration=duration.Duration(singlechordlength))
                    elif singlechordlength <= 0.125:
                        chord_music = Chords_Util.getChord(key, basenote, singlechordlength*singlebeat, [0, 4])
                    else:
                        chord_music = Chords_Util.getChord(key, basenote, singlechordlength*singlebeat, [0, 2, 4])
                    self.chords_music.append(chord_music.__deepcopy__())'''

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

if __name__ == "__main__":
     blubb = SkaChords()

     mystream = stream.Stream()
     myPart = stream.Part()
     mystream.insert(0, instrument.ElectricGuitar())
     for _ in range(10):
         beat = blubb.generateSkaBeat(0.125, 2, "pop", "nlubdofn")
         print(beat)
         for singlebeat in beat:
             if singlebeat == 0:
                 #mychord = chord.Chord(["C", "G"], duration=duration.Duration(0.25))
                 #mychord.volume = volume.Volume(velocity=45)
                 #mystream.append((mychord))
                 myPart.append(note.Rest(duration=duration.Duration(0.5)))
             else:
                 mychord2 = chord.Chord(["C", "G"], duration=duration.Duration(0.5 * singlebeat))
                 myPart.append((mychord2))
         myPart.append(note.Rest(duration=duration.Duration(8)))


     n = note.Note("A1", type='quarter')
     drumPart = stream.Part()
     drumPart.insert(0, instrument.Woodblock())

     for _ in range(int(myPart.quarterLength)):
         drumPart.append(n.__deepcopy__())



     mystream.insert(0, myPart)
     mystream.insert(0, drumPart)
     #myPart.show()
     #drumPart.show()
     midi.realtime.StreamPlayer(mystream).play()
