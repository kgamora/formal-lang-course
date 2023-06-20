import pytest
import project  # on import will print something from __init__ file
from project.task_04.source import *
from pyformlang.regular_expression import PythonRegex


def setup_module(module):
    print("basic setup module")


def teardown_module(module):
    print("basic teardown module")


def test_rpq_for_start_states():
    m1_states: dict[State, int]
    m1_matrix: dict[Symbol, dok_matrix]

    regX: str = "a(b|c)"
    m1 = deterministic_state_machine_from_regex(regX)
    graph = m1.to_networkx()

    regX: str = "a(c|d)"
    result = rpq(
        graph=graph,
        regex=regX,
        start_states=m1.start_states,
        final_states=m1.final_states,
    )
    assert len(result) > 0


def test_rpq_for_start_states_2():
    regX: str = r"a|b*|d"
    m1 = deterministic_state_machine_from_regex(regX)
    graph = m1.to_networkx()
    regX: str = r"(b)(b)(b)(b)|c"
    m2 = deterministic_state_machine_from_regex(regX)
    result = rpq(
        graph=graph,
        regex=regX,
        start_states=m1.start_states,
        final_states=m1.final_states,
    )
    assert len(result) > 0


# def test_automata_rpq():
#     regX: str = "a(b|c)(a|c|d|b)"
#     m1 = deterministic_state_machine_from_regex(regX)
#     regX: str = "a(c|d)b"
#     assert rpq(m1, regX)
#     assert len(rpq(m1, regX)) == 1
#     regX: str = "a(c|d)(a*|b*)"
#     assert rpq(m1, regX)
