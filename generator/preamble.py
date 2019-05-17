from typing import List

from wasm.model import (
    Module,
    Func,
    Memory,
    Global,
    GetGlobal,
    GetLocal,
    SetGlobal,
    Instruction,
    BinaryOperation,
    Const,
    Param,
    Result,
)


def preamble() -> List[Instruction]:
    """
    :return: the list of instructions required to bootstrap the
    system, i.e. initializing memory, specifying the heap pointer
    address, and providing the fundamental building blocks of
    memory management.
    """
    allocate_memory = Memory(size=1, export="memory")
    heap_pointer = Global(
        name="$heap_pointer", type="mut i32", value=Const(type="i32", val="12")
    )
    self_pointer = Global(
        name="$self_pointer", type="mut i32", value=Const(type="i32", val="0")
    )

    # Simple bump allocator, functionally equivalent to:
    # export function malloc(required_bytes: i32): i32 {
    #   let location = heap_pointer
    #   heap_pointer += 4 * required_bytes
    #   return location
    # }
    malloc = Func(
        name="$malloc",
        params=[Param(type="i32", name="$required_bytes")],
        locals=[],
        result=Result(type="i32"),
        instructions=[
            GetGlobal(name="$heap_pointer"),
            SetGlobal(
                name="$heap_pointer",
                val=(
                    BinaryOperation(
                        op="i32.add",
                        left=(
                            BinaryOperation(
                                op="i32.mul",
                                left=(Const(type="i32", val="4")),
                                right=GetGlobal(name="$heap_pointer"),
                            )
                        ),
                        right=GetLocal(name="$required_bytes"),
                    )
                ),
            ),
        ],
    )

    return [allocate_memory, heap_pointer, self_pointer, malloc]


def with_preamble(module: Module) -> Module:
    module.instructions = preamble() + module.instructions
    return module
