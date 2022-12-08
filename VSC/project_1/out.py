import os
import platform

class OutputCom(object):
    # in many cases can be used for clear outputs in terminal
    @classmethod
    def clear(self):
        system = platform.system()
        
        if system == "Windows":
            os.system('cls')

        if system == "Linux":
            os.system('clear')

    # basic info print on output
    @classmethod
    def info(self):
        print("[INFO] VSC Project - simple ANN classificator")
        print("[INFO] Author: Martin Juricek")
        print("[INFO] Teacher: doc. Matousek Radomil")
        print("[INFO] Teacher: Ing. Ladislav Dobrovsky")
        print("[INFO] IACS FME BUT @2021")

    # this function print array in form [X1|X2|Classification],
    # i hope this mean "standardni vystup"
    @classmethod
    def print_data(self, points):
        print("[INFO][X1|X2|Classification]")
        for i in points:
            print("[INFO]" + str(i))