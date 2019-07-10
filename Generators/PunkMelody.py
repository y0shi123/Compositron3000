from music21 import *
import random as rn
import music21
class PunkMelody:

    def generateMelodyPartsList(self,
        #noteints = ["0","1","2","4","5","6","r", "p", "p", "b", "b", "b"],
        noteints=["1", "2", "4", "5", "6", "r", "p", "p", "b", "b", "b"],
        timeoptions = ["h","d", " ", " "],
        stepoptions = ["+", "-", " ", " "],
        steplengths = [0,0,1,1,2,3,4], firstnotesettochord=False, addpauses=False):

        '''noteints = ["1","2","4","5","6","r", "p", "p", "b", "b", "b"]
        timeoptions = ["h","d", " ", " "]
        stepoptions = ["+", "-", " ", " "]
        steplengths = [0,0,1,1,2,3,4]'''

        melodys = []
        for length in [1,2,4,8,16]*3:
            melodys += [self.generateMelodyPartListEntry(length=length, noteints=noteints, stepoptions=stepoptions,
                                                         timeoptions = timeoptions, steplengths=steplengths, firstnotesettochord=firstnotesettochord)]

        if addpauses:
            for _ in range(3):
                melodys+= ["p", "p,p", "p,p,p,p", "p,p,p,p,p,p,p,p", "p,p,p,p,p,p,p,p,p,p,p,p,p,p,p,p"]

        for entry in melodys:
            if entry == "d":
                print("Found something odd")
        return melodys

    def generateMelodyPartListEntry(self, length, noteints, stepoptions, timeoptions, steplengths, firstnotesettochord=False):

        melody = ""
        firstnote=True
        while(len(melody.split(",")) < length+1):
            noteint    = rn.choice(noteints)
            stepoption = rn.choice(stepoptions)
            timeoption = rn.choice(timeoptions)
            steplength = rn.choice(steplengths)
            #print("noteint: {}, stepoption: {}, timeoption: {}, steplength: {}".format(noteint,stepoption,timeoption,steplength))
            if firstnotesettochord and firstnote:
                melody += "b" + ","
                firstnote=False
            elif ("+" in stepoption or "-" in stepoption) and ("h" in timeoption or "d" in timeoption):
                '''if(rn.randint(0,1) == 0):
                    melody +=  str(noteint) + str(timeoption) + ","
                else:
                    melody += str(stepoption) + str(steplength) + ","'''
                melody += str(stepoption) + str (steplength) + str(timeoption) + ","
            elif "+" in stepoption or "-" in stepoption:
                melody += str(stepoption) + str(steplength) + ","
            elif "h" in timeoption or "d" in timeoption:
                melody += str(noteint) + str(timeoption) + ","
            else:
                melody += str(noteint) + ","
        melody = melody[:-1]
        #print(melody)
        return melody

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
        self.melodys = ["bd, ,+2d, ,+rh,-rh,+r,b"]


        '''                "bh, rh, +r, -r",
            "bd,  , rd, , +2, +4, -2d, ",
            "b, r,+2,+4,b,+4,-2,0",
            "bd, ,+2d, ,+4d, ,rd, "]
        '''

    def currentchord(self, offset = 4, position=None):
        if self.chords_music is None or self.chords_music.getElementsByClass("Chord") is None:
            print("No Chords found in Punkmelody")
            return None

        currentchord = None
        if position is None:
            position=self.melody_music.quarterLength

        for elem in self.chords_music.getElementsByClass("Chord"):
            if(elem.getOffsetBySite(self.chords_music)+elem.duration.quarterLength > position):
                currentchord = elem.__deepcopy__()
                return currentchord
        print("No Chord found")
        return chord.Chord("C C# D#")

    def currentchordfixed(self, offset = 4, position=None):
        if self.chords_music is None or self.chords_music.getElementsByClass("Chord") is None:
            print("No Chords found in Punkmelody")
            return None

        if position is None:
            position=self.melody_music.quarterLength

        previous = None
        #print("##############################")
        #self.chords_music.show('text')
        #print("##############################")
        for elem in self.chords_music.getElementsByClass("Chord"):
            if(elem.getOffsetBySite(self.chords_music) < position):
                previous = elem
            else:
                return previous

        print("returning last chord found")
        return previous

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

        #print("Found no notes at position: {}".format(position))
        #print("returning 0")
        return 0

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
                return elem
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

    def generateSimpleMelodyPattern(self, length, basenotelength, anchor=1):
        if 1 > length:
           print("ERROR")
           exit(1)
        if length == anchor:
            #print("Returning anchor")
            return str(int(anchor))
        #elif length*basenotelength > 4:
        elif length > anchor*2:
            #print(str(length) + " Upp")
            results = ["2,2","2,2",
                           "4,4,4,4",
                           "4,4,2",
                           "4,2,4",
                           "2,4,4"]
        else:
            #print(str(length) + " Down")
            results = ["1",
                           "1",
                           "1",
                           "2,2",
                           "2,2"]
        res = rn.choice(results)
        #print("Splitting {} into parts with: {}".format(length,res))
        if res == "1":
            return str(length)
        else:
            bla = ""
            for entry in res.split(","):
                if (rn.randint(0, 6) <= 1 and length <= 8) :
                   #print("Finished here")
                   bla = bla + str(int(length / int(entry))) + ","
                else:
                   #print("Recursive Call")
                   bla = bla + self.generateSimpleMelodyPattern(int(length / int(entry)), basenotelength=basenotelength,anchor=anchor) + ","
            #print(bla[:-1])
            return bla[:-1]

    def generateMelodyFromParts(self, mykey, mycompl, mytempo, myscale, mygenre, length, pattern, singlenotelength=0.5):

        for patternentry in pattern.split(","):

            # TODO: Entrys sollten sich merken an welcher Stelle sie verwendet wurden und besonders in vielfachen dieser Stelle wiederholt werden

            #print(patternentry)
            currentbasenotelength = singlenotelength
            matchinglength = list(filter(lambda x: len(x.split(",")) == int(patternentry), self.melodys))
            usedmelodysmatchinglength = list(filter(lambda x: len(x.split(",")) == int(patternentry), self.usedmelodys))
            #print(matchinglength)
            #print(self.usedmelodys)
            #print(usedmelodysmatchinglength)
            reusedcounter = 0



            if len(matchinglength) == 0 and len(usedmelodysmatchinglength) == 0:
                print("Cant create melody of this length, exiting")
                exit(0)

            if (len(usedmelodysmatchinglength) != 0 and rn.randint(0,8) < 2*len(usedmelodysmatchinglength) + 5-mycompl - reusedcounter):
                reusedcounter += 1
                chosenmelody = rn.choice(usedmelodysmatchinglength)
                print("Reusing Melodys " + str(chosenmelody))

            else:
                reusedcounter -= 1
                print("Did not reuse Melody")
                chosenmelody = rn.choice(matchinglength)
            if (not self.useparsedmelodys):
                self.usedmelodys += [chosenmelody]

            #print("The chosen melody is         : " + str(chosenmelody))
            parsedchosenmelody = ""
            skipnext = False
            for index, melodyentry in enumerate(chosenmelody.split(",")):
                #print("current melodyentry: " + str(melodyentry))
                multiply = 1
                if skipnext:
                    #print("skipped")
                    skipnext=False
                    parsedchosenmelody += " ,"
                    continue
                if "d" in melodyentry:
                    #if self.melody_music.quarterLength + 2*singlenotelength <= self.chords_music.quarterLength :

                    #print("testing doubling function at position {}: comparing these values: {}, {}".format(
                    #    self.melody_music.quarterLength,
                    #    int((self.melody_music.quarterLength + 2*singlenotelength-0.0001)/4), int(self.melody_music.quarterLength/4)))
                    if int((self.melody_music.quarterLength + 2*singlenotelength-0.001)/4) == int((self.melody_music.quarterLength)/4):
                        #print("took the if branch")
                        multiply = 2
                        melodyentry=melodyentry[:-1]
                        skipnext = True
                    else:
                        #print("took the else branch")
                        melodyentry = melodyentry[:-1]

                if "h" in melodyentry or self.melody_music.quarterLength + 0.5*singlenotelength == self.chords_music.quarterLength:
                    multiply = 0.5
                    melodyentry=melodyentry[:-1]

                if "b" in melodyentry:
                    #print("Timing: {}, Current Chord: {} with length:{}".format(self.melody_music.quarterLength, self.currentchord(), self.currentchord().duration))
                    parsedmelodyentry = self.keypitchnames().index(self.currentchord(offset=1).pitches[0].name)
                    mynote = note.Note(mykey.pitches[int(parsedmelodyentry)],
                                       duration=duration.Duration(singlenotelength))
                    parsedchosenmelody+="b"
                elif "p" in melodyentry:
                    mynote = note.Rest(duration=duration.Duration(singlenotelength))
                    parsedchosenmelody += "p"
                elif "r" in melodyentry and not ("+" in melodyentry or "-" in melodyentry):
                    parsedmelodyentry = rn.choice(range(7))
                    mynote = note.Note(mykey.pitches[parsedmelodyentry],
                                       duration=duration.Duration(singlenotelength))
                    parsedchosenmelody += str(parsedmelodyentry)
                elif "+" in melodyentry:
                    if "r" in melodyentry:
                        parsedmelodyentry = self.currentNoteIndex()
                        randint = rn.randint(0,6)
                        mynote = note.Note(self.key.pitches[(parsedmelodyentry + randint) % 7],
                                           duration=duration.Duration(singlenotelength))
                        #if (parsedmelodyentry + randint > 6):
                        #    mynote.octave = mynote.octave + 1
                        parsedchosenmelody += "+" + str(randint)
                    else:
                        parsedmelodyentry = self.currentNoteIndex()
                        #print("Currentlz in + path" + str(melodyentry))
                        #print("Trying to add pitch: {} of key".format((parsedmelodyentry + int(melodyentry[1])%7)))
                        mynote = note.Note(self.key.pitches[(parsedmelodyentry + int(melodyentry[1])) % 7],
                                           duration=duration.Duration(singlenotelength))
                        #if(parsedmelodyentry + int(melodyentry[-1]) > 6):
                        #    mynote.octave = mynote.octave+1
                        parsedchosenmelody += "+" + melodyentry[-1]
                    #parsedchosenmelody += str((parsedmelodyentry + int(melodyentry[-1])) % 7)
                elif "-" in melodyentry:
                    if "r" in melodyentry:
                        parsedmelodyentry = self.currentNoteIndex()
                        randint = rn.randint(0,6)

                        mynote = note.Note(self.key.pitches[int(parsedmelodyentry - randint) % 7],
                                           duration=duration.Duration(singlenotelength))
                        #if (parsedmelodyentry - randint < 0):
                        #    mynote.octave = mynote.octave - 1
                        parsedchosenmelody += "-" + str(randint)
                    else:
                        parsedmelodyentry = self.currentNoteIndex()
                        #print("Trying to add pitch: {} of key".format((parsedmelodyentry + int(melodyentry[1]) % 7)))
                        mynote = note.Note(self.key.pitches[(parsedmelodyentry - int(melodyentry[1])) % 7],
                                          duration=duration.Duration(singlenotelength))
                        #if (parsedmelodyentry - int(melodyentry[-1]) < 0):
                        #    mynote.octave = mynote.octave - 1
                        parsedchosenmelody += "-" + melodyentry[-1]
                        #parsedchosenmelody += str((parsedmelodyentry - int(melodyentry[-1])) % 7)
                else:
                    mynote = note.Note(self.key.pitches[int(melodyentry)],
                                       duration=duration.Duration(singlenotelength))
                    parsedchosenmelody += str(melodyentry)

                '''            if self.melody_music.quarterLength + singlenotelength*2 <= self.chords_music.quarterLength and rn.randint(0,3) == 3:
                #pass
                currentNote.duration.quarterLength*=2
            elif(self.melody_music.quarterLength + singlenotelength/2 == self.chords_music.quarterLength):
                currentNote.duration.quarterLength/=2
                '''


                if multiply == 2:
                    parsedchosenmelody += "d"
                if multiply == 0.5:
                    parsedchosenmelody += "h"
                    copy = mynote.__deepcopy__()
                    copy.duration.quarterLength /= 2
                    if self.melody_music.quarterLength + 0.5*singlenotelength < self.chords_music.quarterLength:
                        self.melody_music.append(copy)
                mynote.duration.quarterLength *= multiply
                self.melody_music.append(mynote)
                parsedchosenmelody += ","
                #print(parsedchosenmelody)
            #print("the complete parsed melody is:" + str(parsedchosenmelody))
            if self.useparsedmelodys:
                self.usedmelodys += [parsedchosenmelody[:-1]]
            #print("#################################################")
        return self.melody_music

    def generateOctaveMelodyFromParts(self, mykey, mycompl, mytempo, myscale, mygenre, length, pattern, singlenotelength=0.5):

        #print("generating octave melodys")
        stepoptions = ["+", "+", "+", "-"]
        if(rn.randint(0,1)==0):
            stepoptions+=[" "]
        self.melodys = self.generateMelodyPartsList(noteints = ["p"],
        timeoptions = ["d"," "," "," "," "],
        stepoptions = stepoptions,
        steplengths = [0,0,0,0,0,0,0,0,0,1,1,1,1,2,2])
        self.generateMelodyFromParts(mykey, mycompl, mytempo, myscale, mygenre, length, pattern, singlenotelength)
        #self.melody_music.show()
        replacewithoctaves = stream.Part()

        treble = clef.TrebleClef()
        replacewithoctaves.insert(0, self.key.__deepcopy__())
        replacewithoctaves.insert(0, treble)
        replacewithoctaves.insert(0, tempo.MetronomeMark(number=mytempo))
        for mynote in self.melody_music.getElementsByClass("Note"):
            copynote = mynote.__deepcopy__()
            copynote.pitch.octave+=1
            self.melody_music.insert(mynote.getOffsetBySite(self.melody_music), copynote)

            octavechord = chord.Chord([mynote.pitch.nameWithOctave, copynote.pitch.nameWithOctave])
            octavechord.quarterLength = copynote.duration.quarterLength
            replacewithoctaves.insert(mynote.getOffsetBySite(self.melody_music), octavechord)

        for myrest in self.melody_music.getElementsByClass("Rest"):
            print("Pause gefunden")
            replacewithoctaves.insert(myrest.getOffsetBySite(self.melody_music), myrest.__deepcopy__())

        #self.melody_music.show()
        #replacewithoctaves.show()

        self.melody_music = replacewithoctaves

    def generateWalkMelody(self, mykey, mycompl, mytempo, myscale, mygenre, length, singlenotelength):
        notesToUse = [1,2,4,5,6]
        currentNoteValue = rn.choice(notesToUse)
        #steps = [0]
        steps = [0,0,1,1,1,1,2,3,4]
        direction = 1

        while (self.melody_music.quarterLength < length):
            #if(rn.randint(0,5) == 5 and self.melody_music.quarterLength + singlenotelength < self.chords_music.quarterLength ):
            #    self.melody_music.append(note.Rest(duration=duration.Duration(singlenotelength)))

            step = 0
            if(rn.randint(0,2) == 2):
                step = rn.choice(steps)
            currentNoteValue = ((currentNoteValue + direction * step) % 7)
            currentNote =(note.Note(mykey.pitches[currentNoteValue].name, duration=duration.Duration(singlenotelength)))
            if (rn.randint(0,10) < 4):
                direction*= -1
            if self.melody_music.quarterLength + singlenotelength*2 <= self.chords_music.quarterLength and rn.randint(0,3) == 3:
                #pass
                currentNote.duration.quarterLength*=2
            elif(self.melody_music.quarterLength + singlenotelength/2 == self.chords_music.quarterLength):
                currentNote.duration.quarterLength/=2
            #print("currentnote will be: {} with length: {}".format(currentNoteValue, currentNote.duration.quarterLength))
            self.melody_music.append(currentNote)
        #self.connectChords(singlenotelength, length)
        return self.melody_music

    def connectChords(self, singlenoteLength, length):
        #print("Connecting Chords..")
        #allpitches = ["A", "A-", "B", "B-", "C", "D", "D-", "E", "E-", "F", "G", "G-"]
        allpitches = ["A-", "A", "B-", "B", "C", "D-", "D", "E-", "E", "F", "G-", "G"]
        keychords = []
        fullchords = []
        fullchordsstream = stream.Stream()

        # Trying to fix the method below which sometimes wont work
        #keychords += [self.currentchordfixed(position=0.0001)]

        for x in range(4, int(length), 4):
            keychords += [self.currentchordfixed(position=x)]
        keychords += [self.currentchordfixed(position=int(length)-0.01)]
        print(keychords)
        #print(keychords)

        for singlechord in keychords:
            basenoteIndex = self.keypitchnames().index(singlechord.pitches[0].name)
            notelist = [self.key.pitches[basenoteIndex], self.key.pitches[(basenoteIndex + 2) % 7],
                        self.key.pitches[(basenoteIndex + 4) % 7], self.key.pitches[(basenoteIndex+7)%7]]
            notelist = list(filter(lambda x: x != self.key.pitches[0], notelist))
            if(len(notelist)==2):
                notelist += [self.key.pitches[0]]
            fullchord = music21.chord.Chord(notelist, duration=duration.Duration(4))
            fullchordsstream.append(fullchord)
            fullchords += [fullchord]
        #print(fullchords)
        keychords = []

        ###################################

        '''for singlechord in self.chords_music.getElementsByClass("Chord"):
            if(singlechord.getOffsetBySite(self.chords_music)% 4 == 0 and not singlechord.getOffsetBySite(self.chords_music) >= self.melody_music.quarterLength):
                basenoteIndex = self.keypitchnames().index(singlechord.pitches[0].name)
                notelist = [self.key.pitches[basenoteIndex], self.key.pitches[(basenoteIndex+2)%7], self.key.pitches[(basenoteIndex+4)%7], self.key.pitches[(basenoteIndex+6)%7], ]
                fullchord = music21.chord.Chord(notelist, duration=duration.Duration(4))
                fullchordsstream.append(fullchord)
                keychords += [fullchord]

        print(keychords)
        '''
        for index, chord in enumerate(fullchords):

            if index==0:
                continue
            foundsomething = False
            predecessor = fullchords[index-1]

            for currentpitch in chord.pitches:
                for oldpitch in predecessor.pitches:
                    if allpitches.index(currentpitch.name) == (allpitches.index(oldpitch.name)-1)%12:
                        #print(str(chord) + " und " + str(predecessor) + " sind verbunden durch :" + str(currentpitch) + " und " + str(oldpitch))
                        foundsomething = True
                        currentNote = self.currentNoteObject(position = chord.getOffsetBySite(fullchordsstream))
                        oldNote     = self.currentNoteObject(position =chord.getOffsetBySite(fullchordsstream)-0.001 )
                        if (currentNote is not oldNote):
                            currentNote.pitch = currentpitch
                            oldNote.pitch = oldpitch
                    if foundsomething:
                        break
                    if allpitches.index(currentpitch.name) == (allpitches.index(oldpitch.name)+1)%12:
                        #print(str(chord) + " und " + str(predecessor) + " sind verbunden durch :" + str(currentpitch) + " und " + str(oldpitch))
                        foundsomething = True
                        currentNote = self.currentNoteObject(position = chord.getOffsetBySite(fullchordsstream))
                        oldNote     = self.currentNoteObject(position =chord.getOffsetBySite(fullchordsstream)-0.001 )
                        if (currentNote is not oldNote):
                            currentNote.pitch = currentpitch
                            oldNote.pitch = oldpitch

                    if foundsomething:
                       break

                if foundsomething:
                    break
            if not foundsomething:
                print("Nothing was found")

    def generate(self, mykey, mycompl, mytempo, myscale, mygenre, length, basenotelength):
        self.melody_music = stream.Part()
        self.key = key.Key(mykey, myscale)
        print(self.key.pitches)
        treble = clef.TrebleClef()
        self.melody_music.insert(0, self.key.__deepcopy__())
        self.melody_music.insert(0, treble)
        self.melody_music.insert(0, tempo.MetronomeMark(number=mytempo))

        pattern = self.generateSimpleMelodyPattern(length=int((length)/basenotelength), basenotelength=basenotelength, anchor=4/basenotelength)
        print("melodypattern: " + str(pattern))

        if mygenre == "Blink" or mygenre == "PopPunk" or mygenre == "Acoustic":
            self.melodys = self.generateMelodyPartsList(firstnotesettochord=True)
            self.generateMelodyFromParts(mykey=self.key, mycompl=mycompl, mytempo=mytempo, myscale=myscale, mygenre=mygenre,
                                           pattern=pattern, length=length, singlenotelength=basenotelength)
        elif mygenre == "Rise" or mygenre == "Punk":
            print("Generating Octaves")
            self.generateOctaveMelodyFromParts(mykey=self.key, mycompl=mycompl, mytempo=mytempo, myscale=myscale, mygenre=mygenre,
                                           pattern=pattern, length=length, singlenotelength=basenotelength)
        elif mygenre == "Solo":
            self.generateWalkMelody(mykey = self.key, mycompl=mycompl, mytempo=mytempo, myscale=myscale, mygenre=mygenre, length=length, singlenotelength=basenotelength)
            self.connectChords(singlenoteLength=basenotelength, length=length)
        else:
            print("Else Path")
            self.generateMelodyFromParts(mykey=self.key, mycompl=3, mytempo=mytempo, myscale="Major", mygenre="pop",
                                         pattern=pattern, length=length, singlenotelength=basenotelength)

        return self.melody_music

    def keypitchnames(self):
        x = []
        for pitch in self.key.pitches:
            x += [str(pitch.name)]
        return x

if __name__== "__main__":


    blubb = PunkMelody()

    '''for _ in range(10):
        ql = rn.choice([0.5, 1, 0.25])
        print("QuarterLänge: "+str(ql))
        print(blubb.generateSimpleMelodyPattern(int(16/ql), ql, anchor=4))
        print("#############################")'''
    #length=int((length)/basenotelength)
    #blubb.melodys = blubb.generateMelodyPartsList()
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

    blubb.generate(mykey="C", mycompl=3, mytempo=120, myscale="Major", mygenre="Solo",length=bla.quarterLength, basenotelength=1)
    #blubb.melody_music.show()

    mergedstream = stream.Stream()
    mergedstream.insert(0,blubb.chords_music)
    mergedstream.insert(0,blubb.melody_music)
    mergedstream.show()
    #print(blubb.generateSinmpleMelodyPattern(length=32))