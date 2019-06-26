from music21 import *
import random as rn

class PunkMelody:

    def __init__(self):
        self.basenote = 0
        self.useparsedmelodys = True
        self.noteusage= {"A":0,
                         "B": 0,
                         "C": 0,
                         "D":0,
                         "E":0,
                         "F":0,
                         "G":0}
        self.melody_music = stream.Part()
        self.chords_music = None
        self.usedmelodys = []
        self.melodys = ["bd,  , +2d, , +rh, -rh, +r, b",
                        "bh, rh, +r, -r"]
        '''[
            "bd,  , rd, , +2, +4, -2d, ",
            "b, r,+2,+4,b,+4,-2,0",
            "bd, ,+2d, ,+4d, ,rd, ",


            {"b, rh, +r , -r"]
            
        self.melodys = [
             "+0, +2, +4, +6",
             "0, 2, 4, 6",
             "+2, +4, +2, +6",
             "2, 4, 5, 2",
             "2, p, 5, p",
             "+2, +4",
             "2, r",
             "2, r",
             "+3, +4",
             "+1, +4",
             "+3, -2",
             "+6, -4",
             "+1, 0",
             "+1, 0, +1, 0",
             "4, 0, 7, 0",
             "4, 2, 5, 4",
             "r, 2",
             "r, 2",
             "2, p, 7, p",
             "p, p, p, p",
             "p, p, p, p",
             "p, p",
             "0,0",
             "0, r, 0, r",
             "r, r",
             "0 ,r, r, 0, 2, 4, r",
             "0, p, 0, p",
             "0",
             "p",
             "p",
             "p",
             "+0, +2, +4, +2, +5, +4, +2, +4",
             "r,r,r,r,r,r,r,r",
             "r,p,r,p,0,2,4,p",
             "+0, +2, +4, +2, +5, +4, +2, +4, +0, +2, +4, +2, +5, +4, +2, +4",
             "+0, +2, +4, +2, +5, +4, +2, +4, +0, +2, +4, +2, +5, +4, +2, +4,+0, +2, +4, +2, +5, +4, +2, +4, +0, +2, +4, +2, +5, +4, +2, +4",
        ]'''

    def currentchord(self, offset = 4, position=None):
        if self.chords_music is None or self.chords_music.getElementsByClass("Chord") is None:
            print("No Chords found in Punkmelody")
            return None

        currentchord = None
        if position is None:
            position=self.melody_music.quarterLength

        for elem in self.chords_music.getElementsByClass("Chord"):
            #print("CurrentChordTest - Melody QL: {}, currentchordoffset: {}".format(position, elem.getOffsetBySite(self.chords_music)))
            if(elem.getOffsetBySite(self.chords_music)+elem.duration.quarterLength > position):
                currentchord = elem.__deepcopy__()
                #print("Returning: " + str(currentchord))
                return currentchord
        print("No Chord found")

    def currentNoteIndex(self, position=None):
        if self.melody_music is None:
            print("No Chords found in Punkmelody")
            return None
        if  self.melody_music.getElementsByClass("Note") is None:
            return "0"

        if position is None:
            position=self.melody_music.quarterLength

        for elem in self.melody_music.getElementsByClass("Note"):
            #print(str(elem) + str(elem.getOffsetBySite(self.melody_music)) + ", " + str(position))
            if(elem.getOffsetBySite(self.melody_music) + elem.duration.quarterLength >= position):
                mycurrentnote = elem.__deepcopy__()
                for index, pitch in enumerate(self.key.pitches):
                    if pitch.name == mycurrentnote.name:
                        return index
        print("ERROR :( :( :( ")
        exit(0)


    def currentNoteObject(self, position=None):
        if self.melody_music is None:
            print("No Chords found in Punkmelody")
            return None
        if  self.melody_music.getElementsByClass("Note") is None:
            return "0"

        if position is None:
            position=self.melody_music.quarterLength
        previousNote = None
        for elem in self.melody_music.getElementsByClass("Note"):
            #print(str(elem) + str(elem.getOffsetBySite(self.melody_music)) + ", " + str(position))
            if(elem.getOffsetBySite(self.melody_music) + elem.duration.quarterLength > position):
                return  elem
            previousNote = elem
        print("ERROR :( :( :( ")
        exit(0)

    def followthechords(self):
        currentchord = self.currentchord()
        while (currentchord != None):
            print(currentchord)
            mynote = note.Note(rn.choice(currentchord.pitches).name, duration=duration.Duration(0.25))
            #mynote.transpose(interval.Interval(rn.choice([0, 2, -2])), inPlace=True)
            self.melody_music.append(mynote)
            self.melody_music.append(mynote.transpose(interval.Interval(rn.choice([0, 2, -2])))
            )
            currentchord = self.currentchord()

    def generateSimpleMelodyPattern(self, length, basenotelength):
        if 1 > length:
           print("ERROR")
           exit(1)
        if length == 4:
            return "4"
        elif length*basenotelength > 4:
                results = ["2,2"]
                '''         ,"2,2","2,2",
                           "4,4,4,4",
                           "4,4,2",
                           "4,2,4",
                           "2,4,4"]'''
        else:
                results = ["1"]
                '''    ,
                           "1",
                           "1"
                           "2,2",
                           "2,2"]
                '''
        res = rn.choice(results)
        # print(res)
        if res == "1":
            return str(length)
        else:
            bla = ""
            for entry in res.split(","):
                if (rn.randint(0, 6) <= 4 and length <= 8) :
                   bla = bla + str(int(length / int(entry))) + ","
                else:
                   bla = bla + self.generateSimpleMelodyPattern(int(length / int(entry)), basenotelength=basenotelength) + ","
            return bla[:-1]

    def generateMelody(self, mykey, mycompl, mytempo, myscale, mygenre, length, pattern, singlenotelength=0.5):

        for patternentry in pattern.split(","):

            #print(patternentry)
            currentbasenotelength = singlenotelength
            matchinglength = list(filter(lambda x: len(x.split(",")) == int(patternentry), self.melodys))
            usedmelodysmatchinglength = list(filter(lambda x: len(x.split(",")) == int(patternentry), self.usedmelodys))
            #print(matchinglength)
            #print(self.usedmelodys)
            #print(usedmelodysmatchinglength)



            if len(matchinglength) == 0 and len(usedmelodysmatchinglength) == 0:
                print("Cant create melody of this length, exiting")
                exit(0)

            if (len(usedmelodysmatchinglength) != 0 and rn.randint(0,5) > len(usedmelodysmatchinglength)):

                chosenmelody = rn.choice(usedmelodysmatchinglength)
                #if(len(chosenmelody.split(",")) > 2):
                print("Reusing Melodys " + str(chosenmelody))

            else:
                chosenmelody = rn.choice(matchinglength)
            if (not self.useparsedmelodys):
                self.usedmelodys += [chosenmelody]

            print("The chosen melody is         : " + str(chosenmelody))
            parsedchosenmelody = ""
            skipnext = False
            for index, melodyentry in enumerate(chosenmelody.split(",")):
                multiply = 1
                if skipnext:
                    skipnext=False
                    parsedchosenmelody += " ,"
                    continue
                if "d" in melodyentry:
                    multiply = 2
                    melodyentry=melodyentry[:-1]
                    skipnext = True
                if "h" in melodyentry:
                    multiply = 0.5
                    melodyentry=melodyentry[:-1]

                if "b" in melodyentry:
                    #print("Timing: {}, Current Chord: {} with length:{}".format(self.melody_music.quarterLength, self.currentchord(), self.currentchord().duration))
                    parsedmelodyentry = self.keypitchnames().index(self.currentchord(offset=1).pitches[0].name)
                    mynote = note.Note(mykey.pitches[int(parsedmelodyentry)],
                                       duration=duration.Duration(singlenotelength))
                    parsedchosenmelody+=" b"
                elif "p" in melodyentry:
                    mynote = note.Rest(duration=duration.Duration(singlenotelength))
                    parsedchosenmelody += " p"
                elif "r" in melodyentry and not ("+" in melodyentry or "-" in melodyentry):
                    parsedmelodyentry = rn.choice(range(7))
                    mynote = note.Note(mykey.pitches[parsedmelodyentry],
                                       duration=duration.Duration(singlenotelength))
                    parsedchosenmelody += " " + str(parsedmelodyentry)
                elif "+" in melodyentry:
                    if "r" in melodyentry:
                        parsedmelodyentry = self.currentNoteIndex()
                        randint = rn.randint(0,6)
                        mynote = note.Note(self.key.pitches[(parsedmelodyentry + randint) % 7],
                                           duration=duration.Duration(singlenotelength))
                        if (parsedmelodyentry + randint > 6):
                            mynote.octave = mynote.octave + 1
                        parsedchosenmelody += " +" + str(randint)
                    else:
                        parsedmelodyentry = self.currentNoteIndex()
                        mynote = note.Note(self.key.pitches[(parsedmelodyentry + int(melodyentry[-1])) % 7],
                                           duration=duration.Duration(singlenotelength))
                        if(parsedmelodyentry + int(melodyentry[-1]) > 6):
                            mynote.octave = mynote.octave+1
                        parsedchosenmelody += " +" + melodyentry[-1]
                    #parsedchosenmelody += str((parsedmelodyentry + int(melodyentry[-1])) % 7)
                elif "-" in melodyentry:
                    if "r" in melodyentry:
                        parsedmelodyentry = self.currentNoteIndex()
                        randint = rn.randint(0,6)
                        mynote = note.Note(self.key.pitches[(parsedmelodyentry - randint) % 7],
                                           duration=duration.Duration(singlenotelength))
                        if (parsedmelodyentry - randint > 6):
                            mynote.octave = mynote.octave - 1
                        parsedchosenmelody += " -" + str(randint)
                    else:
                        parsedmelodyentry = self.currentNoteIndex()
                        mynote = note.Note(self.key.pitches[(parsedmelodyentry - int(melodyentry[-1])) % 7],
                                          duration=duration.Duration(singlenotelength))
                        if (parsedmelodyentry - randint > 6):
                            mynote.octave = mynote.octave - 1
                        parsedchosenmelody += " -" + melodyentry[-1]
                        #parsedchosenmelody += str((parsedmelodyentry - int(melodyentry[-1])) % 7)
                else:
                    mynote = note.Note(self.key.pitches[int(melodyentry)],
                                       duration=duration.Duration(singlenotelength))
                    parsedchosenmelody += str(melodyentry)
                mynote.duration.quarterLength *= multiply

                if multiply == 2:
                    parsedchosenmelody += "d"
                if multiply == 0.5:
                    parsedchosenmelody += "h"
                    self.melody_music.append(mynote.__deepcopy__())
                self.melody_music.append(mynote)
                parsedchosenmelody += ","
                #print(parsedchosenmelody)
            print("the complete parsed melody is:" + str(parsedchosenmelody))
            if self.useparsedmelodys:
                self.usedmelodys += [parsedchosenmelody[:-1]]
            print("#################################################")
        return self.melody_music

    def generateWalkMelody(self, mykey, mycompl, mytempo, myscale, mygenre, length, singlenotelength):
        notesToUse = [1,2,4,5,6]
        currentNoteValue = rn.choice(notesToUse)
        steps = [0]
        steps = [1,1,1,1,2,3,4]
        direction = 1

        while (self.melody_music.quarterLength < length):
            if(rn.randint(0,5) == 5 and self.melody_music.quarterLength + singlenotelength < self.chords_music.quarterLength ):
                self.melody_music.append(note.Rest(duration=duration.Duration(singlenotelength)))

            step = 0
            if(rn.randint(0,3) == 3):
                step = rn.choice(steps)
            currentNoteValue = ((currentNoteValue + direction * step) % 7)
            currentNote =(note.Note(mykey.pitches[currentNoteValue].name, duration=duration.Duration(singlenotelength)))
            if (rn.randint(0,10) < 4):
                direction*= -1
            if self.melody_music.quarterLength + singlenotelength*2 <= self.chords_music.quarterLength and rn.randint(0,3) == 3:
                pass
                #currentNote.duration.quarterLength*=2
            elif(self.melody_music.quarterLength + singlenotelength/2 == self.chords_music.quarterLength):
                currentNote.duration.quarterLength/=2
            #print("currentnote will be: {} with length: {}".format(currentNoteValue, currentNote.duration.quarterLength))
            self.melody_music.append(currentNote)
        self.connectChords(singlenotelength)
        return self.melody_music

    def connectChords(self, singlenoteLength):
        allpitches = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
        keychords = []

        for chord in self.chords_music.getElementsByClass("Chord"):
            #print(chord.getOffsetBySite(self.chords_music))
            if(chord.getOffsetBySite(self.chords_music)% 4 == 0 and not chord.getOffsetBySite(self.chords_music) >= self.melody_music.quarterLength):
                keychords += [chord]
        print(keychords)

        for index, chord in enumerate(keychords):

            if index==0:
                continue
            foundsomething = False
            predecessor = keychords[index-1]

            for currentpitch in chord.pitches:
                for oldpitch in predecessor.pitches:
                    if allpitches.index(currentpitch.name) == (allpitches.index(oldpitch.name)-1)%12:
                        print(str(chord) + " und " + str(predecessor) + " sind verbunden durch :" + str(currentpitch) + " und " + str(oldpitch))
                        foundsomething = True
                        currentNote = self.currentNoteObject(position = chord.getOffsetBySite(self.chords_music))
                        oldNote     = self.currentNoteObject(position =chord.getOffsetBySite(self.chords_music)-0.001 )
                        if (currentNote is not oldNote):
                            currentNote.pitch = currentpitch
                            oldNote.pitch = oldpitch
                    if foundsomething:
                        break
                    if allpitches.index(currentpitch.name) == (allpitches.index(oldpitch.name)+1)%12:
                        print(str(chord) + " und " + str(predecessor) + " sind verbunden durch :" + str(currentpitch) + " und " + str(oldpitch))
                        foundsomething = True
                        currentNote = self.currentNoteObject(position = chord.getOffsetBySite(self.chords_music))
                        oldNote     = self.currentNoteObject(position =chord.getOffsetBySite(self.chords_music)-0.001 )
                        if (currentNote is not oldNote):
                            currentNote.pitch = currentpitch
                            oldNote.pitch = oldpitch

                    if foundsomething:
                       break
                if foundsomething:
                    break

    def generate(self, mykey, mycompl, mytempo, myscale, mygenre, length, basenotelength=0.5 ):
        self.melody_music = stream.Part()
        self.key = key.Key(mykey, myscale)
        treble = clef.TrebleClef()
        self.melody_music.insert(0, treble)
        self.melody_music.insert(0, tempo.MetronomeMark(number=mytempo))
        #print(self.key)
        #print(int(length/basenotelength))
        pattern = self.generateSimpleMelodyPattern(length=int(length/basenotelength), basenotelength=basenotelength)
        print(pattern)

        #self.generateWalkMelody(mykey = self.key, mycompl=3, mytempo=3, myscale="Major", mygenre="pop", length=length/2, singlenotelength=basenotelength)

        self.generateMelody(mykey=self.key, mycompl=3, mytempo=3, myscale="Major", mygenre="pop", pattern=pattern, length=length/2, singlenotelength=basenotelength)


    def keypitchnames(self):
        x = []
        for pitch in self.key.pitches:
            x += [str(pitch.name)]
        return x

