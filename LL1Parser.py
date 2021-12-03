from Grammar import Grammar
from copy import deepcopy

class LL1Parser:

    def __init__(self, grammar: Grammar):
        self.grammar = grammar
        # first and follow will be dictionaries that have as keys all non-terminals and as values list containing terminals corresponding to first respectively follow
        self.FIRST = {}
        self.FOLLOW = {}
        self.constructFirst()
        self.constructFollow()

    def constructFirst(self):
        hasChanged = False
        for lhs in self.grammar.P.keys():
            self.FIRST[lhs] = set()
            currentSet = deepcopy(self.FIRST[lhs])
            productions = self.grammar.P[lhs]
            for production in productions:
                productionList = production[0]
                if productionList[0] in self.grammar.Sigma:
                    currentSet.add(productionList[0])

            if len(self.FIRST[lhs]) != len(currentSet):
                self.FIRST[lhs] = currentSet
                hasChanged = True

        while hasChanged:
            hasChanged = False
            for lhs in self.grammar.P.keys():
                currentSet = self.FIRST[lhs]
                productions = self.grammar.P[lhs]
                for production in productions:
                    productionList = production[0]

                    copyCurrentSet = deepcopy(currentSet)
                    for symbol in productionList:
                        if symbol in self.grammar.N:
                            for additional_symbol in self.FIRST[symbol]:
                                if additional_symbol != 'eps':
                                    copyCurrentSet.add(additional_symbol)
                            if 'eps' not in self.FIRST[symbol]:
                                break
                            else:
                                if symbol != productionList[len(productionList) - 1]: # there are still some symbols in the productions to be checked
                                    continue
                                copyCurrentSet.add('eps')
                                break
                        else:
                            copyCurrentSet.add(symbol)
                            break

                    currentSet = currentSet.union(copyCurrentSet)

                    if len(self.FIRST[lhs]) != len(currentSet):
                        self.FIRST[lhs] = currentSet
                        hasChanged = True

    def constructFollow(self):
        hasChanged = False
        self.FOLLOW[self.grammar.S] = set("eps")

        for lhs in self.grammar.P.keys():
            self.FOLLOW[lhs] = set()
            hasChanged = True

        while hasChanged:
            hasChanged = False
            for lhs in self.grammar.P.keys():
                productionsContainingNonTerminal = self.isContainedInRhs(lhs)
                currentSet = deepcopy(self.FOLLOW[lhs])

                for production_key, p in productionsContainingNonTerminal.items():
                    for production in p:
                        copyCurrentSet = deepcopy(currentSet)
                        for symbol in production:
                            if symbol == lhs:
                                if symbol != production[len(production) - 1]:
                                    next_symbol = production[production.index(symbol) + 1]
                                    if next_symbol in self.grammar.Sigma:
                                        currentSet.add(next_symbol)
                                        break
                                    # elif next_symbol == production[len(production) - 1]: ceva ceva to be done daca e ultimu in secventa
                                    #     pass
                                        # currentSet = currentSet.union(self.FOLLOW[production_key])
                                    else:
                                        currentSet = currentSet.union(self.FIRST[next_symbol])
                                        if 'eps' in self.FIRST[next_symbol]:
                                            currentSet.remove('eps')
                                            currentSet = currentSet.union(self.FOLLOW[production_key])
                                else:
                                    currentSet = currentSet.union(self.FOLLOW[production_key])

                        if len(self.FOLLOW[lhs]) != len(currentSet):
                            self.FOLLOW[lhs] = currentSet
                            hasChanged = True


    def isContainedInRhs(self, nonTerminal):
        productionsContainingNonTerminal = {}
        for lhs in self.grammar.P.keys():
            productions = self.grammar.P[lhs]
            for production in productions:
                productionList = production[0]
                for symbol in productionList:
                    if symbol == nonTerminal:
                        if lhs in productionsContainingNonTerminal.keys():
                            productionsContainingNonTerminal[lhs].append(productionList)
                        else:
                            productionsContainingNonTerminal[lhs] = [productionList]

        return productionsContainingNonTerminal


if __name__ == "__main__":
    grammar = Grammar("g3.txt")
    parser = LL1Parser(grammar)
    parser.constructFirst()
    print(parser.FIRST)
    print(parser.isContainedInRhs("E'"))
    print(parser.FOLLOW)