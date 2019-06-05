import antlr4

import compiler.ast as ast
from semantic_analysis.declaration_analysis_vistor import DeclarationAnalysisVisitor
from generator.ast_visitor import AstVisitor as GeneratorAstVisitor
from generator.preamble import with_preamble
from parser.BugLexer import BugLexer
from parser.BugParser import BugParser
from wasm.model import Module
from .parse_tree_visitor import ParseTreeVisitor
from .error_listener import ErrorListener


def get_parse_tree(input_stream: antlr4.InputStream):
    lexer = BugLexer(input_stream)
    tokens = antlr4.CommonTokenStream(lexer)
    parser = BugParser(tokens)
    parser.removeErrorListeners()
    parser.addErrorListener(ErrorListener())
    tree = parser.program()
    return tree


def get_ast(tree: BugParser.program) -> ast.Program:
    visitor = ParseTreeVisitor()
    ast = visitor.visit(tree)

    return ast


def get_semantic_analysis(program: ast.Program) -> ast.Program:
    visitor = DeclarationAnalysisVisitor()
    program_with_types = program.accept(visitor)
    return program_with_types


def get_wasm(program: ast.Program) -> Module:
    visitor = GeneratorAstVisitor()
    wasm = program.accept(visitor)
    return wasm


def generate(input_stream: antlr4.InputStream) -> Module:
    parse_tree = get_parse_tree(input_stream)
    ast = get_ast(parse_tree)
    ast_with_type_information = get_semantic_analysis(ast)
    wasm = get_wasm(ast_with_type_information)
    module = with_preamble(wasm)

    return module
