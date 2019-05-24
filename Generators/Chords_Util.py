from music21 import *
import random as rn

class Chords_Util:

    def genChords(key, pattern, singlechordlength, beat, notesInChords):
        chords_music = stream.Part()
        for basenote in pattern:
            for singlebeat in beat:
                if singlebeat == 0:
                    chord_music = note.Rest(duration=duration.Duration(singlechordlength))
                elif singlechordlength <= 0.125:
                    chord_music = Chords_Util.getChord(key, basenote, singlechordlength*singlebeat, notesInChords)
                else:
                    chord_music = Chords_Util.getChord(key, basenote, singlechordlength*singlebeat, notesInChords)
                chords_music.append(chord_music)
        return chords_music

    def getChord(key, basenote, singlechordlength, chordnotes):
        chord_music = stream.Part()
        mychord = chord.Chord(duration=duration.Duration(singlechordlength))
        mypitches = key.pitches
        for i in chordnotes:
               mychord.add(mypitches[(basenote+i)%len(mypitches)])
        return mychord


    def generatePopPattern(length=4):
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
        return chords