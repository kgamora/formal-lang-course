from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton.deterministic_finite_automaton import (
    DeterministicFiniteAutomaton,
)
from networkx import MultiDiGraph
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton
from pyformlang.finite_automaton import State
from infixpy import Seq


def deterministic_state_machine_from_regex(regex: str) -> DeterministicFiniteAutomaton:
    return Regex(regex).to_epsilon_nfa().minimize()


def non_deterministic_state_machine_from_graph(
    graph: MultiDiGraph, start_states=None, final_states=None
) -> NondeterministicFiniteAutomaton:
    nfa: NondeterministicFiniteAutomaton = (
        NondeterministicFiniteAutomaton.from_networkx(graph)
    )
    start_states = graph.nodes.items() if start_states is None else start_states
    final_states = graph.nodes.items() if final_states is None else final_states
    Seq(start_states).foreach(lambda state: nfa.add_start_state(State(state)))
    Seq(final_states).foreach(lambda state: nfa.add_final_state(State(state)))
    return nfa
