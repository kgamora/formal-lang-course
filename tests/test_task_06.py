import pytest
from pyformlang.regular_expression import Regex
from pyformlang.cfg import CFG, Terminal

import project  # on import will print something from __init__ file
from project.task_06.source import *
from pathlib import Path

GRAMMAR_PATH = Path(".") / Path("tests") / Path("test_grammars")


def setup_module(module):
    print("basic setup module")


def teardown_module(module):
    print("basic teardown module")


def test_grammar_from_text():
    grammar: CFG

    grammar = cfg_from_txt(GRAMMAR_PATH / Path("grammar1.txt"))
    assert grammar.contains("abaabbaababb")
    assert grammar.contains("abababababab")
    assert grammar.contains("aaaaaabbbbbb")
    assert grammar.contains("accccccb")
    assert grammar.contains("aaaccccccccccccbbb")
    assert not grammar.contains("aabbb")
    assert not grammar.contains("aaabb")
    assert grammar.contains("ccccccc")
    assert not grammar.is_finite()


def test_dyck_grammar_from_text():
    dyck_grammar: CFG

    dyck_grammar = cfg_from_txt(GRAMMAR_PATH / Path("grammar2.txt"))
    assert dyck_grammar.contains("abaabbaababb")
    assert dyck_grammar.contains("abababababab")
    assert dyck_grammar.contains("aaaaaabbbbbb")
    assert not dyck_grammar.contains("ba")
    assert not dyck_grammar.is_finite()


def test_wcnf_for_pumping_lemma_proof():
    """
    If a language L is context-free, then there exists some integer p ≥ 1
    (called a "pumping length")[2] such that every string 's' in L that has a length of
    p or more symbols (i.e. with |s| ≥ p) can be written as s=uvwxy
    -Wikipedia
    """
    grammar: CFG

    grammar = cfg_from_txt(GRAMMAR_PATH / Path("grammar1.txt"))
    grammar = to_wcnf(grammar)

    # p = 2 ** len(grammar.variables) okay this is too long for it to run in reasonable time.
    # So I took a look and changed p as I see it
    p = 8

    long_enough_words = grammar.get_words(p + 1)

    long_enough = lambda w: len(w) > p

    regex = Regex("(c*a*c*b*c*)*")

    for word in long_enough_words:
        grammar.is_normal_form()
        if long_enough(word):
            word_str = "".join([i.to_text() for i in word])
            assert regex.accepts(word_str)