if __name__== "__main__":
    anote = note.Note()

    blubb = PunkMelody()
    bla = stream.Part()
    bla.append(chord.Chord("A4 C4 E4", duration=duration.Duration(4)))
    bla.append(chord.Chord("F4 A4 C4", duration=duration.Duration(4)))
    bla.append(chord.Chord("C4 E4 G4", duration=duration.Duration(4)))
    bla.append(chord.Chord("G4 B4 D4", duration=duration.Duration(4)))

    bla.append(chord.Chord("A4 C4 E4", duration=duration.Duration(4)))
    bla.append(chord.Chord("F4 A4 C4", duration=duration.Duration(4)))
    bla.append(chord.Chord("C4 E4 G4", duration=duration.Duration(4)))
    bla.append(chord.Chord("G4 B4 D4", duration=duration.Duration(4)))

    print(bla.quarterLength)
    #bla.show()
    blubb.chords_music = bla

    blubb.generate(mykey="C", mycompl=3, mytempo=120, myscale="Major", mygenre="pop",length=bla.quarterLength, basenotelength=0.5)
    #blubb.melody_music.show()

    mergedstream = stream.Stream()
    mergedstream.insert(0,blubb.chords_music)
    mergedstream.insert(0,blubb.melody_music)
    mergedstream.show()
    #print(blubb.generateSinmpleMelodyPattern(length=32))'''