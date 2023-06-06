import pytest
from project.task_08.source import *
from project.task_06.source import *
import networkx

GRAMMAR_PATH = Path(".") / Path("tests") / Path("test_grammars")
GRAPH_PATH = Path(".") / Path("tests") / Path("test_graphs")


def setup_module(module):
    print("basic setup module")


@pytest.mark.parametrize(
    "cfg_path, graph_path, expected_cfpq, start_nodes, final_nodes",
    [
        (
            Path("grammar5.txt"),
            Path("graph1.dot"),
            {(1, 2), (0, 3), (2, 3), (0, 2), (2, 2), (1, 3)},
            None,
            None,
        ),
        (
            Path("grammar5.txt"),
            Path("graph1.dot"),
            {(0, 3), (2, 3)},
            {0, 2},
            {3},
        ),
    ],
)
def test_cfpq(
    cfg_path,
    graph_path,
    expected_cfpq,
    start_nodes,
    final_nodes,
):
    expected_cfpq = set(map(lambda pair: (str(pair[0]), str(pair[1])), expected_cfpq))
    start_nodes = (
        None if start_nodes is None else set(map(lambda v: str(v), start_nodes))
    )
    final_nodes = (
        None if final_nodes is None else set(map(lambda v: str(v), final_nodes))
    )
    cfg = cfg_from_txt(GRAMMAR_PATH / cfg_path)
    graph = networkx.drawing.nx_pydot.read_dot(GRAPH_PATH / graph_path)
    res_cfpq = cfpq(graph, cfg, start_nodes, final_nodes, Variable("S"), "hellings")
    assert res_cfpq == expected_cfpq


def teardown_module(module):
    print("basic teardown module")
