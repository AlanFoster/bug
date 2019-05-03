import antlr4
from parser.BugLexer import BugLexer
from parser.BugParser import BugParser
from .visitor import Visitor


def generate(input_stream: antlr4.InputStream) -> str:
    visitor = Visitor()
    lexer = BugLexer(input_stream)
    tokens = antlr4.CommonTokenStream(lexer)
    parser = BugParser(tokens)
    tree = parser.program()

    return visitor.visit(tree)
