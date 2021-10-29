import re
import pprint

from SymbolTable import SymbolTable


class Scanner:
    def __init__(self, file):
        self.operators = ["+", "-", '*', "%", "/", "=", "<", "<=", "==", ">=", ">"]
        self.separators = ["[", "]", "{", "}", "(", ")", ";", ",", " ", "\t", "\n", ":"]
        self.reservedWords = ["for", "char", "const", "do", "else", "if", "int", "float", "for", "while",
                              "bool", "true", "false", "cin", "cout"]
        self.st = SymbolTable(50)
        self.pif = []
        self.file = file

    def isIdentifier(self, token):
        if re.match('^[a-zA-Z0-9_]+$', token):
            return True
        return False

    def isIntegerConstant(self, token):
        if re.match('^[+|-]?[1-9][0-9]*$', token):
            return True
        return False

    def isStringConstant(self, token):
        if re.match('^".*"$', token):
            return True
        return False

    def isBoolConstant(self, token):
        if token == "true" or token == "false":
            return True
        else:
            return False

    def isAnOperator(self, char):
        for operator in self.operators:
            if char in operator:
                return True
        return False


    def tokenize(self, line):
        tokenList = []
        token = ''
        idx = 0
        while idx < len(line):
            #Operator
            if line[idx] in self.operators:
                if token:
                    tokenList.append(token)
                    token = ''
                while idx < len(line) and self.isAnOperator(line[idx]):
                    token += line[idx]
                    idx += 1
                tokenList.append(token)
                token = ''

            #Separator check
            elif line[idx] in self.separators:
                if token:
                    tokenList.append(token)
                token = line[idx]
                tokenList.append(token)
                idx += 1
                token = ''

            #String constant
            elif line[idx] == '\"':
                if token:
                    tokenList.append(token)
                    token = ''
                quotes = 0
                while idx < len(line) and quotes < 2:
                    if line[idx] == '\"':
                        quotes += 1
                    token += line[idx]
                    idx += 1
                tokenList.append(token)
                token = ''

            else:
                token += line[idx]
                idx += 1
        if token:
            tokenList.append(token)
        return tokenList


    def analyze(self):
        fileOpen = open(self.file, "r")
        lines = fileOpen.readlines()
        lineIndex = 1
        errors = []
        for line in lines:
            # line = line.split()
            tokenList = self.tokenize(line)
            for token in tokenList:
                if token in self.separators + self.operators + self.reservedWords:
                    if token == " " or token == '\n' or token == '\t' or token == "":
                        continue
                    self.pif.append((token, 0))
                elif self.isBoolConstant(token) or self.isStringConstant(token) or self.isIntegerConstant(token):
                    position = self.st.addToken(token)
                    self.pif.append(("constant", position))
                elif self.isIdentifier(token):
                    position = self.st.addToken(token)
                    self.pif.append(("identifier", position))
                else:
                    errors.append("Lexical error at line " + str(lineIndex) + " on token " + str(token))
            lineIndex += 1

        if(len(errors) == 0):
            with open('ST.out', 'w') as writer:
                writer.write(str(self.st.get_st()))

            with open('PIF.out', 'w') as writer:
                for tuple in self.pif:
                    message = str(tuple[0]) + "->" + str(tuple[1]) + '\n'
                    writer.write(message)
            print("Lexically correct!")

        else:
            for error in errors:
                print(error)


if __name__ == '__main__':
    scanner = Scanner("pb1err.txt")
    scanner.analyze()
