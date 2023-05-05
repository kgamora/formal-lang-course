from typing import Any as Node
from networkx import MultiDiGraph
from project.task_06.source import *
from scipy.sparse import dok_matrix, eye
from pyformlang.cfg import Variable, Epsilon, Terminal


def matrix(cfg: CFG, target: MultiDiGraph):
    n: int
    # E: set[Edge]
    adjacency_mats: dict[Variable, dok_matrix]
    nodes_mapping: dict[Node, int]

    cfg = to_wcnf(cfg)
    TERM, VAR, EPS = "term", "var", "eps"
    prods = {TERM: set(), VAR: set(), EPS: set()}
    for production in cfg.productions:
        match production.body:
            case [Epsilon()]:
                prods[EPS].add(production)
            case [Terminal()]:
                prods[TERM].add(production)
            case [Variable(), Variable()]:
                prods[VAR].add(production)

    adjacency_mats = {
        var: dok_matrix((len(target.nodes), len(target.nodes)), dtype=bool)
        for var in cfg.variables
    }
    nodes_mapping = {node: i for i, node in enumerate(target.nodes)}

    for (start, end, label) in target.edges(data="label"):
        for production in prods[TERM]:
            adjacency_mats[production.head][
                nodes_mapping[start], nodes_mapping[end]
            ] |= (label == production.body[0].value)

    for adj in adjacency_mats.values():
        adj.tocsr()

    for production in prods[EPS]:
        adjacency_mats[production.head] += eye(
            len(nodes_mapping), dtype=bool, format="csr"
        )

    changes = True
    while changes:
        changes = False
        for production in prods[VAR]:
            prev_nnz = adjacency_mats[production.head].nnz
            adjacency_mats[production.head] += (
                adjacency_mats[production.body[0]] @ adjacency_mats[production.body[1]]
            )
            changes |= adjacency_mats[production.head].nnz != prev_nnz

    nodes_mapping = {i: n for n, i in nodes_mapping.items()}
    result = []

    for N, adj in adjacency_mats.items():
        for i, j in zip(*adj.nonzero()):
            result.append((nodes_mapping[i], N, nodes_mapping[j]))

    return result
