from music21 import *
import random as rn

class PopMelody:

    def __init__(self):
        self.chords_music = stream.Part()
        self.chords_music.quarterLength=16

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
        elif length > self.totallength / 2:
                results = ["1",
                           "2,2",
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
        if res == "1":
            return str(length)
        else:
            bla = ""
            for entry in res.split(","):
                if rn.randint(0, 5) > 2:
                   bla = bla + self.generateMelodyPattern(int(length / int(entry))) + ","
                else:
                   bla = bla + str(int(length / int(entry))) + ","
            return bla[:-1]

    def generateMelody(self, mykey, mycompl, mytempo, myscale, mygenre, length, pattern, singlechordlength=0.25):
        x = [["+2, +4, +6"],
                     ["2, 4, 6"],
                     ["2, 4, 2, 6"],
                     ["2, 4, 5, 2"]
                    ]
        mykeyobj = key.Key(mykey, myscale)
        print(pattern)
        return self.chords_music

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
        '''x = [["+2, +4, +6", 3],
             ["2, 4, 6", 3],
             ["2, 4, 2, 6", 4],
             ["2, 4, 5, 2", 4]
            ]
        mykeyobj = key.Key(mykey, myscale)

        return self.chords_music'''


if __name__== "__main__":
    blubb = PopMelody()
    blubb.generate("C", 3, 4, "Major", "Pop", 16)