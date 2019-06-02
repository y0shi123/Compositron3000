import random as rn
from music21 import *
from Generators.Chords_Util import *
#import Generators.Chords_Util

class PunkChords:

    def __init__(self):
        pass
        self.chords_music = stream.Part()

    def generate(self, mykey = "C", mycompl = 3, mytempo = 4, myscale = "Major", mygenre = "Punk", singlechordlength=0.25, length = 4):

        self.chords_music = stream.Part()
        self.chords_music.append(tempo.MetronomeMark(number=mytempo))
        self.chords_music.append(instrument.ElectricGuitar())
        pattern = self.generatePattern(length=4)
        mykeyobj = key.Key(mykey, myscale)
        self.genAppegioChords(mykeyobj, self.chords_music, pattern, 0.125,
                            self.generateEightsBeat(singlechordlength=0.125, chordlength=1, mygenre=mygenre,
                                                    mycompl=mycompl),
                            [0,2,4,6])
        self.chords_music.append(note.Rest(duration=duration.Duration(2)))
        self.genMutedChords(mykeyobj, self.chords_music, pattern, 0.125,
                       self.generateEightsBeat(singlechordlength=0.125, chordlength=1, mygenre=mygenre, mycompl=mycompl),
                       [0, 4])
        return self.chords_music.__deepcopy__()

    def generateEightsBeat(self, singlechordlength=0.125, chordlength = 1, mygenre = "Punk", mycompl = 3):
        sum = 0
        beat = []
        maxlength = chordlength/singlechordlength
        while sum < maxlength:
            while(True):
                if(sum == (maxlength-1)):
                    x = [1]
                elif(sum < maxlength/2):
                    x = [0, 1, 1, 1, 1, 1, 2, 2]
                else:
                    x = [0, 1, 1, 1, 1, 1, 1, 2]
                currentbeat = rn.choice(x)
                currentbeatvalue = 0
                if currentbeat == 0:
                    currentbeatvalue = 1
                else:
                    currentbeatvalue = currentbeat
                #print("the current sum is {}, the currentbeatvalue is {}, the current maxlength is{}".format(sum, currentbeatvalue, maxlength))
                if sum+currentbeatvalue <= maxlength:
                    beat += [int(currentbeat)]
                    sum += currentbeatvalue
                    break
        return beat

    def genMutedChords(self, key, chords_music, pattern, singlechordlength, beat, notesInChords):
        for basenote in pattern:
            for singlebeat in beat:
                if singlebeat == 0:
                    chord_music = note.Rest(duration=duration.Duration(singlechordlength))
                else:
                    chord_music = self.getChord(key, basenote, singlechordlength*singlebeat, notesInChords)
                    if(singlebeat > 1):
                        chord_music.volume = volume.Volume(velocity=80)
                    else:
                        chord_music.volume = volume.Volume(velocity=50)
                chords_music.append(chord_music)


    def genAppegioChords(self, mykey, chords_music, pattern, singlenotelength, beat, notesInChords):
        muster= []
        while(len(set(muster)) < int(len(notesInChords)/2)):
            muster = []
            skipnext = False
            oldnote = "-1"
            currentnote = "-1"
            for counter, _ in enumerate((range(int(1 / singlenotelength)))):
                if skipnext:
                    skipnext=False
                    continue
                currentnote = str(rn.choice(notesInChords))
                while(currentnote == oldnote):
                    currentnote = str(rn.choice(notesInChords))
                print("currentnote: {} oldnote {}, counter: {} abbruch: {}".format(currentnote, oldnote, counter, int(1/singlenotelength)-1))
                if (rn.choice(range(3)) == 2 and counter != int(1/singlenotelength)-1):
                    muster += [currentnote + "d"]
                    skipnext=True
                else:
                    muster += [currentnote]
                oldnote=currentnote

        print(muster)

        for basenote in pattern:
            #mychord = self.getChord(key, basenote, singlenotelength, notesInChords)
            for singlenote in muster:
                filterednote = int(singlenote[0])
                mynotename = mykey.pitches[(filterednote+basenote)%7]
                if (filterednote+basenote>6):
                    mynotename.octave = mynotename.implicitOctave +1
                mynotename.octave += rn.choice([0, 0, 0, 0])
                if "d" in singlenote:
                    mynote = note.Note(mynotename, duration=duration.Duration(singlenotelength*2))
                else:
                    mynote = note.Note(mynotename, duration=duration.Duration(singlenotelength))
                chords_music.append(mynote)
        return chords_music

    def getChord(self, key, basenote, singlechordlength, chordnotes):
        mychord = chord.Chord(duration=duration.Duration(singlechordlength))
        mypitches = key.pitches
        for i in chordnotes:
               #mychord.add(mypitches[(basenote+i)%len(mypitches)])
               mypitch = mypitches[(basenote + i) % 7]
               if basenote+i > 6:
                   mypitch.octave += 1
               mychord.add(mypitch)
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
                break
            else:
                chords=[]
        print("pattern: {}".format(chords))
        return chords

    def printtestpattern(self):
        for _ in range(10):
            print(self.generatePattern())



if __name__ == "__main__":
    # {'mood': '3', 'compl': '1', 'tempo': '2', 'parts': 'Chorus, Chorus', 'genre': 'pop', 'key': 'C', 'scale': 'dorian'}
    #def generate(self, mykey, mycompl, mytempo, myscale, mygenre, singlechordlength=0.25):

    foo = PunkChords()
    bar = foo.generate('C', 4, 40, "Major", "Punk" )
    bar.show()
    midi.realtime.StreamPlayer(bar).play()

