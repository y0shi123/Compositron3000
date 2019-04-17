import random as rn
import sys

from music21 import *




environment.set("musicxmlPath", r"C:\Program Files\MuseScore 3\bin\MuseScore3.exe")
#environment.set('midiPath', env.env["midiPath"])
#environment.set('musicxmlPath', env.env["musicxmlPath"])


def main():
    description = {
        "key": ('c', 'major'),
        # "key": None,
        "speed": None,
        "melody": None,
        "chords": None,
        "adj": ['simple', 'sad'],  # ["sad", "happy"]

    }

    mykey = getKey(description)

    song = stream.Stream()


    chorus = stream.Stream()
    chorus.quarterLength = 16

    verse = stream.Stream()
    verse.quarterLength = 16

    bridge = stream.Stream()
    bridge.quarterLength = 24

    allparts = [verse, bridge, chorus]



    for part in allparts:

        chordlength = 2
        singlechordlength = 2

        if(part == verse):
            singlechordlength = 1


        if(part == bridge):
            mykey = mykey.relative

        partChords = stream.Part()
        partChords.quarterLength = part.quarterLength

        getChords(description, mykey, partChords, singlechordlength, chordlength)

        partMelody = stream.Part()
        partMelody.quarterLength = part.quarterLength

        #if(part != verse):
        writeMelody(description, mykey, partMelody)
        #else:
        #partMelody.insert(note.Rest(duration=duration.Duration(part.quarterLength)))

        #partChords.show()
        #partMelody.show()

        part.insert(0, partChords)
        part.insert(0, partMelody)


        if(part == bridge):
            mykey = mykey.relative

    structure = [chorus, verse, chorus, verse, chorus, bridge, chorus, chorus]
    #structure = [chorus, bridge]

    #chorus.show()
    #verse.show()
    #bridge.show()

    # for part in chorus.getElementsByClass(stream.Part):
    #     song.append(part)

    #song.show()

    chordacc = stream.Part()
    melodyacc= stream.Part()
    count = 0
    for songpart in structure:
        for singlemeasure in songpart.getElementsByClass(stream.Part).stream():
           if(count%2 == 0):
               chordacc.append(singlemeasure.__deepcopy__())
           else:
               melodyacc.append(singlemeasure.__deepcopy__())
           count = count + 1
    song.append(chordacc)
    song.append(melodyacc)
    song.show()

    #song.append(allchords)
    #song.append(allmelodies)
    # song.show()


def getChords(desc, mykey, partChords, singlechordlength, chordlength):
    chordbasenotes = writeChords(desc)
    partlength = partChords.quarterLength
    timeused = 0
    index = 0
    #print(partChords.quarterLength)
    while(timeused < partlength):
        currentchord = getChord(mykey, chordbasenotes[index], duration = duration.Duration(singlechordlength))
        for _ in range(int(chordlength/singlechordlength)):
                partChords.append(currentchord.__deepcopy__())
        timeused = timeused + chordlength
        index    = (index + 1) % len(chordbasenotes)
    #partChords.show()


'''def getMelody(desc, mykey, partMelody):
    mymelody = stream.Part()
    count = 0
    for part in allchords.getElementsByClass(stream.Stream):
        melody = stream.Stream()
        melody.duration = part.duration
        writeMelody(desc, melody, mykey)
        melody.append(note.Rest(duration=duration.Duration(4)))
        mymelody.append(melody)
    # mymelody.show()
    return mymelody'''


