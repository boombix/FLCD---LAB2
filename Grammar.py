class Grammar:
    def __init__(self, fileName):
        self.N = []
        self.Sigma = []
        self.P = {}  # key represents left-hand side of the production, value is a list containing tuples of type (list with every element of the derivation, derivationIndex)
        self.S = ''
        self.fileName = fileName
        self.readGrammar()

    def readGrammar(self):
        with open(self.fileName) as file:
            self.N = set(file.readline().strip().split(" "))
            self.Sigma = file.readline().strip().split(" ")
            self.S = file.readline().strip()
            productionIndex = 1
            for line in file:
                leftHandSide = line.split("->")[0].strip()
                rightHandSide = line.split("->")[1].split("|")
                for i in range(0, len(rightHandSide)):
                    rightHandSide[i] = rightHandSide[i].lstrip().rstrip().split(" ")
                    if leftHandSide in self.P.keys():
                        tupleProd = rightHandSide[i], productionIndex
                        self.P[leftHandSide].append(tupleProd)
                        productionIndex += 1
                    else:
                        tupleProd = rightHandSide[i], productionIndex
                        self.P[leftHandSide] = [tupleProd]
                        productionIndex += 1

    def verifyCFG(self):
        for key in self.P.keys():
            if key not in self.N:
                return False
        return True

    def searchProductionbyPI(self, index):
        for lhs in self.P.keys():
            productions = self.P[lhs]
            for production in productions:
                productionIndex = production[1]
                if productionIndex == index:
                    return lhs, production[0]
