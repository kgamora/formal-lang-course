import os.path
import random
import pytest
import project  # on import will print something from __init__ file
from project.source import *


def setup_module(module):
    print("basic setup module")


def teardown_module(module):
    print("basic teardown module")


def test_graph_info_by_name():
    graph_info = get_graph_info_by_name("skos")
    assert graph_info["node_count"] == 144
    assert graph_info["edge_count"] == 252
    assert graph_info["edge_labels"][0][0] == 't'
    assert graph_info["edge_labels"][0][1] == 'y'


def test_save_double_cycle_dot():
    graph_info = get_graph_info_by_name("skos")
    file_name = "some_name.dot"
    make_double_cycled_graph_and_save_into_dot(random.randint(100, 200), random.randint(100, 200),
                                               graph_info["edge_labels"],
                                               file_name)
    assert os.path.exists(file_name)
