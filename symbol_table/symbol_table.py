from abc import abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Optional

from symbol_table.type import Type


class SymbolKind(Enum):
    LOCAL = 1
    PARAM = 2
    FUNC = 3
    DATA = 4
    DATA_FIELD = 5


@dataclass
class Symbol:
    name: str
    type: Type
    kind: SymbolKind
    field_number: Optional[int] = None

    @property
    def generated_name(self):
        if self.kind is SymbolKind.DATA:
            return f"${self.name}.new"

        return f"${self.name}"


class SymbolTable:
    @abstractmethod
    def add(self, symbol: Symbol):
        raise NotImplementedError()

    @abstractmethod
    def get(self, name: str) -> Symbol:
        raise NotImplementedError()

    @abstractmethod
    def has(self, name: str) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def enter_scope(self) -> "SymbolTable":
        raise NotImplementedError()

    @abstractmethod
    def exit_scope(self) -> "SymbolTable":
        raise NotImplementedError()

    @abstractmethod
    def tree(self, depth: int = 0) -> str:
        raise NotImplementedError()


class EmptySymbolTable(SymbolTable):
    def add(self, symbol: Symbol):
        raise NotImplementedError()

    def get(self, name: str) -> Symbol:
        raise ValueError(f"Missing variable '{name}'.")

    def has(self, name: str) -> bool:
        return False

    def enter_scope(self) -> SymbolTable:
        return ChildSymbolTable(self)

    def exit_scope(self) -> SymbolTable:
        raise NotImplementedError()

    def tree(self, depth: int = 0) -> str:
        return "[Empty]"


@dataclass
class ChildSymbolTable(SymbolTable):
    parent: Optional[SymbolTable]
    symbols: Dict[str, Symbol] = field(default_factory=dict)

    def add(self, symbol: Symbol):
        if symbol.name in self.symbols:
            raise ValueError(f"Duplicate variable {symbol.name} found.")
        self.symbols[symbol.name] = symbol

    def get(self, name: str) -> Symbol:
        if name in self.symbols:
            return self.symbols[name]

        return self.parent.get(name)

    def has(self, name: str) -> bool:
        if name in self.symbols:
            return True

        return self.parent.has(name)

    def enter_scope(self) -> SymbolTable:
        return ChildSymbolTable(self)

    def exit_scope(self) -> SymbolTable:
        return self.parent

    def locals(self):
        return [v for k, v in self.symbols.items() if v.kind is SymbolKind.LOCAL]

    def tree(self, depth: int = 0) -> str:
        symbols = ", ".join(
            [f"({symbol.name}: {symbol.type})" for _key, symbol in self.symbols.items()]
        )
        return f"[{symbols}]" + "\n->" + self.parent.tree(depth + 1)
