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
