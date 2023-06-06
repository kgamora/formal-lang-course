import pytest
from project.task_11.source import valid


def setup_module(module):
    print("basic setup module")


@pytest.mark.parametrize(
    "program, is_valid",
    [
        ("var = True;\nvar = False;", bool(1)),
        ("var = 1;", bool(1)),
        ('var = "string value";', bool(1)),
    ],
)
def test_var_rule(program: str, is_valid: bool):
    assert is_valid == valid(program)


@pytest.mark.parametrize(
    "program, is_valid",
    [
        ('a = 1;\nb = 2;\nedge_label = "edge label";\ne = (a,edge_label,b);', bool(1)),
        ('e2 = ( 1, "my_little_label", 7);', bool(1)),
    ],
)
def test_edge_rule(program: str, is_valid: bool):
    assert is_valid == valid(program)


@pytest.mark.parametrize(
    "program, is_valid",
    [('my_mapped = map(lambda a, b, c -> "Hello World!", "expression");', bool(1))],
)
def test_lambda_map_rule(program: str, is_valid: bool):
    assert is_valid == valid(program)


@pytest.mark.parametrize(
    "program, is_valid",
    [('my_mapped = filter(lambda a, b, c -> "Hello World!", "expression");', bool(1))],
)
def test_lambda_filter_rule(program: str, is_valid: bool):
    assert is_valid == valid(program)


@pytest.mark.parametrize(
    "program, is_valid",
    [
        ("a = {};", bool(1)),
        ("a = {a, 1};", bool(1)),
        ("a = {a, a};", bool(1)),
        ("a = {1, 1};", bool(1)),
        ("a = {a, 1, True};", bool(0)),
    ],
)
def test_simple_vertices_rule(program: str, is_valid: bool):
    assert is_valid == valid(program)


@pytest.mark.parametrize(
    "program, is_valid",
    [
        ("a = {};", bool(1)),
        ("a = {a, 1};", bool(1)),
        ('a = {a, "a"};', bool(1)),
        ('a = {a, 1, "a"};', bool(1)),
        ("a = {a, 1, True};", bool(0)),
    ],
)
def test_simple_labels_rule(program: str, is_valid: bool):
    assert is_valid == valid(program)


@pytest.mark.parametrize(
    "program, is_valid",
    [
        ('a = load_graph("my_simple_graph.txt");', bool(1)),
        ('a = set_start({0, 1},load_graph("my_simple_graph.txt"));', bool(1)),
        (
            'a = set_final({2, 3},set_start({},load_graph("my_simple_graph.txt")));',
            bool(1),
        ),
        (
            'a = add_start({a, 2}, set_final({2, 3},set_start({},load_graph("my_simple_graph.txt"))));',
            bool(1),
        ),
        (
            'a = add_final({b, c}, add_start({}, set_final({2, 3},set_start({},load_graph("my_simple_graph.txt")))));',
            bool(1),
        ),
        (
            'a = add_final(add_start({}, set_final({2, 3},set_start({},load_graph("my_simple_graph.txt")))));',
            bool(0),
        ),
        ("a = load_graph(True);", bool(0)),
    ],
)
def test_graph_rule(program: str, is_valid: bool):
    assert is_valid == valid(program)


@pytest.mark.parametrize(
    "program, is_valid",
    [
        ('a = ( load_graph("my_simple_graph.txt") == "Hello graph!" );', bool(1)),
        ('a = load_graph("my_simple_graph.txt") == "Hello graph!";', bool(0)),
    ],
)
def test_equals_rule(program: str, is_valid: bool):
    assert is_valid == valid(program)


@pytest.mark.parametrize(
    "program, is_valid",
    [
        ("a = intersect(a, a);", bool(1)),
        ("a = unite(a, a);", bool(1)),
        ("a = concat(a, a);", bool(1)),
        ("a = star(a);", bool(1)),
    ],
)
def test_intersect_concat_unite_star(program: str, is_valid: bool):
    assert is_valid == valid(program)


@pytest.mark.parametrize(
    "program, is_valid",
    [
        ("", bool(1)),
        ('print("Hello World!");', bool(1)),
    ],
)
def test_simplest_exprx(program: str, is_valid: bool):
    assert is_valid == valid(program)


def teardown_module(module):
    print("basic teardown module")
