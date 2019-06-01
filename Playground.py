import json
from music21 import *
environment.set("musicxmlPath", r"C:\Program Files\MuseScore 3\bin\MuseScore3.exe")


mykey = key.Key("C")
mykey.show('text')
mystring = "tinyNotation: 4/4"
for pitch in mykey.pitches:
    mystring += " " + str(pitch.name)

print(mystring)
s = converter.parse("tinyNotation: 4/4 c8 d8 e8")
s.show('text')


s.show()