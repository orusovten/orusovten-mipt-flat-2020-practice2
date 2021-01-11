import pytest

from MyEarleyParser import EarlyParser, Situation


def test_predict():
    rules = {'S': ['S+P', 'P'], 'P': ['P*T', 'T'], 'T': ['(S)', 'x', 'y', 'z']}
    D = [set()]
    D[0].add(Situation("SS", "S", 0, 0))
    EarlyParser.predict(rules, D, 0)
    assert D[0] == {Situation('SS', 'S', 0, 0), Situation('S', 'S+P', 0, 0), Situation('S', 'P', 0, 0)}


def test_scan():
    word = "abc"
    D = [set(), set(), set()]
    D[1] = {Situation("S", "bGd", 0, 1), Situation("T", "rbbY", 0, 1), Situation("T", "bb+R", 1, 0)}
    EarlyParser.scan(word, D, 1)
    assert D[2] == {Situation('T', 'bb+R', 2, 0), Situation('S', 'bGd', 1, 1)}


def test_complete():
    D = [set() for i in range(3)]
    D[0] = {Situation('S', 'S+P', 0, 0), Situation('T', '(S)', 0, 0), Situation('T', 'x', 0, 0),
            Situation('P', 'T', 0, 0), Situation('S', 'P', 0, 0),
            Situation('T', 'y', 0, 0), Situation('T', 'z', 0, 0), Situation('P', 'P*T', 0, 0),
            Situation('SS', 'S', 0, 0)}
    D[1] = {Situation('T', '(S)', 1, 0), Situation('S', 'P', 0, 1), Situation('T', 'y', 0, 1),
            Situation('P', 'T', 0, 1),
            Situation('T', 'z', 0, 1),
            Situation('S', 'S+P', 0, 1), Situation('P', 'P*T', 0, 1), Situation('T', '(S)', 0, 1),
            Situation('T', 'x', 0, 1)}
    D[2].add(Situation('T', 'x', 1, 1))
    EarlyParser.complete(D, 2)
    assert D[2] == {Situation('T', 'x', 1, 1), Situation('P', 'T', 1, 1)}


def test_is_word_in_language():
    rules = {"S": ["S+P", "P"], "P": ["P*T", "T"], "T": ["(S)", "x", "y", "z"]}
    word = "(x+y)*z"
    parser = EarlyParser(rules)
    assert parser.is_word_in_language(word) is True
