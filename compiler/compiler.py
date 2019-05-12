import antlr4

import compiler.ast as ast
from generator.ast_visitor import AstVisitor
from generator.preamble import with_preamble
from parser.BugLexer import BugLexer
from parser.BugParser import BugParser
from wasm.model import Module
from .parse_tree_visitor import ParseTreeVisitor


def get_parse_tree(input_stream: antlr4.InputStream):
    lexer = BugLexer(input_stream)
    tokens = antlr4.CommonTokenStream(lexer)
    parser = BugParser(tokens)
    tree = parser.program()
    return tree


def get_ast(tree: BugParser.program) -> ast.Program:
    visitor = ParseTreeVisitor()
    ast = visitor.visit(tree)

    return ast


def get_wasm(program: ast.Program) -> Module:
    visitor = AstVisitor()
    wasm = program.accept(visitor)
    return wasm


def generate(input_stream: antlr4.InputStream) -> Module:
    parse_tree = get_parse_tree(input_stream)
    ast = get_ast(parse_tree)
    wasm = get_wasm(ast)
    module = with_preamble(wasm)

    return module
