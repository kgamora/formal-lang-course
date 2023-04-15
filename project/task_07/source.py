from __future__ import annotations

from typing import AbstractSet
from pyformlang.cfg import CFG, Variable, Terminal
from pyformlang.regular_expression import Regex
from pathlib import Path


class ECFG:
    def __init__(
        self,
        variables: AbstractSet[Variable],
        terminals: AbstractSet[Terminal],
        start_symbol: Variable,
        productions: dict,
    ):
        self.variables = variables
        self.terminals = terminals
        self.start_symbol = start_symbol
        self.productions = productions

    @classmethod
    def from_cfg(cls, cfg: CFG) -> ECFG:
        """
        Constructs ECFG object from given CFG
        :param cfg: context-free grammar to construct ECFG from
        :return: ECFG from given CFG
        """
        productions: dict = {}
        for production in cfg.productions:
            body = Regex(
                " ".join(var.value for var in production.body)
                if len(production.body) > 0
                else ""
            )
            productions[production.head] = (
                productions[production.head].union(body)
                if production.head in productions
                else body
            )
        return cls(
            set(cfg.variables), set(cfg.terminals), cfg.start_symbol, productions
        )

    @classmethod
    def from_file(cls, file: Path) -> ECFG:
        """
        Constructs ECFG from a given file
        :param file: Path to a file with a grammar
        :return: ECFG from given file
        """
        ecfg_string: str

        if not file.exists():
            raise FileNotFoundError(f"{file} not found.")
        elif not file.is_file():
            raise ValueError(f"{file} is not a file.")

        with open(str(file), "r") as source:
            ecfg_string = source.read()
        return cls.from_text(ecfg_string)

    @classmethod
    def from_text(cls, text: str, start_symbol=Variable("S")) -> ECFG:
        """
        Constructs ECFG from text
        :param text: productions (str)
        :param start_symbol: start symbol ("S" by default)
        :return: ECFG
        """
        variables: set
        productions: dict

        variables, productions = (set(), dict())

        for line in text.splitlines():
            line = line.strip()
            if len(line) == 0:
                continue

            production = line.split("->")

            if len(production) != 2:
                raise Exception(f"Error in line: {line}")

            head = Variable(production[0].strip())
            body = Regex(production[1].strip())

            if head in variables:
                raise Exception(f"Error in line: {line}")

            variables.add(head)
            productions[head] = body

        return cls(variables, None, start_symbol, productions)
