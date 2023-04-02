import pytest
import project  # on import will print something from __init__ file
from project.task_02.source import deterministic_state_machine_from_regex
from project.task_02.source import non_deterministic_state_machine_from_graph
from project.task_01.source import make_double_cycled_graph


def setup_module(module):
    print("basic setup module")


def teardown_module(module):
    print("basic teardown module")


def test_regex_to_dsm():
    regX: str = "a(b|c)"
    assert deterministic_state_machine_from_regex(regX).accepts("ac")
    assert deterministic_state_machine_from_regex(regX).accepts("ab")
    assert not deterministic_state_machine_from_regex(regX).accepts("abc")
    assert not deterministic_state_machine_from_regex(regX).accepts("ca")
    assert not deterministic_state_machine_from_regex(regX).accepts("c")


def test_2():
    graph = make_double_cycled_graph(7, 3, ("a", "b"))
    start_states = {1, 5, 2}
    final_states = {7, 3, 4}
    res = non_deterministic_state_machine_from_graph(graph, start_states, final_states)
    assert res.start_states == start_states
    assert res.final_states == final_states
