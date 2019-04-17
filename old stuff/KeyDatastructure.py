from music21 import * 
import random as rn
import numpy  as np
import sys

#environment.set('midiPath', '/home/sturmd00/.local/bin/wildmidi_silent')
#äenvironment.set('musicxmlPath', '/home/sturmd00/.local/bin/musescore')

environment.set("musicxmlPath", r"C:\Program Files\MuseScore 3\bin\MuseScore3.exe")


def main():

   description = {
                  #"key"       : ('a', 'aeolian'), 
                  "key"       : None, 
                  "speed"     : [],
                  "melody"    : [],
                  "chords"    : [],
                  "adj"       : None, #["sad", "happy"]
                }
   key = getKey(description)
   
   print(key)



def getKey(desc):
   supported = {
                "happy"   : ['ionian' , 'lydian', 'mixolydian'],
                "sad"     : ['aeolian', 'dorian', 'phrygian'],
                "chaotic" : ['locrian']
               }

   if 'key' in desc and desc["key"] is not None:
      tuple = desc["key"]
      try:
         mykey = key.Key(tuple[0], tuple[1])
         print (mykey)
         return mykey
      except:
         print("Kein gültiger Key")
         sys.exit()

   if 'adj' in desc and desc["adj"] is not None:
      try:
         mood = rn.choice(desc["adj"])
         print(mood)
         if mood in supported.keys():
            mykey  = key.Key('c', 'aeolian')
            mykey = key.Key(rn.choice(['a','b','c','d','e','f','g']), rn.choice(supported[mood])) 
            return mykey
         else:
            print("error")
            print("Adjektiv: ", mood, " konnte nicht verwendet werden, nutze stattdessen random key")
      except TypeError as e:
         print(type(e))
         sys.exit()
         
   randommood = rn.choice(list(supported.keys()))
   print("Randommood", randommood)
   mykey  = key.Key(rn.choice(['a','b','c','d','e','f','g']), rn.choice(supported[randommood])) 
   return mykey      
    











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
     return [[cP], [cP+4, cP+3, cP], [cP], [cP], [cP, cP+1, cP+2, cP ],[cP], [cP, cP+1, cP, cP+2 ],[cP]]

def randompropmatrix(i, c):
   
   completelist = []
   for p in range(c):
        matrix  = []
        matrix2 = []
        factor  = 0.8
        for _ in range(i):
                matrix += [rn.randint(0, 100)]
        summe  = sum(matrix)
        for x in matrix:
             matrix2  += [((x/summe))]
        if(c==1):
             return matrix2
        completelist+=[matrix2]

   return completelist

def biasedrandompropmatrix(i, c, bias):
   
   completelist = []
   for p in range(c):
        matrix  = []
        matrix2 = []
        factor  = 0.8
        for _ in range(i):
                matrix += [rn.randint(0, 100)]
        summe  = sum(matrix)
        for x in matrix:
             matrix2  += [((x/summe)*bias)]
        for x in [0,3,4]:
                 matrix2[x] += (1-bias)/3
        if(c==1):
             return matrix2
        completelist+=[matrix2]
   return completelist

def between(i, p, q):
        return ((i >= p) and (i < q))

def getChordOld(akey, i, **kwargs):
       return chord.Chord([akey.pitches[i], 
                           akey.pitches[(i+2)%7], 
                           akey.pitches[(i+4)%7]], **kwargs)#.transpose(-12)
        

def getChord(akey, i, **kwargs):
       one = akey.pitches[i]
       if(i+2 > 6):
          two = akey.pitches[(i+2)%7].transpose(12)
       else:
          two = akey.pitches[(i+2)]
       if(i+4 > 6):
          three = akey.pitches[(i+4)%7].transpose(12)
       else:
          three = akey.pitches[(i+4)]
       return chord.Chord([one, two, three], **kwargs)     
       '''return chord.Chord([akey.pitches[i], 
                           akey.pitches[(i+2)%7], 
                           akey.pitches[(i+4)%7]], **kwargs)#.transpose(-12)
        '''
if __name__ == "__main__":
    main()
