import antlr4
from pathlib import Path
from dataclasses import dataclass
from compiler import compiler
from typing import List, Any
from wasm.printer import pretty_print
import sys

from wasm.wat_to_wasm import wat_to_wasm


@dataclass(frozen=True)
class CompileTarget:
    file: Path

    @property
    def wat_path(self):
        return self.file.with_suffix(".wat")

    @property
    def wasm_path(self):
        return self.file.with_suffix(".wasm")


@dataclass(frozen=True)
class Configuration:
    targets: List[CompileTarget]


def parse_argv(argv: List[Any]) -> Configuration:
    input_path = Path(argv[1]).absolute()
    files = [input_path] if input_path.is_file() else list(input_path.glob("*.bug"))
    targets = []
    for path in files:
        targets.append(CompileTarget(file=path))

    return Configuration(targets=targets)


def main(argv: List[Any]) -> None:
    configuration = parse_argv(argv)

    for target in configuration.targets:
        input_stream = antlr4.FileStream(str(target.file))
        result = compiler.generate(input_stream)
        wat = pretty_print(result)

        with target.wat_path.open(mode="w") as file:
            file.write(wat)

        with target.wasm_path.open(mode="wb") as file:
            file.write(wat_to_wasm(wat))


if __name__ == "__main__":
    main(sys.argv)
