from FiniteAutomata import FiniteAutomata


class Menu:
    def __init__(self, fa: FiniteAutomata):
        self.fa = fa

    @staticmethod
    def print_Menu():
        print("========FINITE AUTOMATON========")
        print("What do you want to do?")
        print("1. Print the set of states")
        print("2. Print the alphabet")
        print("3. Print all transitions")
        print("4. Print set of final states")
        print("5. Print initial state")
        print("6. Print all FA")
        print("7. Check a sequence")
        print("8. Exit")
        print('\n')

    def start(self):
        while True:
            self.print_Menu()
            cmd = input(">>>>")
            if cmd == '1':
                print(self.fa.Q)
            elif cmd == '2':
                print(self.fa.Sigma)
            elif cmd == '3':
                print(self.fa.Delta)
            elif cmd == '4':
                print(self.fa.F)
            elif cmd == '5':
                print(self.fa.q0)
            elif cmd == '6':
                print(self.fa)
            elif cmd == '7':
                sequence = input("Type your sequence:\n >>>>  ")
                if self.fa.verifySequence(sequence):
                    print("Sequence accepted")
                else:
                    print("Sequence not accepted")
            elif cmd == '8':
                exit()
            else:
                print("Bad command!!!")


if __name__ == '__main__':
    try:
        fa = FiniteAutomata("FA.in")
        menu = Menu(fa)
        menu.start()
    except Exception as e:
        print(str(e))
