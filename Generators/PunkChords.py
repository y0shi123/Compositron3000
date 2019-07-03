import random as rn
from music21 import *
from Generators.Chords_Util import *
#import Generators.Chords_Util
#environment.set("musicxmlPath", r"C:\Program Files (x86)\tuxguitar-1.5.2\tuxguitar.exe")
environment.set("musicxmlPath", r"C:\Program Files\MuseScore 3\bin\MuseScore3.exe")


class PunkChords:

    def __init__(self):
        pass
        self.chords_music = stream.Part()


    def generate(self, mykey = "C", mycompl = 3, mytempo = 120, myscale = "Major", mygenre = "Punk", singlechordlength=0.50, length = 8):

        self.chords_music = stream.Part()
        treble = clef.TrebleClef()
        self.chords_music.insert(0, treble)
        self.chords_music.append(tempo.MetronomeMark(number=mytempo))
        #self.chords_music.append(instrument.ElectricGuitar())
        pattern = self.generatePattern(length=length/2)
        #pattern += pattern
        mykeyobj = key.Key(mykey, myscale)
        self.key = mykeyobj
        self.chords_music.insert(0, self.key)

        #self.genAppegioChords(mykey=mykeyobj, chords_music=self.chords_music, pattern=pattern,
        #                      singlenotelength=0.125, length = 4,
        #                     notesInChords=[0,2,4,6])
        #print("Länge nach Appegio: {}".format(self.chords_music.quarterLength))
        #self.chords_music.append(note.Rest(duration=duration.Duration(2)))
        #self.chords_music.append(instrument.ElectricGuitar())


        #chordlength = anzahl der takte die der akkord spielen soll, singlechordlength = wie klein sind die einzelnen akkorde innerhalb dieses zeitraums.
        # bzw scl = 0.125, cl = 1 könnte 8 acht achtel ergeben
        #self.genMutedChords(self.key, self.chords_music, pattern, singlechordlength,
        #               self.generateEightsBeat(singlechordlength=singlechordlength, chordlength=4, mygenre=mygenre, mycompl=mycompl),
        #               [0, 4])

        #self.chords_music.append(note.Rest(duration=duration.Duration(2)))
        self.genRockChords(mykeyobj, self.chords_music, pattern, 0.5,
                       self.generateRockBeat(singlechordlength=0.5, chordlength=4, mygenre=mygenre, mycompl=mycompl),
                       [0, 4])
        return self.chords_music.__deepcopy__()