def writeMelody(desc, mykey, melody):
    partlength = melody.quarterLength
    posspatternparts = ['f', 'h', 'q', 'e']
    possnotes = list(range(8))

    notelength = {
        'f': 1,
        'h': 0.5,
        'q': 0.25,
        'e': 0.125
    }

    # availablepattern = [['h', 'q', 'q', 'h', 'h']]
    availablepattern = [
                        [('h'), ('q', 'q', 'q', 'q'), ('h')],
                        [('f'), ('h'), ('h')],
                        [('h'), ('h'), ('h') , ('h')],
                        [('h', 'q', 'q'), ('h', 'q', 'q')],
                        [('f'), ('f')]
                       ]


    currentpattern = availablepattern[rn.choice(range(len(availablepattern)))]

    basicpattern = {
        ('h')               : [(0,), (3,), (4,), (5,)],
        ('q', 'q', 'q', 'q'): [(0, 2, 4, 2), (0, 1, 2, 1), (0, 3, 4, 5), (0, 2, 3, 2), (2, 3, 4, 5), (3, 4, 3, 5),
                               (1, 4, 0, 6)],
        ('f')               : [(0,), (3,), (4,), (5,)],
        ('h', 'q', 'q')     : [(0, 2, 4), (0, 0, 0)]
    }

    chosenbasicpattern = {}
    for eachkey in basicpattern.keys():
        chosenbasicpattern[eachkey] = rn.choice(basicpattern[eachkey])

    print("~~~~~~~~~~")
    print(chosenbasicpattern)
    print("~~~~~~~~~~")

    currentduration = 0
    while currentduration < partlength:
       #print(currentpattern)
         for currentbasicpattern in currentpattern:
             durations = []
             for currentsinglepattern in list(currentbasicpattern):
                 # print(currentsinglepattern)
                 durations = durations + [notelength[currentsinglepattern]]
                 currentduration = currentduration + notelength[currentsinglepattern]
                 # melody.append(note.Note(mykey.pitches[currentnote], duration=duration.Duration(1)))
                 # melody.append(note.Note(mykey.pitches[i], duration=duration.Duration(notelength[el])))
             rootnote = rn.choice(basicpattern[('h')])[0]
             index = 0
             for currentnote in chosenbasicpattern[currentbasicpattern]:
                 #print(['duration'] + durations)
                 #print('index %i' % index)
                 #print('currentnote:')
                 #print(currentnote)
                 melody.append(note.Note(mykey.pitches[(currentnote + rootnote) % 7],
                                            duration=duration.Duration(durations[index])))
                 index = index + 1


    '''currentduration = 0
    while currentduration < partlength:
        #print(currentpattern)
        for currentbasicpattern in currentpattern:
            durations = []
            for currentsinglepattern in list(currentbasicpattern):
                # print(currentsinglepattern)

                durations = durations + [notelength[currentsinglepattern]]
                currentduration = currentduration + notelength[currentsinglepattern]
                # melody.append(note.Note(mykey.pitches[currentnote], duration=duration.Duration(1)))
                # melody.append(note.Note(mykey.pitches[i], duration=duration.Duration(notelength[el])))
            rootnote = rn.choice(basicpattern[('h')])[0]
            index = 0
            for currentnote in rn.choice(basicpattern[currentbasicpattern]):
                #print(['duration'] + durations)
                #print('index %i' % index)
                #print('currentnote:')
                #print(currentnote)
                melody.append(note.Note(mykey.pitches[(currentnote + rootnote) % 7],
                                        duration=duration.Duration(durations[index])))
                index = index + 1
    '''


def getKey(desc):
    supported = {
        "happy": ['ionian', 'lydian', 'mixolydian'],
        "sad": ['aeolian', 'dorian', 'phrygian'],
        "chaotic": ['locrian'],
        "simple": ['ionian', 'aeolian']
    }

    if 'key' in desc and desc["key"] is not None:
        tuple = desc["key"]
        try:
            mykey = key.Key(tuple[0], tuple[1])
            print(mykey)
            return mykey
        except Exception as e:
            print(type(e))
            sys.exit()

    if 'adj' in desc and desc["adj"] != []:
        try:
            mood = rn.choice(desc["adj"])
            if mood in supported.keys():
                mykey = key.Key(rn.choice(['a', 'b', 'c', 'd', 'e', 'f', 'g']), rn.choice(supported[mood]))
                desc["adj"] += [mood]
                return mykey
            else:
                print("error")
                print("Adjektiv: ", mood, " konnte nicht verwendet werden, nutze stattdessen random key")
        except TypeError as e:
            print(type(e))
            sys.exit()

    randommood = rn.choice(list(supported.keys()))
    desc["adj"] += [randommood]
    mykey = key.Key(rn.choice(['a', 'b', 'c', 'd', 'e', 'f', 'g']), rn.choice(supported[randommood]))
    return mykey


def writeChords(desc):
    if 'adj' in desc and 'simple' in desc["adj"]:
        while (True):
            chords = []
            currentchord = -1
            counter = 0
            while (counter != 4):
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
    return chords + chords


