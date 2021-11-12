class FiniteAutomata:
    def __init__(self, fileName):
        self.Q = []
        self.Sigma = []
        self.Delta = {}
        self.q0 = ''
        self.F = []
        self.fileName = fileName
        self.readFA()

    def readFA(self):
        with open(self.fileName) as file:
            self.Q = set(file.readline().strip().split(" "))
            for state in self.Q:
                if len(state) > 2:
                    raise Exception("Length of state ", state, " is greater than 1")
                if not state[0].islower():
                    raise Exception("First part of the state ", state, " must be a lower letter")
                if len(state) == 2 and not state[1].isdigit():
                    raise Exception("Second part of the state ", state, " must be a digit or nothing")

            self.Sigma = file.readline().strip().split(" ")
            self.q0 = file.readline().strip()
            if self.q0 not in self.Q:
                raise Exception("Initial state not in the set of states")
            self.F = set(file.readline().strip().split(" "))
            for finalState in self.F:
                if finalState not in self.Q:
                    raise Exception("Final state ", state, " not in the set of states")
            line_idx = 5
            for line in file:
                source = line.split("=")[0].strip().split(",")[0]
                if source not in self.Q:
                    raise Exception("Source ", source, " of the transition ", line, " on line ", line_idx, " is not part of the set of states")
                symbol = line.split("=")[0].strip().split(",")[1]
                if symbol not in self.Sigma:
                    raise Exception("Symbol ", symbol, " of the transition ", line, " on line ", line_idx,
                                    " is not part of the alphabet")
                destination = line.split("=")[1].strip()
                if destination not in self.Q:
                    raise Exception("Destination ", destination, " of the transition ", line, " on line ", line_idx, " is not part of the set of states")
                if (source, symbol) in self.Delta.keys():
                    if destination in self.Delta[(source, symbol)]:
                        raise Exception("Transition ", line, " on line ", line_idx, "already exists!")
                    else:
                        self.Delta[(source, symbol)].append(destination)
                else:
                    self.Delta[(source, symbol)] = [destination]
                line_idx += 1

    def verifyDeterministic(self):
        for key in self.Delta.keys():
            if len(self.Delta[key]) > 1:
                return False
        return True

    def verifySequence(self, sequence):
        if self.verifyDeterministic():
            state = self.q0
            for element in sequence:
                if (state, element) in self.Delta.keys():
                    state = self.Delta[(state, element)][0]
                else:
                    return False
            if state in self.F:
                return True
            return False
        else:
            print("Automaton is not deterministic!")
            return False

    def __str__(self):
        return "Q = { " + ', ' + self.Q.__str__() + " }\n" \
               + "Σ = { " + ', ' + self.Sigma.__str__() + " }\n" \
               + "q0 = { " + self.q0 + " }\n" \
               + "F = { " + ', ' + self.F.__str__() + " }\n" \
               + "δ = { " + self.Delta.__str__() + " } "
