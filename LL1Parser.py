from Grammar import Grammar


class LL1Parser:

    def __init__(self, grammar: Grammar):
        self.grammar = grammar
        # first and follow will be dictionaries that have as keys all non-terminals and as values list containing terminals corresponding to first respectively follow
        self.FIRST = {}
        self.FOLLOW = {}


    def constructFirstForAlpha(self, remainingSymbols: list):
        pass


    def constructFirst(self):
        for lhs in self.grammar.P.keys():
            self.FIRST[lhs] = set()
            currentSet = set()
            productions = self.grammar.P[lhs]
            # print(productions)
            for production in productions:
                productionList = production[0]
                if productionList[0] in self.grammar.Sigma:
                    currentSet.add(productionList[0])
            if currentSet != self.FIRST[lhs]:
                self.FIRST[lhs] = self.FIRST[lhs].union(currentSet)

        hasChangedMare = True
        print(self.FIRST)
        while hasChangedMare:
            hasChangedMare = False
            for lhs in self.grammar.P.keys():
                productions = self.grammar.P[lhs]
                for production in productions:
                    initialSet = self.FIRST[lhs]
                    productionList = production[0]
                    hasChangedMic = False
                    index = 0
                    while index < len(productionList):
                        if productionList[index] in self.grammar.N:
                            self.FIRST[lhs] = self.FIRST[lhs].union(self.FIRST[productionList[index]])
                            if 'eps' not in currentSet:
                                break
                            index += 1
                    if initialSet != self.FIRST[lhs]:
                        hasChangedMare = True

                #     if productionList[0] in self.grammar.N:
                #         self.FIRST[lhs] = self.FIRST[lhs].union(self.FIRST[productionList[0]])
                #     while 'eps' in self.FIRST[lhs] and index < len(productionList):
                #         self.FIRST[lhs].remove('eps')
                #         self.FIRST[lhs] = self.FIRST[lhs].union(self.FIRST[productionList[index]])
                #         index += 1
                # hasChangedMare = False

        print(self.FIRST)



    def constructFollow(self):
        pass

if __name__ == "__main__":
    grammar = Grammar("g3.txt")
    parser = LL1Parser(grammar)
    parser.constructFirst()