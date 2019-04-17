from Parts.generic_part import  *

class Intro(generic_part):

    def __init__(self, passedmusicpart, name):
        super().__init__(passedmusicpart, name)
        print("This is the {}".format(name))
