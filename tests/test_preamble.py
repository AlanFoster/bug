from generator.preamble import preamble
from wasm.model import Module
from wasm.printer import pretty_print


def test_preamble(snapshot):
    wasm_result = pretty_print(Module(imports=[], instructions=preamble()))
    snapshot.assert_match(wasm_result)