'''mykey = key.Key("C5")
    notesused = [0]*7

    part1     = stream.Score()
    part2     = stream.Score()
    part1.insert(0.0, instrument.Guitar())
    part2.insert(0.0, instrument.Guitar())

    mysong    = stream.Stream()

    for i in [1,2]:
         print(i)
         mychords = stream.Part()
         currentpitch     = 0
         currentpattern   = 0 

         patternlist = [] 
         notes                      = range(7)
         # Erstellt eine Markovkette mit Bias für jeden der Töne    
         notetransitionmatrix       = biasedrandompropmatrix(len(notes)  , 7, 0.7)
         #notetransitionmatrix       = randompropmatrix(len(notes)  , 7)

         # Wählt 3 zufällige Pattern auf Grundlage der Markovkette des Grundtons 
         for _ in range (1,3):   
             patternlist += [([np.random.choice(notes, replace = True, p=notetransitionmatrix[0]) for _ in range(rn.randint(0,3))]) ] 

         # Erstellt eine Markovkette für die Pattern
         patterntransitionmatrix    = randompropmatrix(len(patternlist), len(patternlist))

         # Wählt 8 zufällige Akkorde der Tonart auf Grundlage der Markovkette des Grundtons,4,0,0,4,3,5]])
         mychords.append([getChord(mykey, v, duration=duration.Duration(2)) for v in 
                         [np.random.choice(notes, replace = True, p=notetransitionmatrix[currentpitch]) for _ in range(8)]])
         # mychords.append([getChord(mykey, i, duration=duration.Duration(4)) for i in [0,3]

         mymelody = stream.Part()

         singlenoteduration = 1

         while mymelody.quarterLength < mychords.quarterLength:
                 mynotes  = stream.Part()
                 if(between(rn.randint(0,4), 3, 5)):
                         currentpattern = np.random.choice(range(len(patternlist)), replace = True, p=patterntransitionmatrix[currentpattern])
    #                     print("the current pattern is: {dings}".format(dings=patternlist[currentpattern]))
                         for r in patternlist[currentpattern]:
                               notesused[r]+=1
                               mynotes.append(note.Note (pitch    = mykey.pitches[r], 
                                                         duration = duration.Duration(singlenoteduration)))
                 else:
                         currentpitch   = np.random.choice(notes, replace = True, p=notetransitionmatrix[currentpitch])
     #                    print("the current note is: {dings}".format(dings=currentpitch))    
                         notesused[currentpitch]+=1           
                         mynotes.append(note.Note (pitch = mykey.pitches[currentpitch], 
                                                   duration = duration.Duration(singlenoteduration)))
                 if((mymelody.quarterLength + mynotes.quarterLength) <= mychords.quarterLength):
                      mymelody.append(mynotes.flat)
                 mymelody = mymelody.flat
         if(i==1):
            #part1.insert(0, mychords)
            #part1.insert(0, mymelody)
            part1.append( mychords)
            part1.append( mymelody)
         else:
            part2.insert(0, mychords)
            part2.insert(0, mymelody)
    part1.show('text')         
    #part2.show('text')
    #mysong.insert(0, part1)
    for anypart in part1.getElementsByClass(stream.Part):
        mysong.repeatInsert(anypart, [0,1])
    #mysong.show('text')
    # mysong.repeatInsert(part2, [part1.quarterLength, part1.quarterLength*2+part2.quarterLength])
    #mysong.insert(0, mychords)
    #mysong.insert(0, mymelody)

    print(notesused) 
    #mysong.show('midi')
    #s1 = stream.Stream()
    #s1.append(mysong)
    #s1.show('text')
    #s1.show()
    #mysong.show()
'''


def getPatternList(cP):
    #  return [[cP], [cP+4, cP+3, cP], [cP, cP+1, cP+2],[cP, cP+1, cP+2, cP ], [cP, cP+1, cP, cP+2 ]]
    return [[cP], [cP + 4, cP + 3, cP], [cP], [cP], [cP, cP + 1, cP + 2, cP], [cP], [cP, cP + 1, cP, cP + 2], [cP]]


def randompropmatrix(i, c):
    completelist = []
    for p in range(c):
        matrix = []
        matrix2 = []
        factor = 0.8
        for _ in range(i):
            matrix += [rn.randint(0, 100)]
        summe = sum(matrix)
        for x in matrix:
            matrix2 += [((x / summe))]
        if (c == 1):
            return matrix2
        completelist += [matrix2]

    return completelist


def biasedrandompropmatrix(i, c, bias):
    completelist = []
    for p in range(c):
        matrix = []
        matrix2 = []
        factor = 0.8
        for _ in range(i):
            matrix += [rn.randint(0, 100)]
        summe = sum(matrix)
        for x in matrix:
            matrix2 += [((x / summe) * bias)]
        for x in [0, 3, 4]:
            matrix2[x] += (1 - bias) / 3
        if (c == 1):
            return matrix2
        completelist += [matrix2]
    return completelist


def between(i, p, q):
    return ((i >= p) and (i < q))


def getChordOld(akey, i, **kwargs):
    return chord.Chord([akey.pitches[i],
                        akey.pitches[(i + 2) % 7],
                        akey.pitches[(i + 4) % 7]], forceOctave=4 ** kwargs)  # .transpose(-12)


def getChord(akey, i, **kwargs):
    one = akey.pitches[i]
    if (i + 2 > 6):
        two = akey.pitches[(i + 2) % 7].transpose(12)
    else:
        two = akey.pitches[(i + 2)]
    if (i + 4 > 6):
        three = akey.pitches[(i + 4) % 7].transpose(12)
    else:
        three = akey.pitches[(i + 4)]
    return chord.Chord([one, two, three], **kwargs)
    '''return chord.Chord([akey.pitches[i], 
                        akey.pitches[(i+2)%7], 
                        akey.pitches[(i+4)%7]], **kwargs)#.transpose(-12)
     '''


if __name__ == "__main__":
    main()