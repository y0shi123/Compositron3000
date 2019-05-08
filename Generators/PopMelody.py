from music21 import *
import random as rn

class PopMelody:

    def __init__(self):
        self.melody_music = stream.Part()
        self.melodys = [
             "+0, +2, +4, +6",
             "0, 2, 4, 6",
             "+2, +4, +2, +6",
             "2, 4, 5, 2",
             "2, p, 5, p",
             "+2, +4",
             "p, p, p, p",
             "p, p, p, p",
             "p, p, p, p",
             "p, p",
             "p, p"
             "p, p, p, p, p, p, p, p",
             "0,0",
             "0, r, 0, r",
             "r, r",
             "0 ,r, r, 0, 2, 4, r",
             "0, p, 0, p",
             "0",
             "p",
             "+0, +2, +4, +2, +5, +4, +2, +4",
             "r,r,r,r,r,r,r,r",
             "r,p,r,p,0,2,4,p",
             "+0, +2, +4, +2, +5, +4, +2, +4, +0, +2, +4, +2, +5, +4, +2, +4",
             "+0, +2, +4, +2, +5, +4, +2, +4, +0, +2, +4, +2, +5, +4, +2, +4,+0, +2, +4, +2, +5, +4, +2, +4, +0, +2, +4, +2, +5, +4, +2, +4",
        ]

    def generateMelodyPattern(self, length):
        if 1 > length:
           print("ERROR")
           exit(1)
        if length == 1:
            return "1"
        elif length == 2:
                results = ["1",
                           "2,2"
                           ]
        elif length > 8:
                results = ["2,2",
                           "4,4,4,4",
                           "4,4,2",
                           "4,2,4",
                           "2,4,4"]
        else:
                results = ["1", "1",
                           "2,2", "2,2",
                           "4,4,2",
                           "4,2,4",
                           "2,4,4"]

        res = rn.choice(results)
        # print(res)
        if res == "1" :
            return str(length)
        else:
            bla = ""
            for entry in res.split(","):
                if (rn.randint(0, 6) <= 4 and length <= 8) :
                   bla = bla + str(int(length / int(entry))) + ","
                else:
                   bla = bla + self.generateMelodyPattern(int(length / int(entry))) + ","
            return bla[:-1]

    def parsemelodyentry(self, melodyentry, basenote, basenotelength, mykeyobj):
        if "p" in melodyentry:
            mynote = note.Rest(duration=duration.Duration(basenotelength))
        elif "b" in melodyentry:
            mynote = note.Note(mykeyobj.pitches[basenote],
                               duration=duration.Duration(basenotelength))
        elif "r" in melodyentry:
            randompitch = rn.choice(range(8))
            mynote = note.Note(mykeyobj.pitches[randompitch],
                               duration=duration.Duration(basenotelength))
            basenote = randompitch
        elif "+" in melodyentry:
            mynote = note.Note(mykeyobj.pitches[(basenote + int(melodyentry[-1])) % 8],
                               duration=duration.Duration(basenotelength))
            basenote = basenote + int(melodyentry[-1])
        elif "-" in melodyentry:
            mynote = note.Note(mykeyobj.pitches[(basenote + int(melodyentry[-1])) % 8],
                               duration=duration.Duration(basenotelength))
            basenote = basenote + int(melodyentry[-1])
        else:
            mynote = note.Note(mykeyobj.pitches[(basenote + int(melodyentry[-1])) % 8],
                               duration=duration.Duration(basenotelength))
        return mynote

    def generateMelody(self, mykey, mycompl, mytempo, myscale, mygenre, length, pattern, basenotelength=0.5):

        mykeyobj = key.Key(mykey, myscale)
        basenote = 0

        for patternentry in pattern.split(","):
            currentbasenotelength = basenotelength

            tempoadjust = rn.choice(range(6))
            if tempoadjust == 0 and (int(patternentry) / 2) == (int(int(patternentry) / 2)):
                print("Old Tempo: " + str(patternentry))
                patternentry = int(int(patternentry) / 2)
                print("Tempo Adjusted: " + str(patternentry))
                currentbasenotelength = basenotelength * 2
            if tempoadjust == 1:
                print("Old Tempo: " + str(patternentry))
                patternentry = int(patternentry) * 2
                print("Tempo Adjusted: " + str(patternentry))
                currentbasenotelength = basenotelength / 2

            matchinglength = list(filter(lambda x: len(x.split(",")) == int(patternentry), self.melodys))

            if len(matchinglength) == 0:
                print("Cant create melody of this length, exiting")
                exit(0)

            chosenmelody = rn.choice(matchinglength)

            for melodyentry in chosenmelody.split(","):
                self.melody_music.append(self.parsemelodyentry(melodyentry,basenote,currentbasenotelength, mykeyobj))

        #self.melody_music.show()
        return self.melody_music

    def generate(self, mykey, mycompl, mytempo, myscale, mygenre, length, singlechordlength=0.25 ):
        self.totallength = length
        result = self.generateMelodyPattern(length=length)
        sum = 0
        for entry in result.split(","):
            sum += int(entry)
        if sum != length:
            print("Falsche länge :(")
        print(result)
        self.generateMelody(mykey, mycompl, mytempo, myscale, mygenre, length,result)


if __name__== "__main__":
    blubb = PopMelody()
    blubb.generate("C", 3, 4, "Major", "Pop", 32)