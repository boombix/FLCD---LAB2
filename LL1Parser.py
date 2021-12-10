from Grammar import Grammar
from copy import deepcopy

class LL1Parser:

    def __init__(self, grammar: Grammar):
        self.grammar = grammar
        # first and follow will be dictionaries that have as keys all non-terminals and as values list containing terminals corresponding to first respectively follow
        self.FIRST = {}
        self.FOLLOW = {}
        self.M = {}
        self.constructFirst()
        self.constructFollow()
        self.constructTable()

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

        self.FOLLOW[self.grammar.S] = set("$")
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


    def calculateFirstForAlpha(self, alpha):
        firstAlpha = set()
        for index in range(0, len(alpha)):
            symbol = alpha[index]
            if symbol in self.grammar.Sigma:
                firstAlpha.add(symbol)
                break
            elif symbol in self.grammar.N:
                firstAlpha = firstAlpha.union(self.FIRST[symbol])
                if 'eps' in firstAlpha:
                    if index < len(alpha) - 1:
                        firstAlpha.remove('eps')
                    continue
                else:
                    break
        return firstAlpha



    def constructTable(self):
        self.M[("$", "$")] = "acc"
        for terminal in self.grammar.Sigma:
            if terminal != 'eps':
                self.M[(terminal, terminal)] = "pop"

        for lhs in self.grammar.P.keys():
            productions = self.grammar.P[lhs]
            for production in productions:
                productionList = production[0]
                firstAlpha = self.calculateFirstForAlpha(productionList)
                if 'eps' in firstAlpha:
                    followLhs = self.FOLLOW[lhs]
                    for symbol in followLhs:
                        if symbol == 'eps':
                            if (lhs, '$') in self.M.keys():
                                self.M[(lhs, '$')].append(production)
                                print("Production ", production, "with key, value", lhs, " $ ", " was added in a non emtpy cell!")
                            else:
                                self.M[(lhs, '$')] = [production]
                        else:
                            if (lhs,symbol) in self.M.keys():
                                self.M[(lhs, symbol)].append(production)
                                print("Production ", production, "with key, value", lhs, symbol,
                                      " was added in a non emtpy cell!")
                            else:
                                self.M[(lhs, symbol)] = [production]
                else:
                    for symbol in firstAlpha:
                        if (lhs, symbol) in self.M.keys():
                            self.M[(lhs, symbol)].append(production)
                            print("Production ", production, "with key, value", lhs, symbol,
                                  " was added in a non emtpy cell!")
                        else:
                            self.M[(lhs, symbol)] = [production]

    def evaluateSequence(self, seq):
        inputStack = seq.split(" ")
        inputStack.append("$")
        workingStack = [self.grammar.S, "$"]
        output = ""
        s = ""
        go = True
        while go:
            if inputStack[0] != workingStack[0]:
                if (workingStack[0], inputStack[0]) not in self.M.keys():
                    s = "error"
                    go = False
                else:
                    production = self.M[(workingStack[0], inputStack[0])][0]
                    productionList = production[0]
                    productionIndex = production[1]
                    workingStack.pop(0)
                    workingStack = productionList + workingStack
                    if 'eps' in workingStack:
                        workingStack.remove('eps')
                    output = output + str(productionIndex) + " "

            else:
                if self.M[(workingStack[0], inputStack[0])] == "pop":
                    workingStack.pop(0)
                    inputStack.pop(0)
                else:
                    if self.M[(workingStack[0], inputStack[0])] == "acc":
                        go = False
                        s = "accepted"
                    else:
                        go = False
                        s = "error"

        if s == "accepted":
            print("Sequence accepted")
            return output
        else:
            print("Sequence not accepted!")











if __name__ == "__main__":
    grammar = Grammar("g2.txt")
    print(grammar.searchProductionbyPI(2))
    parser = LL1Parser(grammar)
    parser.constructFirst()
    print(parser.FIRST)
    print(parser.isContainedInRhs("E'"))
    print(parser.FOLLOW)
    print(parser.calculateFirstForAlpha(["T", "E'"]))
    for pair in parser.M.items():
        print(pair)
    sequence = "( int ) + int"
    print(parser.evaluateSequence(sequence))
