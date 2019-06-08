import pytest
from prettyprinter import pformat

from compiler.ast import Program
from wasm.model import Module
from wasm.printer import pretty_print
from generator.preamble import with_preamble
from wasm.wat_to_wasm import wat_to_wasm, WatToWasmException


def assert_valid_wat(wat: str):
    try:
        wat_to_wasm(wat)
    except WatToWasmException as e:
        pytest.fail(f"Invalid wasm:\n{e}")


def assert_valid_module(module: Module):
    wat = pretty_print(module)
    assert_valid_wat(wat)


def assert_equal_modules(actual: Module, expected: Module):
    assert pretty_print(actual) == pretty_print(
        expected
    ), "The given module instances do not pretty print to the same string"
    assert (
        actual == expected
    ), "The given module instances pretty print to the same value, but object equality differs"
    assert_valid_module(with_preamble(actual))


def assert_equal_programs(actual: Program, expected: Program):
    assert pformat(actual) == pformat(
        expected
    ), "The given program instances do not pretty print to the same string"
    assert (
        actual == expected
    ), "The given program instances pretty print to the same value, but object equality differs"
