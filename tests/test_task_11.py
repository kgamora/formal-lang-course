import pytest
from project.task_11.source import valid


def setup_module(module):
    print("basic setup module")


@pytest.mark.parametrize(
    "program, is_valid",
    [
        ("", bool(0)),
        ('print("Hello World!");', bool(1)),
        ("var = True;", bool(1)),
        ("var = 1;", bool(1)),
        ('var = "string value";', bool(1)),
    ],
)
def test_var_rule(program: str, is_valid: bool):
    assert is_valid == valid(program)


def teardown_module(module):
    print("basic teardown module")
