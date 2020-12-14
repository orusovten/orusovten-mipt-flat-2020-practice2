import pytest

from MyEarleyParser import EarlyParser


def test_predict():
    rules = {'S': ['S+P', 'P'], 'P': ['P*T', 'T'], 'T': ['(S)', 'x', 'y', 'z']}
    parser = EarlyParser(rules)
    parser.D = [set()]
    parser.D[0].add(("SS", "S", 0, 0))
    parser.predict(0)
    assert parser.D[0] == {('SS', 'S', 0, 0), ('S', 'S+P', 0, 0), ('S', 'P', 0, 0)}


def test_scan():
    word = "abc"
    parser = EarlyParser(dict())
    parser.letters = set(word)
    parser.D = [set(), set(), set()]
    parser.D[1] = {("S", "bGd", 0, 1), ("T", "rbbY", 0, 1), ("T", "bb+R", 1, 0)}
    parser.scan(word, 1)
    assert parser.D[2] == {('T', 'bb+R', 2, 0), ('S', 'bGd', 1, 1)}


def test_complete():
    parser = EarlyParser(dict())
    parser.D = [set() for i in range(3)]
    parser.D[0] = {('S', 'S+P', 0, 0), ('T', '(S)', 0, 0), ('T', 'x', 0, 0), ('P', 'T', 0, 0), ('S', 'P', 0, 0),
                   ('T', 'y', 0, 0), ('T', 'z', 0, 0), ('P', 'P*T', 0, 0), ('SS', 'S', 0, 0)}
    parser.D[1] = {('T', '(S)', 1, 0), ('S', 'P', 0, 1), ('T', 'y', 0, 1), ('P', 'T', 0, 1), ('T', 'z', 0, 1),
                   ('S', 'S+P', 0, 1), ('P', 'P*T', 0, 1), ('T', '(S)', 0, 1), ('T', 'x', 0, 1)}
    parser.D[2].add(('T', 'x', 1, 1))
    parser.complete(2)
    assert parser.D[2] == {('T', 'x', 1, 1), ('P', 'T', 1, 1)}
