from pyformlang.finite_automaton import FiniteAutomaton
from project.task_03.source import fa_to_matrix
from project.task_02.source import deterministic_state_machine_from_regex
from pyformlang.finite_automaton import State, Symbol
from scipy.sparse import dok_matrix, kron, csr_matrix


def create_frontier(
    m1: FiniteAutomaton, target: FiniteAutomaton, start_states: set[State]
) -> dok_matrix:
    m1_states: dict[State, int]
    m1_matrix: dict[Symbol, dok_matrix]
    target_states: dict[State, int]
    target_matrix: dict[Symbol, dok_matrix]
    frontier: dok_matrix
    m1_start_row: dok_matrix

    m1_states, m1_matrix = fa_to_matrix(m1)
    target_states, target_matrix = fa_to_matrix(target)

    frontier = dok_matrix(
        (len(target_states), len(target_states) + len(m1_states)), dtype=bool
    )
    m1_start_row = dok_matrix((1, len(m1)), dtype=bool)

    for i in [m1_states[state] for state in start_states]:
        m1_start_row[0, i] = True

    for i in [target_states[state] for state in target.start_states]:
        frontier[i, i] = True
        frontier[i, len(target_states) :] = m1_start_row

    return frontier
