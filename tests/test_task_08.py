import pytest
from project.task_08.source import *
from project.task_06.source import *

GRAMMAR_PATH = Path(".") / Path("test_grammars")


def setup_module(module):
    print("basic setup module")


def teardown_module(module):
    print("basic teardown module")


@pytest.mark.parametrize(
    "cfg_path, graph_edges, expected_cfpq, start_nodes, final_nodes",
    [
        (
            Path("grammar5.txt"),
            [
                (0, 1, {"label": "a"}),
                (1, 2, {"label": "a"}),
                (2, 0, {"label": "a"}),
                (2, 3, {"label": "b"}),
                (3, 2, {"label": "b"}),
            ],
            {(1, 2), (0, 3), (2, 3), (0, 2), (2, 2), (1, 3)},
            None,
            None,
        ),
        (
            "grammar5.txt",
            [
                (0, 1, {"label": "a"}),
                (1, 2, {"label": "a"}),
                (2, 0, {"label": "a"}),
                (2, 3, {"label": "b"}),
                (3, 2, {"label": "b"}),
            ],
            {(0, 3), (2, 3)},
            {0, 2},
            {3},
        ),
    ],
)
def test_cfpq(
    cfg_path,
    graph_edges,
    expected_cfpq,
    start_nodes,
    final_nodes,
):
    cfg = cfg_from_txt(GRAMMAR_PATH / cfg_path)
    graph = MultiDiGraph()
    graph.add_edges_from(graph_edges)
    res_cfpq = cfpq(graph, cfg, start_nodes, final_nodes)
    assert res_cfpq == expected_cfpq
