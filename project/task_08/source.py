from networkx import MultiDiGraph
from typing import AbstractSet
from pyformlang.cfg import Variable, Epsilon, Terminal
from project.task_06.source import *
from project.task_09.source import *

Node = object


def labeled_graph_from_text(edges: str) -> MultiDiGraph:
    graph = MultiDiGraph()
    graph.add_edges_from(edges)
    return graph


def labeled_graph_from_file(target: Path) -> MultiDiGraph:
    with open(target) as text:
        return labeled_graph_from_text(text.read())


def cfpq(
    target: MultiDiGraph | Path,
    cfg: CFG | Path,
    start_nodes: AbstractSet[Node] = None,
    final_nodes: AbstractSet[Node] = None,
    start_symbol: Variable = Variable("S"),
    implementation: str = "matrix",
):
    """
    Returns all pairs of nodes u, v such that v is reachable from u in target graph under cfg constraints
    and u is from start nodes and v is from final nodes
    :param target: target graph
    :param cfg: context-free grammar
    :param start_nodes: start nodes
    :param final_nodes: final nodes
    :param start_symbol: start symbol
    :param implementation: implementation of the algorithm - `matrix` or `hellings`
    :return: all pairs of nodes u, v such that v is reachable from u in graph under cfg constraints
    """
    target = labeled_graph_from_file(target) if isinstance(target, Path) else target
    cfg = cfg_from_txt(cfg) if isinstance(cfg, Path) else cfg
    start_nodes = target.nodes if start_nodes is None else start_nodes
    final_nodes = target.nodes if final_nodes is None else final_nodes

    match implementation:
        case "matrix":
            implementation = matrix
        case "hellings":
            implementation = hellings

    return {
        (u, v)
        for (u, V, v) in implementation(cfg, target)
        if V == start_symbol and u in start_nodes and v in final_nodes
    }


def hellings(cfg: CFG, target: MultiDiGraph):
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

    r = list()

    for (start, end, label) in target.edges(data="label"):
        for term_prod in prods[TERM]:
            if term_prod.body[0].value == label:
                r.append((term_prod.head, start, end))

    for eps_prod in prods[EPS]:
        for node in target.nodes:
            r.append((eps_prod.head, node, node))

    m = r.copy()

    while len(m) > 0:
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
                        m.append(triple)
                        r.append(triple)
        for (n_j, u1, v1) in r:
            if u1 == u:
                for var_prod in prods[VAR]:
                    triple = (var_prod.head, v, v1)
                    if (
                        var_prod.body[0] == n_i
                        and var_prod.body[1] == n_j
                        and triple not in r
                    ):
                        m.append(triple)
                        r.append(triple)

    res = set(map(lambda var: (var[1], var[0], var[2]), r))

    return res
