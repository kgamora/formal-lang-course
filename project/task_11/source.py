from graphQL.graphQLParser import graphQLParser
from graphQL.graphQLLexer import graphQLLexer
from graphQL.graphQLListener import graphQLListener
from antlr4 import CommonTokenStream, InputStream, ParserRuleContext
from antlr4.tree.Tree import ParseTreeWalker, TerminalNodeImpl
from pathlib import Path
from pydot import Dot, Edge, Node


def parser(text: str) -> graphQLParser:
    return graphQLParser(CommonTokenStream(graphQLLexer(InputStream(text))))


def valid(text: str) -> bool:
    lang_parser = parser(text)
    lang_parser.removeParseListeners()
    lang_parser.program()
    return lang_parser.getNumberOfSyntaxErrors() == 0


def save_parse_tree_to_dot(text: str, path: Path | str):
    if not valid(text):
        raise ValueError("Text does not belong to the language.")
    lang_parser = parser(text)
    listener = TreeGraphQLListener()
    ParseTreeWalker().walk(listener, lang_parser.program())
    listener.dot.write(path)


class TreeGraphQLListener(graphQLListener):
    def __int__(self):
        self.dot = Dot("tree", graph_type="digraph")
        self.num_nodes = 0
        self.nodes = dict()
        self.ruleNames = graphQLParser.ruleNames
        super(TreeGraphQLListener, self).__init__()

    def enterEveryRule(self, context: ParserRuleContext):
        if context not in self.nodes:
            self.num_nodes += 1
            self.nodes[context] = self.num_nodes
        if context.parentCtx:
            self.dot.add_edge(Edge(self.nodes[context.parentCtx], self.nodes[context]))
        label = self.ruleNames[context.getRuleIndex()]
        self.dot.add_node(Node(self.nodes[context], label=label))

    def visitTerminal(self, node: TerminalNodeImpl):
        self.num_nodes += 1
        self.dot.add_edge(Edge(self.nodes[node.parentCtx], self.num_nodes))
        self.dot.add_node(Node(self.num_nodes, label=f"{node.getText()}"))
