import pytest
from pyformlang.regular_expression import Regex
from pyformlang.cfg import CFG, Terminal

import project  # on import will print something from __init__ file
from project.task_07.source import *
from project.task_06.source import *

GRAMMAR_PATH = Path(".") / Path("test_grammars")


def setup_module(module):
    print("basic setup module")


def teardown_module(module):
    print("basic teardown module")


def test_cyk():
    grammar: CFG

    grammar = cfg_from_txt(GRAMMAR_PATH / Path("grammar1.txt"))
    assert grammar.contains("abaabbaababb")
    assert cyk(grammar, "abaabbaababb")
    assert grammar.contains("abababababab")
    assert cyk(grammar, "abababababab")
    assert grammar.contains("aaaaaabbbbbb")
    assert cyk(grammar, "aaaaaabbbbbb")
    assert grammar.contains("accccccb")
    assert cyk(grammar, "accccccb")
    assert grammar.contains("aaaccccccccccccbbb")
    assert not grammar.contains("aabbb")
    assert not cyk(grammar, "aabbb")
    assert not grammar.contains("aaabb")
    assert not cyk(grammar, "aaabb")
    assert grammar.contains("ccccccc")
    assert cyk(grammar, "ccccccc")
    assert not grammar.is_finite()


def test_dyck_grammar_cyk():
    dyck_grammar: CFG

    dyck_grammar = cfg_from_txt(GRAMMAR_PATH / Path("grammar2.txt"))
    assert dyck_grammar.contains("abaabbaababb")
    assert cyk(dyck_grammar, "abaabbaababb")
    assert dyck_grammar.contains("abababababab")
    assert cyk(dyck_grammar, "abababababab")
    assert dyck_grammar.contains("aaaaaabbbbbb")
    assert cyk(dyck_grammar, "aaaaaabbbbbb")
    assert not dyck_grammar.contains("ba")
    assert not cyk(dyck_grammar, "ba")
    assert not dyck_grammar.is_finite()
