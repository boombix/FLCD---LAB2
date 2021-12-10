from Grammar import Grammar
from LL1Parser import LL1Parser


class Node:
    def __init__(self, info, index):
        self.info = info
        self.index = index
        self.parent = None
        self.leftSibling = None
        self.leftChild = None


class ParserOutput:
    def __init__(self, output, grammar, filename):
        self.output = output.strip().split(" ")
        print(self.output)
        self.grammar = grammar
        self.root = Node(self.grammar.S, 0)
        self.index = 1
        self.derivationString = ""
        self.fileName = filename


    def constructDerivationString(self):
        for index in self.output:
            productionTuple = self.grammar.searchProductionbyPI(int(index))
            self.derivationString += productionTuple[0] + " -> "
            for symbol in productionTuple[1]:
                self.derivationString += symbol + " "
            self.derivationString += "\n"

    def constructNode(self, node):
        productionIndex = int(self.output.pop(0))
        productionTuple = self.grammar.searchProductionbyPI(productionIndex)
        for symbol in productionTuple[1]:
            if symbol in self.grammar.Sigma:
                node = Node(symbol, self.index)

    def writeDerivationString(self):
        file = open(self.fileName, "a")
        file.write(self.derivationString)
        file.close()


if __name__ == "__main__":
    grammar = Grammar("g4.txt")
    parser = LL1Parser(grammar)
    sequence = "( int ) + int"
    print(parser.readSequenceFromFile("sequence.txt"))
    result = parser.evaluateSequence(sequence)
    parserOutput = ParserOutput(result, grammar, "g1out.txt")
    parserOutput.constructDerivationString()
    print(parserOutput.derivationString)
    parserOutput.writeDerivationString()

