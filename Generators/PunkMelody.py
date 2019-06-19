from music21 import *
import random as rn

class PunkMelody:

    def __init__(self):
        self.basenote = 0
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
        self.melodys = [
            "0, 2, 4, 2",
            "b,+2,+2,r,p,b,2,0"
        ]
        '''self.melodys = [
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

    def currentchord(self, position=None, offset=4):
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

    def currentnote(self,  offset, position=None):
        if self.melody_music is None:
            print("No Chords found in Punkmelody")
            return None
        if  self.melody_music.getElementsByClass("Note") is None:
            return "0"

        if position is None:
            position=self.melody_music.quarterLength

        for elem in self.melody_music.getElementsByClass("Note"):
            #print(str(elem) + str(elem.getOffsetBySite(self.melody_music)) + ", " + str(position))
            if(elem.getOffsetBySite(self.melody_music) + offset >= position):
                mycurrentnote = elem.__deepcopy__()
                for index, pitch in enumerate(self.key.pitches):
                    if pitch.name == mycurrentnote.name:
                        return index

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



    def generateSimpleMelodyPattern(self, length):
        if 1 > length:
           print("ERROR")
           exit(1)
        if length == 4:
            return "4"
        elif length > 8:
                results = ["2,2","2,2","2,2",
                           "4,4,4,4",
                           "4,4,2",
                           "4,2,4",
                           "2,4,4"]
        else:
                results = ["1",
                           "1",
                           "2,2",
                           "2,2"]

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
                   bla = bla + self.generateSimpleMelodyPattern(int(length / int(entry))) + ","
            return bla[:-1]



    def generateMelody(self, mykey, mycompl, mytempo, myscale, mygenre, length, pattern, singlenotelength=0.5):

        for patternentry in pattern.split(","):

            print(patternentry)
            currentbasenotelength = singlenotelength
            matchinglength = list(filter(lambda x: len(x.split(",")) == int(patternentry), self.melodys))
            usedmelodysmatchinglength = list(filter(lambda x: len(x.split(",")) == int(patternentry), self.usedmelodys))
            #print(matchinglength)
            print(self.usedmelodys)
            #print(usedmelodysmatchinglength)



            if len(matchinglength) == 0 and len(usedmelodysmatchinglength) == 0:
                print("Cant create melody of this length, exiting")
                exit(0)

            if (len(usedmelodysmatchinglength) != 0 and rn.randint(0,5) > 1):

                chosenmelody = rn.choice(usedmelodysmatchinglength)
                #if(len(chosenmelody.split(",")) > 2):
                print("Reusing Melodys " + str(chosenmelody))

            else:
                chosenmelody = rn.choice(matchinglength)
            print("The chosen melody is; " + str(chosenmelody))
            parsedchosenmelody = ""

            for melodyentry in chosenmelody.split(","):
                if "b" in melodyentry:
                    #print("Timing: {}, Current Chord: {} with length:{}".format(self.melody_music.quarterLength, self.currentchord(), self.currentchord().duration))
                    parsedmelodyentry = mykey.pitches.index(self.currentchord(offset=1).pitches[0])
                    mynote = note.Note(mykey.pitches[int(parsedmelodyentry)],
                                       duration=duration.Duration(singlenotelength))
                    self.melody_music.append(mynote)
                    parsedchosenmelody+=str(parsedmelodyentry)
                elif "p" in melodyentry:
                    mynote = note.Rest(duration=duration.Duration(singlenotelength))
                    self.melody_music.append(mynote)
                    parsedchosenmelody += "p"
                elif "r" in melodyentry:
                    parsedmelodyentry = rn.choice(range(7))
                    mynote = note.Note(mykey.pitches[parsedmelodyentry],
                                       duration=duration.Duration(singlenotelength))
                    self.melody_music.append(mynote)
                    parsedchosenmelody += str(parsedmelodyentry)
                elif "+" in melodyentry:
                    parsedmelodyentry = self.currentnote(offset=singlenotelength)
                    mynote = note.Note(self.key.pitches[(parsedmelodyentry + int(melodyentry[-1])) % 7],
                                       duration=duration.Duration(singlenotelength))
                    self.melody_music.append(mynote)
                    parsedchosenmelody += str((parsedmelodyentry + int(melodyentry[-1])) % 7)
                elif "-" in melodyentry:
                    parsedmelodyentry = self.currentnote(offset=singlenotelength)
                    mynote = note.Note(self.key.pitches[(parsedmelodyentry - int(melodyentry[-1])) % 7],
                                       duration=duration.Duration(singlenotelength))
                    self.melody_music.append(mynote)
                    parsedchosenmelody += str((parsedmelodyentry - int(melodyentry[-1])) % 7)
                else:
                    mynote = note.Note(self.key.pitches[int(melodyentry)],
                                       duration=duration.Duration(singlenotelength))
                    self.melody_music.append(mynote)
                    parsedchosenmelody += str(melodyentry)
                parsedchosenmelody += ","
            print(parsedchosenmelody)
            self.usedmelodys += [parsedchosenmelody[:-1]]


            '''elif "+" in melodyentry:
                    melodyentry = selself.currentchord().pitches[0]
                    mynote = note.Note(mykeyobj.pitches[(self.basenote + int(melodyentry[-1])) % 8],
                                       duration=duration.Duration(basenotelength))
                    self.basenote = self.basenote + int(melodyentry[-1])
                elif "-" in melodyentry:
                    mynote = note.Note(mykeyobj.pitches[(self.basenote + int(melodyentry[-1])) % 8],
                                       duration=duration.Duration(basenotelength))
                    self.basenote = self.basenote + int(melodyentry[-1])

                #self.melody_music.append(self.parsemelodyentry(melodyentry,currentbasenotelength, mykeyobj))
                '''

    def parsemelodyentry(self, melodyentry, basenotelength, mykeyobj):
        if "p" in melodyentry:
            mynote = note.Rest(duration=duration.Duration(basenotelength))
        elif "b" in melodyentry:
            mynote = note.Note(mykeyobj.pitches[self.basenote],
                               duration=duration.Duration(basenotelength))
        elif "r" in melodyentry:
            randompitch = rn.choice(range(8))
            mynote = note.Note(mykeyobj.pitches[randompitch],
                               duration=duration.Duration(basenotelength))
            self.basenote = randompitch
        elif "+" in melodyentry:
            mynote = note.Note(mykeyobj.pitches[(self.basenote + int(melodyentry[-1])) % 8],
                               duration=duration.Duration(basenotelength))
            self.basenote = self.basenote + int(melodyentry[-1])
        elif "-" in melodyentry:
            mynote = note.Note(mykeyobj.pitches[(self.basenote + int(melodyentry[-1])) % 8],
                               duration=duration.Duration(basenotelength))
            self.basenote = self.basenote + int(melodyentry[-1])
        else:
            mynote = note.Note(mykeyobj.pitches[(int(melodyentry)) % 8],
                               duration=duration.Duration(basenotelength))
            self.basenote = int(melodyentry)

        if isinstance(mynote, note.NotRest):
           self.noteusage[str(mynote.pitch)[0]] += 1

        return mynote


    def generate(self, mykey, mycompl, mytempo, myscale, mygenre, length, basenotelength=0.25 ):
        self.melody_music = stream.Part()
        self.key = key.Key(str(mykey))
        print(self.key)
        #print(int(length/basenotelength))
        pattern = self.generateSimpleMelodyPattern(length=int(length/basenotelength))
        print(pattern)
        self.generateMelody(mykey = self.key, mycompl=3, mytempo=3, myscale="Major", mygenre="pop", pattern=pattern, length=length, singlenotelength=basenotelength)


if __name__== "__main__":
    anote = note.Note()

    blubb = PunkMelody()
    bla = stream.Part()
    bla.append(chord.Chord("C4 E4 G4", duration=duration.Duration(4)))
    bla.append(chord.Chord("D4 F4 A4", duration=duration.Duration(4)))
    bla.append(chord.Chord("E4 G4 B4", duration=duration.Duration(4)))
    bla.append(chord.Chord("B4 D4 C4", duration=duration.Duration(4)))
    print(bla.quarterLength)
    #bla.show()
    blubb.chords_music = bla

    blubb.generate(mykey="C", mycompl=3, mytempo=3, myscale="Major", mygenre="pop",length=bla.quarterLength, basenotelength=0.5)
    #blubb.melody_music.show()

    mergedstream = stream.Stream()
    mergedstream.insert(0,blubb.chords_music)
    mergedstream.insert(0,blubb.melody_music)
    mergedstream.show()
    #print(blubb.generateSinmpleMelodyPattern(length=32))'''