from pyformlang.cfg import CFG, Production


def cyk(cfg: CFG, string: str) -> bool:
    """
    Tests whether given string is derivable in a given cfg
    :param cfg: context-free grammar
    :param string: string to check
    :return: bool - whether given string is derivable from given cfg
    """
    single: list[Production]
    binary: list[Production]
    matrix: list[list[set[str]]]
    string_length: int

    string_length = len(string)

    if not cfg.is_normal_form():
        cfg = cfg.to_normal_form()

    if not string:
        return cfg.generate_epsilon()

    binary, single = list(), list()

    for prod in cfg.productions:
        if len(prod.body) == 1:
            single.append(prod)
        elif len(prod.body) == 2:
            binary.append(prod)

    matrix = [[set(str()) for _ in range(string_length)] for _ in range(string_length)]

    for i in range(string_length):
        matrix[i][i].update(
            prod.head.value for prod in single if string[i] == prod.body[0].value
        )

    for i in range(1, string_length):
        for j in range(string_length - i):
            k = j + i
            for z in range(j, k):
                for prod in binary:
                    if (
                        prod.body[0].value in matrix[j][z]
                        and prod.body[1].value in matrix[z + 1][k]
                    ):
                        matrix[j][k].update({prod.head.value})

    return cfg.start_symbol.value in matrix[0][string_length - 1]
