import cfpq_data
import networkx


def get_graph_info_by_name(name: str) -> dict:
    """
    По имени графа вернуть количество вершин, рёбер и перечислить различные метки, встречающиеся на рёбрах.
    :param name: имя графа
    :return: словарь, содержащий ключи node_count, edge_count и edge_labels
    """
    graph_path = cfpq_data.download(name=name)
    graph = cfpq_data.graph_from_csv(graph_path)

    return {
        "node_count": graph.number_of_nodes(),
        "edge_count": graph.number_of_edges(),
        "edge_labels": cfpq_data.get_sorted_labels(graph),
    }


def make_double_cycled_graph_and_save_into_dot(
    number_of_nodes_first_cycle: int,
    number_of_nodes_second_cycle: int,
    labels: tuple,
    file_name: str,
):
    graph = cfpq_data.graphs.generators.labeled_two_cycles_graph(
        number_of_nodes_first_cycle, number_of_nodes_second_cycle, labels=labels
    )
    """
    По количеству вершин в циклах и именам меток строить граф из двух циклов и сохранять его в указанный файл в
    формате DOT (использовать pydot).
    :param number_of_nodes_first_cycle: кол-во вершин в первом цикле
    :param number_of_nodes_second_cycle: кол-во вершин во втором цикле
    :param edge_labels: метки
    :param путь для сохранения DOT-файла
    :return: None
    """
    graph_dot = networkx.drawing.nx_pydot.to_pydot(graph)
    with open(file_name, "w"):
        graph_dot.write(file_name)
