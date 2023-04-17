from networkx import MultiDiGraph
from typing import AbstractSet
from pyformlang.cfg import Variable, Epsilon, Terminal
from project.task_06.source import *

Node = object


def cfpq(
    target: MultiDiGraph,
    cfg: CFG,
    start_nodes: AbstractSet[Node] = None,
    final_nodes: AbstractSet[Node] = None,
    start_symbol: Variable = Variable("S"),
):
    """
    Returns all pairs of nodes u, v such that v is reachable from u in target graph under cfg constraints
    and u is from start nodes and v is from final nodes
    :param target: target graph
    :param cfg: context-free grammar
    :param start_nodes: start nodes
    :param final_nodes: final nodes
    :param start_symbol: start symbol
    :return: all pairs of nodes u, v such that v is reachable from u in graph under cfg constraints
    """
    start_nodes = target.nodes if start_nodes is None else start_nodes
    final_nodes = target.nodes if final_nodes is None else final_nodes
    return {
        (u, v)
        for (u, V, v) in hellings(cfg, target)
        if V == start_symbol and u in start_nodes and v in final_nodes
    }


def hellings(cfg: CFG, target: MultiDiGraph) -> AbstractSet[(Node, Variable, Node)]:
    prods: dict[str, set[Production]]
    res: AbstractSet[(Node, Variable, Node)]

    cfg = to_wcnf(cfg)

    TERM = "term"
    VAR = "var"
    EPS = "eps"

    prods = {TERM: set(), VAR: set(), EPS: set()}

    for production in cfg.productions:
        match production.body:
            case [Epsilon()]:
                prods[EPS].add(production)
            case [Terminal()]:
                prods[TERM].add(production)
            case [Variable(), Variable()]:
                prods[VAR].add(production)

    r = set()

    for (start, label, end) in target.edges(data="label"):
        for term_prod in prods[TERM]:
            if term_prod.body == label:
                r.add((term_prod.head, start, end))

    for eps_prod in prods[EPS]:
        for node in target.nodes:
            r.add((eps_prod.head, node, node))

    m = r.copy()

    while m:
        (n_i, v, u) = m.pop()
        for (n_j, v1, u1) in r:
            if u1 == v:
                for var_prod in prods[VAR]:
                    triple = (var_prod.head, v1, u)
                    if (
                        var_prod.body[0] == n_j
                        and var_prod.body[1] == n_i
                        and triple not in r
                    ):
                        m.add(triple)
                        r.add(triple)
        for (n_j, u1, v1) in r:
            if u1 == u:
                for var_prod in prods[VAR]:
                    triple = (var_prod.head, v, v1)
                    if (
                        var_prod.body[0] == n_i
                        and var_prod.body[1] == n_j
                        and triple not in r
                    ):
                        m.add(triple)
                        r.add(triple)

    res = set(map(lambda var, u, v: (u, var, v), r))

    return res
