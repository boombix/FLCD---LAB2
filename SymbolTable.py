class SymbolTable:

    def __init__(self, size):
        self.size = size
        self.st = {}

    def get_st(self):
        return self.st

    def calculateAsciiSum(self, string):
        ascii_sum = 0
        for item in string:
            ascii_sum += ord(item)
        return ascii_sum

    def addToken(self, token):
        if token not in self.st.values():
            position = self.calculateAsciiSum(token) % self.size
            while position in self.st:
                position = position + 1
            self.st[position] = token
            print("Token ", token, " added on position", position)
            return position

        else:
            position = self.calculateAsciiSum(token) % self.size
            if self.st[position] == token:
                print("Token ", token, " already added on position", position)
                return position
            else:
                while self.st[position] != token:
                    position += 1
                print("Token ", token, " already added on position", position)
                return position

    def searchToken(self, token):
        if token in self.st.values():
            position = self.calculateAsciiSum(token) % self.size
            while position in self.st:
                if self.st[position] == token:
                    return position
                else:
                    position += 1
            return position
        else:
            return -1


def test():
    print("Add test:")
    ST = SymbolTable(1000)
    ST.addToken("ab")
    ST.addToken("ba")
    ST.addToken("2")
    ST.addToken("abc")
    ST.addToken("bca")
    ST.addToken("cab")
    ST.addToken("2")
    ST.addToken("maxim")
    ST.addToken("456")
    ST.addToken("a")

    print("Search test:")
    print(ST.searchToken("ba"))
    print(ST.searchToken("maxim"))
    print(ST.searchToken("bca"))
    print(ST.searchToken("eda"))

    print("The SymbolTable:")
    print(ST.get_st())


if __name__ == "__main__":
    test()