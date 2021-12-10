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
    def __init__(self, output, grammar):
        self.output = output.strip().split(" ")
        print(self.output)
        self.grammar = grammar
        self.root = Node(self.grammar.S, 0)
        self.index = 1
        self.derivationString = ""

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


if __name__ == "__main__":
    grammar = Grammar("g4.txt")
    parser = LL1Parser(grammar)
    sequence = "( int ) + int"
    result = parser.evaluateSequence(sequence)
    parserOutput = ParserOutput(result, grammar)
    parserOutput.constructDerivationString()
    print(parserOutput.derivationString)

