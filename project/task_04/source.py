from pyformlang.finite_automaton import FiniteAutomaton
from project.task_03.source import fa_to_matrix
from pyformlang.finite_automaton import Symbol
from scipy.sparse import dok_matrix, block_diag, vstack
from project.task_02.source import *


def rpq(
    graph: MultiDiGraph,
    regex: str,
    start_states: set[State] = None,
    final_states: set[State] = None,
    each_start_states=False,
) -> set:
    m1: FiniteAutomaton
    target: FiniteAutomaton

    m1 = deterministic_state_machine_from_regex(regex=regex)
    target = non_deterministic_state_machine_from_graph(
        graph=graph, start_states=start_states, final_states=final_states
    )

    return bfs(target, m1, each_start_states)


def bfs(m1: FiniteAutomaton, target: FiniteAutomaton, each_start_states=False):
    """
    Disassembles both automatons. Solves reachability problem under CFL constraints.
    :param m1: automaton
    :param target: target automaton
    :param each_start_states:
    :return:
    """
    m1_states: dict[State, int]
    m1_matrix: dict[Symbol, dok_matrix]
    target_states: dict[State, int]
    target_matrix: dict[Symbol, dok_matrix]
    target_states_number: int

    target_states_number = len(target.states)

    m1_states, m1_matrix = fa_to_matrix(m1)
    target_states, target_matrix = fa_to_matrix(target)

    start_states_indices = [m1_states[state] for state in m1.start_states]
    bfs_frontier = (
        vstack(
            [
                create_frontier(
                    m1_states=m1_states,
                    target_states=target_states,
                    target_start_states=target.start_states,
                    start_states_indices={i},
                )
                for i in start_states_indices
            ]
        )
        if each_start_states
        else create_frontier(
            m1_states=m1_states,
            target_states=target_states,
            target_start_states=target.start_states,
            start_states_indices=set(start_states_indices),
        )
    )
    mat_sum = m_sum(m1_matrix=m1_matrix, target_matrix=target_matrix)
    visited = dok_matrix(bfs_frontier.shape, dtype=bool)
    while True:
        previously_visited = visited.copy()
        for dir_sum_matrix in mat_sum.values():
            new_frontier = (
                visited @ dir_sum_matrix
                if bfs_frontier is None
                else bfs_frontier @ dir_sum_matrix
            )
            visited += bfs_step(m1=m1, target=target, frontier=new_frontier)
        bfs_frontier = None
        if visited.nnz == previously_visited.nnz:
            break

    results = set()
    m1_states_states = [
        k for k, v in sorted(m1_states.items(), key=lambda item: item[1])
    ]
    target_states_states = [
        k for k, v in sorted(target_states.items(), key=lambda item: item[1])
    ]
    for i, j in zip(*visited.nonzero()):
        if (
            j >= target_states_number
            and target_states_states[i % target_states_number] in target.final_states
        ):
            m1_state = j - target_states_number
            if m1_states_states[m1_state] in m1.final_states:
                if each_start_states:
                    results.add(
                        (start_states_indices[i // target_states_number], m1_state)
                    )
                else:
                    results.add(m1_state)
    return results


def create_frontier(
    *,
    m1_states: dict[State, int],
    target_states: dict[State, int],
    target_start_states: set[State],
    start_states_indices: set[int]
) -> dok_matrix:
    """
    Auxiliary method for bfs. Creates frontier for bfs.
    :param m1_states: State to index mapping for automaton
    :param target_states: State to index mapping for target automaton
    :param target_start_states: Set of target automaton start states
    :param start_states_indices: indices of start states
    :return: dok_matrix - frontier for bfs
    """
    frontier: dok_matrix
    m1_start_row: dok_matrix
    m1_states_number: int
    target_states_number: int

    target_states_number = len(target_states)
    m1_states_number = len(m1_states)
    frontier = dok_matrix(
        (target_states_number, target_states_number + m1_states_number), dtype=bool
    )
    m1_start_row = dok_matrix((1, m1_states_number), dtype=bool)

    for i in start_states_indices:
        m1_start_row[0, i] = True

    for i in [target_states[state] for state in target_start_states]:
        frontier[i, i] = True
        frontier[i, target_states_number:] = m1_start_row

    return frontier


def bfs_step(
    *, m1: FiniteAutomaton, target: FiniteAutomaton, frontier: dok_matrix
) -> dok_matrix:
    """
    Auxiliary method for bfs. Performs one step of bfs
    :param m1: finite automaton
    :param target: target finite automaton
    :param frontier: dok_matrix - current bfs_frontier
    :return: dok_matrix - frontier after one step of bfs
    """
    m1_states_number: int
    target_states_number: int
    new_front: dok_matrix
    m1_states_number, target_states_number = len(m1.states), len(target.states)

    new_front = dok_matrix(frontier.shape, dtype=bool)
    for i, j in zip(*frontier.nonzero()):
        if j < target_states_number:
            m1_nnz = frontier[i, target_states_number:]
            if m1_nnz.nnz > 0:
                start_rows = i // target_states_number * target_states_number
                new_front[start_rows + j, j] = True
                new_front[start_rows + j, target_states_number:] += m1_nnz

    return new_front


def m_sum(
    *, m1_matrix: dict[Symbol, dok_matrix], target_matrix: dict[Symbol, dok_matrix]
) -> dict[Symbol, dok_matrix]:
    labels = set(m1_matrix.keys()).intersection(set(target_matrix.keys()))
    direct_sum = dict()
    for label in labels:
        direct_sum[label] = dok_matrix(
            block_diag((target_matrix[label], m1_matrix[label]))
        )
    return direct_sum
