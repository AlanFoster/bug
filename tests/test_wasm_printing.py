from tests.helpers.wasm import assert_valid_wat
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
    LocalGet,
    LocalSet,
    If,
    Drop,
    Return,
    Nop,
    Memory,
    GlobalGet,
    GlobalSet,
    Global,
    Store,
    Load,
)
from wasm.printer import pretty_print


def test_simple_expression(snapshot):
    source = Module(
        imports=[
            Import(
                name="$output_println",
                import_=("System::Output", "println"),
                params=[Param(type="i32", name=None)],
                result=Result(type=None),
            )
        ],
        instructions=[
            Func(
                name="$Main",
                export="Main",
                locals=[],
                params=[],
                result=Result(type=None),
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
    result = pretty_print(source)
    assert_valid_wat(result)
    snapshot.assert_match(result)


def test_function_call_with_params_and_locals(snapshot):
    source = Module(
        imports=[
            Import(
                name="$output_println",
                import_=("System::Output", "println"),
                params=[Param(type="i32", name=None)],
                result=Result(type=None),
            )
        ],
        instructions=[
            Func(
                name="$add",
                params=[Param(type="i32", name="$a"), Param(type="i32", name="$b")],
                result=Result("i32"),
                locals=[Local(type="i32", name="$answer")],
                export=None,
                instructions=[
                    LocalSet(
                        name="$answer",
                        val=BinaryOperation(
                            op="i32.add",
                            left=LocalGet(name="$a"),
                            right=LocalGet(name="$b"),
                        ),
                    ),
                    LocalGet(name="$answer"),
                ],
            ),
            Func(
                name="$Main",
                export="Main",
                params=[],
                locals=[Local(type="i32", name="$a"), Local(type="i32", name="$b")],
                result=Result(type=None),
                instructions=[
                    LocalSet(name="$a", val=Const(type="i32", val="2")),
                    LocalSet(name="$b", val=Const(type="i32", val="3")),
                    Call(
                        name="$output_println",
                        arguments=[
                            Call(
                                name="$add",
                                arguments=[LocalGet(name="$a"), LocalGet(name="$b")],
                            )
                        ],
                    ),
                ],
            ),
        ],
    )
    result = pretty_print(source)
    assert_valid_wat(result)
    snapshot.assert_match(result)


def test_conditionals(snapshot):
    source = Module(
        imports=[
            Import(
                name="$output_println",
                import_=("System::Output", "println"),
                params=[Param(type="i32", name=None)],
                result=Result(type=None),
            )
        ],
        instructions=[
            Func(
                name="$Foo",
                result=Result(type="i32"),
                export=None,
                params=[],
                locals=[],
                instructions=[
                    If(
                        result=Result(type=None),
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
                params=[],
                locals=[],
                result=Result(type=None),
                instructions=[Call(name="$Foo", arguments=[]), Drop()],
            ),
        ],
    )
    result = pretty_print(source)
    assert_valid_wat(result)
    snapshot.assert_match(result)


def test_returns(snapshot):
    source = Module(
        imports=[
            Import(
                name="$output_println",
                import_=("System::Output", "println"),
                params=[Param(type="i32", name=None)],
                result=Result(type=None),
            )
        ],
        instructions=[
            Func(
                name="$meaning_of_life",
                result=Result(type="i32"),
                export=None,
                locals=[],
                params=[],
                instructions=[Return(expression=Const(type="i32", val="42"))],
            ),
            Func(
                name="$output_meaning_of_life",
                result=Result(type=None),
                export=None,
                locals=[],
                params=[],
                instructions=[
                    Call(name="$meaning_of_life", arguments=[]),
                    Return(expression=Nop()),
                ],
            ),
            Func(
                name="$Main",
                export="Main",
                locals=[],
                params=[],
                result=Result(type=None),
                instructions=[Call(name="$output_meaning_of_life", arguments=[])],
            ),
        ],
    )
    result = pretty_print(source)
    assert_valid_wat(result)
    snapshot.assert_match(result)


def test_memory(snapshot):
    source = Module(
        imports=[],
        instructions=[
            Memory(size=1, export="memory"),
            Func(
                name="$set_memory",
                params=[],
                locals=[],
                result=Result(type="i32"),
                export=None,
                instructions=[
                    Store(
                        type="i32",
                        location=Const(type="i32", val="0"),
                        val=Const(type="i32", val="1337"),
                    ),
                    Load(type="i32", location=Const(type="i32", val="0")),
                ],
            ),
        ],
    )
    result = pretty_print(source)
    assert_valid_wat(result)
    snapshot.assert_match(result)


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
                export=None,
                instructions=[
                    GlobalSet(
                        name="$count",
                        val=(
                            BinaryOperation(
                                op="i32.add",
                                left=GlobalGet(name="$count"),
                                right=Const(type="i32", val="1"),
                            )
                        ),
                    ),
                    GlobalGet(name="$count"),
                ],
            ),
        ],
    )

    result = pretty_print(source)
    assert_valid_wat(result)
    snapshot.assert_match(result)
