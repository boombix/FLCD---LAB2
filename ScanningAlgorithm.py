from SymbolTable import SymbolTable
import re

class Scanner:
    def __init__(self, size, file):
        self.st = SymbolTable(50)
        self.pif = {}
        self.file = file

    def readFile(self):
        fileOpen = open(self.file, "r")
        tokens = []
        lines = fileOpen.readlines()
        for line in lines:
            line2 = line.split(" ")
            lineReg = re.split('; |, | \n', line)
            print(lineReg)
            print(line2)
            for linen in line2:
                line3 = linen.split(",")
                if line3 != "\n":
                    print(line3)
            # words = line.split(" ")
            # print(words, "\n")

    def getIdentifier(self, line):
        pass



if __name__ == "__main__":
    scanner = Scanner(20, "pb1.txt")
    scanner.readFile()