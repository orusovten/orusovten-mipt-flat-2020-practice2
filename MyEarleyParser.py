class Rule:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __eq__(self, other):
        return self.left == other.left and self.right == other.right

    def __hash__(self):
        return hash(self.left) + hash(self.right)


class Situation:
    def __init__(self, left_hand_side, right_hand_side, dot, start):
        self.rule = Rule(left_hand_side, right_hand_side)
        self.dot = dot
        self.start = start

    def __eq__(self, other):
        return self.rule == other.rule and self.dot == other.dot and self.start == other.start

    def __hash__(self):
        return hash(self.rule) + self.dot + self.start


class EarlyParser:
    nonterminals = [chr(number) for number in range(ord('A'), ord('Z'))]

    def __init__(self, rules_arg):
        self.rules = rules_arg
        self.D = list()

    @staticmethod
    def predict(rules, D, j):
        situations = D[j].copy()
        for situation in situations:
            if situation.dot < len(situation.rule.right):
                if situation.rule.right[situation.dot] in EarlyParser.nonterminals:
                    nonterminal = situation.rule.right[situation.dot]
                    for right in rules[nonterminal]:
                        D[j].add(Situation(nonterminal, right, 0, j))

    @staticmethod
    def scan(word, D, j):
        letters = set(word)
        for situation in D[j]:
            if situation.dot < len(situation.rule.right):
                if situation.rule.right[situation.dot] in letters:
                    if situation.rule.right[situation.dot] == word[j]:
                        D[j + 1].add(
                            Situation(situation.rule.left, situation.rule.right, situation.dot + 1, situation.start))

    @staticmethod
    def complete(D, j):
        situations = D[j].copy()
        for situation in situations:
            if situation.dot == len(situation.rule.right):
                for second_situation in D[situation.start]:
                    if second_situation.dot < len(second_situation.rule.right):
                        if second_situation.rule.right[second_situation.dot] in EarlyParser.nonterminals:
                            if second_situation.rule.right[second_situation.dot] == situation.rule.left:
                                D[j].add(Situation(second_situation.rule.left, second_situation.rule.right,
                                                   second_situation.dot + 1, second_situation.start))

    def predict_complete_loop(self, j):
        prev_len = len(self.D[j]) - 1
        while prev_len != len(self.D[j]):
            prev_len = len(self.D[j])
            self.predict(self.rules, self.D, j)
            self.complete(self.D, j)

    def is_word_in_language(self, word) -> bool:
        self.D = [set() for i in range(len(word) + 1)]
        self.D[0].add(Situation("SS", "S", 0, 0))
        self.predict_complete_loop(0)
        for j in range(1, len(word) + 1):
            self.scan(word, self.D, j - 1)
            self.predict_complete_loop(j)
        return Situation("SS", "S", 1, 0) in self.D[len(word)]


if __name__ == '__main__':
    rules = dict()
    word = ""
    while True:
        rule = input().split("->")
        if len(rule) == 1:
            word = rule[0]
            break
        rules.update({rule[0]: rule[1].split('|')})
    parser = EarlyParser(rules)
    print(parser.is_word_in_language(word))
