from project.task_02.source import deterministic_state_machine_from_regex
from pyformlang.finite_automaton import (
    FiniteAutomaton,
)
from pyformlang.finite_automaton import State, Symbol
from pyformlang.finite_automaton.deterministic_finite_automaton import (
    DeterministicFiniteAutomaton,
)
from scipy.sparse import dok_matrix, kron, csr_matrix


def fa_to_matrix(m1: FiniteAutomaton) -> (dict[State, int], dict[Symbol, dok_matrix]):
    """
    Auxiliary method to convert FiniteAutomaton into set of adjacency matrices for each symbol.
    :param m1: automaton to convert
    :return: first parameter is mapping from initial states of automaton to integers used in matrices
    """
    m1_states: dict[State, int]
    m1_matrix: dict[Symbol, dok_matrix]
    m1_states_cnt: int

    m1_matrix = dict()
    m1_states = {value: i for i, value in enumerate(m1.states)}
    m1_states_cnt = len(m1_states)
    edges = m1.to_dict()

    for start in edges:
        for label in edges[start]:
            if not isinstance(edges[start][label], set):
                edges[start][label] = {edges[start][label]}

            for final_state in edges[start][label]:
                if label not in m1_matrix:
                    m1_matrix[label] = dok_matrix(
                        (m1_states_cnt, m1_states_cnt), dtype=bool
                    )
                m1_matrix[label][(m1_states[start]), (m1_states[final_state])] = True

    return m1_states, m1_matrix


def intersect_sm(
    m1: DeterministicFiniteAutomaton, m2: DeterministicFiniteAutomaton
) -> DeterministicFiniteAutomaton:
    """
    Intersects two DFAs. Returns a DFA, which start and final states store the information
    about their origins in attribute "initial_states" in a tuple (m1_state, m2_state).
    :param m1: first automaton
    :param m2: second automaton
    :return: their intersection
    """
    m1_states: dict[State, int]
    m1_matrix: dict[Symbol, dok_matrix]
    m2_states: dict[State, int]
    m2_matrix: dict[Symbol, dok_matrix]

    m1_states, m1_matrix = fa_to_matrix(m1)
    m2_states, m2_matrix = fa_to_matrix(m2)

    labels: set[Symbol]
    start_states: set[State]
    final_states: set[State]
    m3_matrix: dict[Symbol, dok_matrix]

    labels = set(m1_matrix.keys()).union(set(m2_matrix.keys()))
    m1_matrix.update(
        {
            label: csr_matrix((len(m1_states), len(m1_states)), dtype=bool)
            for label in labels
            if label not in set(m1_matrix.keys())
        }
    )
    m2_matrix.update(
        {
            label: csr_matrix((len(m2_states), len(m2_states)), dtype=bool)
            for label in labels
            if label not in set(m2_matrix.keys())
        }
    )
    m3_matrix = {
        label: kron(m1_matrix[label], m2_matrix[label], format="csr")
        for label in labels
    }
    transitions = [
        (start_state, label, final_state)
        for label in m3_matrix
        for start_state, final_state in zip(
            m3_matrix[label].nonzero()[0], m3_matrix[label].nonzero()[1]
        )
    ]

    def create_state(m1_st: State, m1_i: int, m2_st: State, m2_i: int) -> State:
        res = State(m1_i * len(m2_states) + m2_i)
        res.initial_states = (m1_st, m2_st)
        return res

    all_states = {
        create_state(m1_state, m1_state_index, m2_state, m2_state_index)
        for m1_state, m1_state_index in m1_states.items()
        for m2_state, m2_state_index in m2_states.items()
    }

    start_states = {
        create_state(m1_state, m1_state_index, m2_state, m2_state_index)
        for m1_state, m1_state_index in m1_states.items()
        for m2_state, m2_state_index in m2_states.items()
        if m1_state in m1.start_states and m2_state in m2.start_states
    }
    final_states = {
        create_state(m1_state, m1_state_index, m2_state, m2_state_index)
        for m1_state, m1_state_index in m1_states.items()
        for m2_state, m2_state_index in m2_states.items()
        if m1_state in m1.final_states and m2_state in m2.final_states
    }

    result: DeterministicFiniteAutomaton
    result = DeterministicFiniteAutomaton()

    for start_state in start_states:
        result.add_start_state(start_state)

    for final_state in final_states:
        result.add_final_state(final_state)

    result.add_transitions(transitions)

    return result


def transitive_closure(
    m1: DeterministicFiniteAutomaton,
) -> (dict[State, int], dok_matrix):
    """Auxiliary method. Performs transitive closure on DFA,
    returning resulting matrix and mapping from states to values in this matrix."""
    m1_states: dict[State, int]
    m1_matrix: dict[Symbol, dok_matrix]

    m1_states, m1_matrix = fa_to_matrix(m1)
    result = sum(m1_matrix.values())
    prev, cur = result.nnz, 0
    while not prev == cur:
        result += result @ result
        prev, cur = cur, result.nnz
    return m1_states, result


def rpq(m1: DeterministicFiniteAutomaton, regex: str) -> set[State, State]:
    """
    Performs rpq for DFA and regex, returning set of pairs from DFA.
    :param m1: DFA
    :param regex: regex
    :return: set of pairs of states (start to final)
    """
    m1: DeterministicFiniteAutomaton
    m2: DeterministicFiniteAutomaton

    m2 = deterministic_state_machine_from_regex(regex)
    m3 = intersect_sm(m1, m2)

    states: dict[State, int]
    matrix: dok_matrix
    states, matrix = transitive_closure(m3)

    start, final = matrix.nonzero()
    res_pairs = list(zip(start, final))

    return {
        (start_state.initial_states[0], final_state.initial_states[0])
        for start_state in m3.start_states
        for final_state in m3.final_states
        if (states[start_state], states[final_state]) in res_pairs
    }
