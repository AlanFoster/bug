import subprocess
import tempfile

import pytest
from prettyprinter import pformat

from compiler.ast import Program
from wasm.model import Module
from wasm.printer import pretty_print
from generator.preamble import with_preamble


def assert_valid_wat(wat: str):
    with tempfile.NamedTemporaryFile(delete=True) as tmp:
        tmp.write(bytes(wat, encoding="utf8"))
        tmp.flush()
        try:
            # TODO: wabt can be called with ffi
            subprocess.run(
                ["wat2wasm", tmp.name, "--output", "/dev/null"],
                check=True,
                capture_output=True,
                universal_newlines=True,
            )
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Invalid wasm:\n{e.stderr}")


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
