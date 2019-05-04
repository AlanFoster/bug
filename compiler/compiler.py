import antlr4
from parser.BugLexer import BugLexer
from parser.BugParser import BugParser
from wasm.model import Module
from .visitor import Visitor


def generate(input_stream: antlr4.InputStream) -> Module:
    visitor = Visitor()
    lexer = BugLexer(input_stream)
    tokens = antlr4.CommonTokenStream(lexer)
    parser = BugParser(tokens)
    tree = parser.program()

    return visitor.visit(tree)
