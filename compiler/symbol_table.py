from abc import abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Optional


@dataclass
class SymbolType(Enum):
    LOCAL = 1


@dataclass
class Symbol:
    name: str
    type: str
    kind: SymbolType

    @property
    def generated_name(self):
        return f"${self.name}"


class SymbolTable:
    @abstractmethod
    def add(self, symbol: Symbol):
        raise NotImplementedError()

    @abstractmethod
    def get(self, name: str):
        raise NotImplementedError()

    @abstractmethod
    def enter_scope(self):
        raise NotImplementedError()

    @abstractmethod
    def exit_scope(self):
        raise NotImplementedError()


class EmptySymbolTable(SymbolTable):
    def add(self, symbol: Symbol):
        raise NotImplementedError()

    def get(self, name):
        raise ValueError(f"Missing variable '{name}'.")

    def enter_scope(self):
        return ChildSymbolTable(self)

    def exit_scope(self):
        raise NotImplementedError()


@dataclass
class ChildSymbolTable(SymbolTable):
    parent: Optional[SymbolTable]
    symbols: Dict[str, Symbol] = field(default_factory=dict)

    def add(self, symbol: Symbol):
        if symbol.name in self.symbols:
            raise ValueError(f"Duplicate variable {symbol.name} found.")
        self.symbols[symbol.name] = symbol

    def get(self, name: str):
        if name in self.symbols:
            return self.symbols[name]

        return self.parent.get(name)

    def enter_scope(self):
        return ChildSymbolTable(self)

    def exit_scope(self):
        return self.parent

    def locals(self):
        return [v for k, v in self.symbols.items() if v.kind is SymbolType.LOCAL]
