from wasm.model import (
    Module,
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
    Condition,
    Drop,
)
from wasm.printer import pretty_print


def test_simple_expression(snapshot):
    source = Module(
        [
            Func(
                name="$output_println",
                import_=("System::Output", "println"),
                params=[Param("i32")],
            ),
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
            ),
        ]
    )
    wasm_result = pretty_print(source)
    snapshot.assert_match(wasm_result)


def test_function_call_with_params_and_locals(snapshot):
    source = Module(
        [
            Func(
                name="$output_println",
                import_=("System::Output", "println"),
                params=[Param("i32")],
            ),
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
        ]
    )
    wasm_result = pretty_print(source)
    snapshot.assert_match(wasm_result)


def test_conditionals(snapshot):
    source = Module(
        [
            Func(
                name="$output_println",
                import_=("System::Output", "println"),
                params=[Param("i32")],
            ),
            Func(
                name="$Foo",
                result=Result(type="i32"),
                export=None,
                locals=[],
                instructions=[
                    If(
                        result=None,
                        condition=Condition(
                            op="i32.lt_s",
                            left=Const(type="i32", val="9"),
                            right=Const(type="i32", val="10"),
                        ),
                        then=[
                            Call(
                                name="$output_println",
                                arguments=[Const(type="i32", val="1")],
                            )
                        ],
                        else_=None,
                    ),
                    If(
                        result=Result(type="i32"),
                        condition=Condition(
                            op="i32.gt_s",
                            left=Const(type="i32", val="9"),
                            right=Const(type="i32", val="10"),
                        ),
                        then=[Const(type="i32", val="1")],
                        else_=[Const(type="i32", val="0")],
                    ),
                ],
            ),
            Func(
                name="$Main",
                export="Main",
                locals=[],
                instructions=[Call(name="$Foo", arguments=[]), Drop()],
            ),
        ]
    )
    wasm_result = pretty_print(source)
    snapshot.assert_match(wasm_result)
