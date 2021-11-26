from FiniteAutomata import FiniteAutomata
from Grammar import Grammar


class Menu:
    def __init__(self, grammar: Grammar):
        self.grammar = grammar

    @staticmethod
    def print_Menu():
        print("========GRAMMAR========")
        print("What do you want to do?")
        print("1. Print the set of non-terminals")
        print("2. Print the set of terminals")
        print("3. Print starting symbol")
        print("4. Print productions")
        print("5. Print productions for a non-terminal")
        print("6. Check if grammar is context free")
        print("7. Exit")
        print('\n')

    def start(self):
        while True:
            self.print_Menu()
            cmd = input(">>>>")
            if cmd == '1':
                print(self.grammar.N)
            elif cmd == '2':
                print(self.grammar.Sigma)
            elif cmd == '3':
                print(self.grammar.S)
            elif cmd == '4':
                print(self.grammar.P)
            elif cmd == '5':
                nt = input("Give non terminal")
                print(self.grammar.P[nt])
            elif cmd == '6':
                print(self.grammar.verifyCFG())
            elif cmd == '7':
                exit()
            else:
                print("Bad command!!!")


if __name__ == '__main__':
    try:
        grammar = Grammar("g1.txt")
        menu = Menu(grammar)
        menu.start()
    except Exception as e:
        print(str(e))
