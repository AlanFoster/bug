from wasm.model import (
    Module,
    Import,
    Func,
    BinaryOperation,
    Call,
    Param,
    Result,
    Const,
    Local,
    GetLocal,
    SetLocal,
    If,
    Drop,
    Return,
    Nop,
    Memory,
    GetGlobal,
    SetGlobal,
    Global,
    Store,
)
from wasm.printer import pretty_print


def test_simple_expression(snapshot):
    source = Module(
        imports=[
            Import(
                name="$output_println",
                import_=("System::Output", "println"),
                params=[Param("i32")],
            )
        ],
        instructions=[
            Func(
                name="$Main",
                export="Main",
                instructions=[
                    Call(
                        name="$output_println",
                        arguments=[
                            BinaryOperation(
                                op="i32.add",
                                left=Const(type="i32", val="1"),
                                right=BinaryOperation(
                                    op="i32.mul",
                                    left=Const(type="i32", val="2"),
                                    right=Const(type="i32", val="3"),
                                ),
                            )
                        ],
                    )
                ],
            )
        ],
    )
    wasm_result = pretty_print(source)
    snapshot.assert_match(wasm_result)


def test_function_call_with_params_and_locals(snapshot):
    source = Module(
        imports=[
            Import(
                name="$output_println",
                import_=("System::Output", "println"),
                params=[Param("i32")],
            )
        ],
        instructions=[
            Func(
                name="$add",
                params=[Param(type="i32", name="$a"), Param(type="i32", name="$b")],
                result=Result("i32"),
                locals=[Local(type="i32", name="$answer")],
                instructions=[
                    SetLocal(
                        name="$answer",
                        val=BinaryOperation(
                            op="i32.add",
                            left=GetLocal(name="$a"),
                            right=GetLocal(name="$b"),
                        ),
                    ),
                    GetLocal(name="$answer"),
                ],
            ),
            Func(
                name="$Main",
                export="Main",
                locals=[Local(type="i32", name="$a"), Local(type="i32", name="$b")],
                instructions=[
                    SetLocal(name="$a", val=Const(type="i32", val="2")),
                    SetLocal(name="$b", val=Const(type="i32", val="3")),
                    Call(
                        name="$output_println",
                        arguments=[
                            Call(
                                name="$add",
                                arguments=[GetLocal(name="$a"), GetLocal(name="$b")],
                            )
                        ],
                    ),
                ],
            ),
        ],
    )
    wasm_result = pretty_print(source)
    snapshot.assert_match(wasm_result)


def test_conditionals(snapshot):
    source = Module(
        imports=[
            Import(
                name="$output_println",
                import_=("System::Output", "println"),
                params=[Param("i32")],
            )
        ],
        instructions=[
            Func(
                name="$Foo",
                result=Result(type="i32"),
                export=None,
                locals=[],
                instructions=[
                    If(
                        result=None,
                        condition=BinaryOperation(
                            op="i32.lt_s",
                            left=Const(type="i32", val="9"),
                            right=Const(type="i32", val="10"),
                        ),
                        then_statements=[
                            Call(
                                name="$output_println",
                                arguments=[Const(type="i32", val="1")],
                            )
                        ],
                        else_statements=None,
                    ),
                    If(
                        result=Result(type="i32"),
                        condition=BinaryOperation(
                            op="i32.gt_s",
                            left=Const(type="i32", val="9"),
                            right=Const(type="i32", val="10"),
                        ),
                        then_statements=[Const(type="i32", val="1")],
                        else_statements=[Const(type="i32", val="0")],
                    ),
                ],
            ),
            Func(
                name="$Main",
                export="Main",
                locals=[],
                instructions=[Call(name="$Foo", arguments=[]), Drop()],
            ),
        ],
    )
    wasm_result = pretty_print(source)
    snapshot.assert_match(wasm_result)


def test_returns(snapshot):
    source = Module(
        imports=[
            Import(
                name="$output_println",
                import_=("System::Output", "println"),
                params=[Param("i32")],
            )
        ],
        instructions=[
            Func(
                name="$meaning_of_life",
                result=Result(type="i32"),
                export=None,
                locals=[],
                instructions=[Return(expression=Const(type="i32", val="42"))],
            ),
            Func(
                name="$output_meaning_of_life",
                result=None,
                export=None,
                locals=[],
                instructions=[
                    Call(name="$meaning_of_life", arguments=[]),
                    Return(expression=Nop()),
                ],
            ),
            Func(
                name="$Main",
                export="Main",
                locals=[],
                instructions=[Call(name="$output_meaning_of_life", arguments=[])],
            ),
        ],
    )
    wasm_result = pretty_print(source)
    snapshot.assert_match(wasm_result)


def test_memory(snapshot):
    source = Module(
        imports=[],
        instructions=[
            Memory(size=1, export="memory"),
            Func(
                name="$set_memory",
                params=[],
                locals=[],
                result=None,
                instructions=[
                    Store(
                        type="i32",
                        location=Const(type="i32", val="0"),
                        val=Const(type="i32", val="1337"),
                    )
                ],
            ),
        ],
    )
    wasm_result = pretty_print(source)
    snapshot.assert_match(wasm_result)


def test_globals(snapshot):
    source = Module(
        imports=[],
        instructions=[
            Global(name="$count", type="mut i32", value=Const(type="i32", val="0")),
            Func(
                name="$increment_count",
                params=[],
                locals=[],
                result=Result(type="i32"),
                instructions=[
                    SetGlobal(
                        name="$count",
                        val=(
                            BinaryOperation(
                                op="i32.add",
                                left=GetGlobal(name="$count"),
                                right=Const(type="i32", val="1"),
                            )
                        ),
                    ),
                    GetGlobal(name="$count"),
                ],
            ),
        ],
    )

    wasm_result = pretty_print(source)
    snapshot.assert_match(wasm_result)
