from music21 import *
import random as rn

class PopMelody:

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
        self.usedmelodys = []
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
        ]
        '''
        self.melodys = [
            "b, 1, 2, 4",
            "b, 1, b, 3",
            "b, 1, 2, 4, b, 1, b, 3",
            "b, 1, 3, 6",
            "b, 7, 4, 2",
            "b, 6, b, 4",
            "0, 0, 0, 0",
            "p",
            "0",
            "4, 4",
            "7, 4"
        ]'''

    def generateMelodyPattern(self, length):
        if 1 > length:
           print("ERROR")
           exit(1)
        if length == 1:
            return "1"
        elif length == 2:
                results = ["1",
                           "2,2",
                           ]
        elif length > 8:
                results = ["2,2","2,2","2,2",
                           "4,4,4,4",
                           "4,4,2",
                           "4,2,4",
                           "2,4,4"]
        else:
                results = ["1", "1", "1",
                           "2,2", "2,2",
                           "4,4,2",
                           "4,2,4",
                           "2,4,4"]

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
                   bla = bla + self.generateMelodyPattern(int(length / int(entry))) + ","
            return bla[:-1]

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

    def generateMelody(self, mykey, mycompl, mytempo, myscale, mygenre, length, pattern, basenotelength=0.5):

        mykeyobj = key.Key(mykey, myscale)
        for patternentry in pattern.split(","):

            currentbasenotelength = basenotelength
            matchinglength = list(filter(lambda x: len(x.split(",")) == int(patternentry), self.melodys))
            usedmelodysmatchinglength = list(filter(lambda x: len(x.split(",")) == int(patternentry), self.usedmelodys))


            if len(matchinglength) == 0 and len(usedmelodysmatchinglength) == 0:
                print("Cant create melody of this length, exiting")
                exit(0)

            if (len(usedmelodysmatchinglength) != 0 and rn.randint(0,5) > 1):
                chosenmelody = rn.choice(usedmelodysmatchinglength)
                #if(len(chosenmelody.split(",")) > 2):
                #   print("Reusing Melodys " + str(chosenmelody))
                if "r" in str(chosenmelody):
                    chosenmelody = rn.choice(matchinglength)
            else:
                '''tempoadjust = rn.choice(range(6))
                if tempoadjust == 0 and (int(patternentry) / 2) == (int(int(patternentry) / 2)):
                    patternentry = int(int(patternentry) / 2)
                    currentbasenotelength = basenotelength * 2
                if tempoadjust == 1:
                    patternentry = int(patternentry) * 2
                    currentbasenotelength = basenotelength / 2'''
                chosenmelody = rn.choice(matchinglength)

            self.usedmelodys += [chosenmelody]

            for melodyentry in chosenmelody.split(","):
                self.melody_music.append(self.parsemelodyentry(melodyentry,currentbasenotelength, mykeyobj))


    def generate(self, mykey, mycompl, mytempo, myscale, mygenre, length, basenotelength=0.5 ):
        self.melody_music = stream.Part()
        result = self.generateMelodyPattern(length=length/basenotelength)
        print(result)
        sum = 0
        for entry in result.split(","):
            sum += int(entry)
        if sum != length/basenotelength:
            print("Falsche länge :(")
        #print(result)
        self.melody_music.append(tempo.MetronomeMark(number=mytempo))
        self.generateMelody(mykey, mycompl, mytempo, myscale, mygenre, length,result, basenotelength=basenotelength)
        return self.melody_music.__deepcopy__()

if __name__== "__main__":
    blubb = PopMelody()
    blubb.generate("C", 3, 40, "Major", "Pop", 128, basenotelength=0.25)
    #print(blubb.noteusage)
    '''for index, entry in enumerate(blubb.usedmelodys):
        print(entry, end=' // ')
        if(index  > 0 and index % 4 == 0):
            print('')
    '''
    blubb.melody_music.show()