#\    def genRockChords(self, key, chords_music, pattern, singlechordlength, beat, notesInChords):



    def generateEightsBeat(self, singlechordlength=0.5, chordlength = 4, mygenre = "Punk", mycompl = 3):
        sum = 0
        beat = []
        maxlength = chordlength/singlechordlength
        while sum < maxlength:
            while(True):
                if(sum == (maxlength-1)):
                    x = [1]
                elif(sum < maxlength/2):
                    x = [0, 1, 1, 1, 1, 2, 2, 2]
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


    def generateRockBeat(self, singlechordlength= 0.5, chordlength=4, mygenre="punk", mycompl=3):
        #print("generating generic beat")
        sum = 0
        beat = []
        maxlength = int(chordlength/singlechordlength)
        while sum < maxlength:
            while(True):
                x = [0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 4, 4, 8]
                #x = [0,1]
                #x = [0,0,0,1]
                currentbeat = rn.choice(x)
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
        print("the beat is {}".format(beat))
        return beat


    def genMutedChords(self, key, chords_music, pattern, singlechordlength, beat, notesInChords):
        for basenote in pattern:
            for singlebeat in beat:
                if singlebeat == 0:
                    chord_music = note.Rest(duration=duration.Duration(singlechordlength))
                else:
                    if not ";" in str(basenote):
                        basenote = int(basenote)
                        chord_music = self.getChord(key, basenote, singlechordlength*singlebeat, notesInChords)
                    else:
                        whichone = rn.choice([0,0,0,1])
                        currentbasenote = -1
                        if whichone == 0:
                            if "-" in basenote.split(";")[0]:
                                currentbasenote = int(basenote[1:3])
                            else:
                                currentbasenote = int(basenote[1])
                        else:
                            if "-" in basenote.split(";")[1]:
                                currentbasenote = int(basenote.split(";")[1][0:2])
                            else:
                                currentbasenote = int(basenote.split(";")[1][0])
                        #print("basenote: {}".format(currentbasenote))
                        chord_music = self.getChord(key, currentbasenote, singlechordlength * singlebeat, notesInChords)

                    if(singlebeat > 1):
                        chord_music.volume = volume.Volume(velocity=80)
                    else:
                        chord_music.volume = volume.Volume(velocity=40)
                chords_music.append(chord_music)


    def genAppegioChords(self, mykey, chords_music, pattern, singlenotelength, length, notesInChords):
        print("Länge: {}, SingleNoteLänge: {} Bruch: {}".format(length, singlenotelength, int(length/singlenotelength)))
        muster= []
        while(len(set(muster)) < int(len(notesInChords)/2)):
            muster = []
            skipnext = False
            oldnote = "-1"
            currentnote = "-1"
            for counter, _ in enumerate((range(int(length / singlenotelength)))):
                if skipnext:
                    skipnext=False
                    continue
                currentnote = str(rn.choice(notesInChords))
                while(currentnote == oldnote and rn.choice([0,1]) == 1):
                    currentnote = str(rn.choice(notesInChords))
                #print("currentnote: {} oldnote {}, counter: {} abbruch: {}".format(currentnote, oldnote, counter, int(1/singlenotelength)-1))
                if (rn.choice(range(3)) == 2 and counter != int(length/singlenotelength)-1):
                    muster += [currentnote + "d"]
                    skipnext=True
                else:
                    muster += [currentnote]
                oldnote=currentnote

        print(muster)

        for basenote in pattern:
            if not ";" in str(basenote):
                currentbasenote = int(basenote)
            else:
                if "-" in basenote.split(";")[0]:
                    currentbasenote = int(basenote[1:3])
                else:
                    currentbasenote = int(basenote[1])

            for singlenote in muster:
                filterednote = int(singlenote[0])
                mynotename = mykey.pitches[(filterednote+currentbasenote)%7]
                if (filterednote+currentbasenote>6):
                    mynotename.octave = mynotename.implicitOctave +1
                #mynotename.octave += rn.choice([0, 0, 0, 0])
                if "d" in singlenote:
                    mynote = note.Note(mynotename, duration=duration.Duration(singlenotelength*2))
                else:
                    mynote = note.Note(mynotename, duration=duration.Duration(singlenotelength))
                mynote.pitch.octave-=1
                chords_music.append(mynote)
        return chords_music

    def genRockChords(self, key, chords_music, pattern, singlechordlength, beat, notesInChords):
        for basenote in pattern:
            for singlebeat in beat:
                if singlebeat == 0:
                    chord_music = note.Rest(duration=duration.Duration(singlechordlength))
                else:

                    if not ";" in str(basenote):
                        currentbasenote = int(basenote)
                        chord_music = self.getChord(key, currentbasenote, singlechordlength * singlebeat, notesInChords)
                    else:
                        whichone = rn.choice([0, 1])
                        currentbasenote = -1
                        if whichone == 0:
                            if "-" in basenote.split(";")[0]:
                                currentbasenote = int(basenote[1:3])
                            else:
                                currentbasenote = int(basenote[1])
                        else:
                            if "-" in basenote.split(";")[1]:
                                currentbasenote = int(basenote.split(";")[1][0:2])
                            else:
                                currentbasenote = int(basenote.split(";")[1][0])
                    chord_music = self.getChord(key, currentbasenote, singlechordlength*singlebeat, notesInChords)
                chords_music.append(chord_music)


    def getChord(self, key, basenote, singlechordlength, chordnotes):
        mychord = chord.Chord(duration=duration.Duration(singlechordlength))
        mypitches = key.pitches
        for i in chordnotes:
               #mychord.add(mypitches[(basenote+i)%len(mypitches)])
               mypitch = mypitches[(basenote + i) % 7]
               #mypitch.octave -= 1
               if basenote+i > 6:
                   mypitch.octave += 1
               mypitch.octave -= 1
               mychord.add(mypitch)
        return mychord


    def generatePattern(self, length=4, mycompl=3):
        chords = []
        while (True):
            currentchord = -1
            counter = 0
            while (counter < length):
                newchord = rn.choice([0, 3, 4, 5])
                if (newchord != currentchord):
                    if(rn.choice(range(mycompl+1)) < mycompl and rn.choice([0,1]) == 1):
                        chords += ["(" + str(newchord) + ";" + str(newchord+int(rn.choice([-1, -2, +1, +2]))) + ")"]
                    else:
                        chords += [str(newchord)]
                    currentchord = newchord
                    counter += 1
            replaceChord = rn.choice(range(0, 3))
            replaceInterval = rn.choice([2, -2])
            try:
                chords[replaceChord] = str((int(chords[replaceChord]) + replaceInterval) % 7)
            except:
                pass
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
    for i in range(5):
        bar = foo.generate('C', 4, 40, "Major", "Punk" )
        print("Länge: {}".format(bar.quarterLength))
        #bar.show()
        #midi.realtime.StreamPlayer(bar).play()
        fp = bar.write('midi', "bla{}.mid".format(i))