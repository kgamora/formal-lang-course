from pyformlang.cfg import CFG, Production
from pathlib import Path


def to_wcnf(grammar: CFG) -> CFG:
    """
    Takes grammar and transforms it into Weak Chomsky Normal Form.
    Code is somewhat equivalent to "to_normal_form" from cfg package
    of pyformlang.
    :param grammar: grammar to transform
    :return: grammar transformed into Weak Chomsky Normal Form
    """
    new_grammar: CFG
    new_productions: list[Production]

    new_grammar = (
        grammar.remove_useless_symbols()
        .eliminate_unit_productions()
        .remove_useless_symbols()
    )

    new_productions = new_grammar._get_productions_with_only_single_terminals()
    new_productions = new_grammar._decompose_productions(new_productions)
    return CFG(start_symbol=new_grammar.start_symbol, productions=set(new_productions))


def cfg_from_txt(file: Path) -> CFG:
    """
    Read a context free grammar from a file.
    The text contains one rule per line.
    The structure of a production is:
    head -> body1 | body2 | ... | bodyn
    where | separates the bodies.
    A variable (or non terminal) begins by a capital letter.
    A terminal begins by a non-capital character
    Terminals and Variables are separated by spaces.
    An epsilon symbol can be represented by epsilon, $, ε, ϵ or Є.
    If you want to have a variable name starting with a non-capital \
    letter or a terminal starting with a capital letter, you can \
    explicitly give the type of your symbol with "VAR:yourVariableName" \
    or "TER:yourTerminalName" (with the quotation marks). For example:
    S -> "TER:John" "VAR:d" a b
    :param file: Path
        The file with text of transform
    :return: cfg : :class:`~pyformlang.cfg.CFG`
        A context free grammar.
    """
    if not file.exists():
        raise FileNotFoundError(f"{file} not found.")
    elif not file.is_file():
        raise ValueError(f"{file} is not a file.")

    with open(str(file), "r") as source:
        cfg_text = source.read()

    return CFG.from_text(cfg_text)
