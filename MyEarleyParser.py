class EarlyParser:
    nonterminals = [chr(number) for number in range(ord('A'), ord('Z'))]
    letters = [chr(number) for number in range(ord('a'), ord('z'))]

    def __init__(self, rules_arg):
        self.rules = rules_arg
        self.D = list()

    def predict(self, j):
        situations = self.D[j].copy()
        for situation in situations:
            if situation[2] < len(situation[1]):
                if situation[1][situation[2]] in EarlyParser.nonterminals:
                    nonterminal = situation[1][situation[2]]
                    for right in self.rules[nonterminal]:
                        self.D[j].add((nonterminal, right, 0, j))

    def scan(self, word, j):
        for situation in self.D[j]:
            if situation[2] < len(situation[1]):
                if situation[1][situation[2]] in self.letters:
                    if situation[1][situation[2]] == word[j]:
                        self.D[j + 1].add((situation[0], situation[1], situation[2] + 1, situation[3]))

    def complete(self, j):
        situations = self.D[j].copy()
        for situation in situations:
            if situation[2] == len(situation[1]):
                for second_situation in self.D[situation[3]]:
                    if second_situation[2] < len(second_situation[1]):
                        if second_situation[1][second_situation[2]] in EarlyParser.nonterminals:
                            if second_situation[1][second_situation[2]] == situation[0]:
                                self.D[j].add((second_situation[0], second_situation[1],
                                               second_situation[2] + 1, second_situation[3]))

    def is_word_in_language(self, word) -> bool:
        self.D = [set() for i in range(len(word) + 1)]
        self.letters = set(word)
        self.D[0].add(("SS", "S", 0, 0))
        while True:
            prev_len = len(self.D[0])
            self.predict(0)
            self.complete(0)
            if prev_len == len(self.D[0]):
                break
            prev_len = len(self.D[0])
        print(0, self.D[0])
        for j in range(1, len(word) + 1):
            self.scan(word, j - 1)
            while True:
                prev_len = len(self.D[j])
                self.predict(j)
                self.complete(j)
                if prev_len == len(self.D[j]):
                    break
                prev_len = len(self.D[j])
            print(j, self.D[j])
        return ("SS", "S", 1, 0) in self.D[len(word)]


if __name__ == '__main__':
    rules = dict()
    word = ""
    while True:
        rule = input().split("->")
        if len(rule) == 1:
            word = rule[0]
            break
        rules.update({rule[0]: rule[1].split('|')})
    print(rules)
    parser = EarlyParser(rules)
    print(parser.is_word_in_language(word))
