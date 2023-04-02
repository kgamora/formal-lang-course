import pytest
import project  # on import will print something from __init__ file
from project.task_03.source import *


def setup_module(module):
    print("basic setup module")


def teardown_module(module):
    print("basic teardown module")


def test_automata_intersect_basic():
    regX: str = "a(b|c)"
    m1 = deterministic_state_machine_from_regex(regX)
    regX: str = "a(c|d)"
    m2 = deterministic_state_machine_from_regex(regX)
    m3 = intersect_sm(m1, m2)
    assert m3.accepts("ac")
    assert m1.accepts("ab")
    assert not m3.accepts("ab")
    assert m2.accepts("ad")
    assert not m3.accepts("ad")


def test_automata_intersect_advanced():
    regX: str = r"a|b*|d"
    m1 = deterministic_state_machine_from_regex(regX)
    regX: str = r"(b)(b)(b)(b)|c"
    m2 = deterministic_state_machine_from_regex(regX)
    m3 = intersect_sm(m1, m2)
    assert m1.accepts("a")
    assert m2.accepts("c")
    assert not m2.accepts("a")
    assert m3.accepts("bbbb")


def test_automata_rpq():
    regX: str = "a(b|c)(a|c|d|b)"
    m1 = deterministic_state_machine_from_regex(regX)
    regX: str = "a(c|d)b"
    assert rpq(m1, regX)
    assert len(rpq(m1, regX)) == 1
    regX: str = "a(c|d)(a*|b*)"
    assert rpq(m1, regX)
