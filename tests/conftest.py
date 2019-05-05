from wasm.model import Module
from wasm.printer import pretty_print


def pytest_assertrepr_compare(op, left, right):
    if isinstance(left, Module) and isinstance(right, Module) and op == "==":
        # The pretty printed modules will be more human readable when diffing
        assert pretty_print(left) == pretty_print(right)

        # In this scenario the string representations are equal, but the object equality differs
        return [
            "Module instances pretty print to the same value, but object equality differs:",
            f"Left: {left}",
            f"Right: {right}",
        ]
