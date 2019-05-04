import antlr4
from wasm.model import (
    Module,
    Func,
    BinaryOperation,
    Call,
    Param,
    Const,
    Local,
    SetLocal,
    GetLocal,
    Result,
)
from compiler import compiler
from wasm.printer import pretty_print


def test_simple_expression():
    source = """
        import System::Output;

        export function Main(): void {
            println(value=1 + 2 * 3);
        }
     """
    result = compiler.generate(antlr4.InputStream(source))

    assert result == Module(
        [
            Func(
                name="$output_println",
                import_=("System::Output", "println"),
                params=[Param("i32")],
            ),
            Func(
                name="$Main",
                export="Main",
                params=[],
                locals=[],
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


def test_simple_assignment():
    source = """
        import System::Output;

        export function Main(): void {
            let a = 5;
            let b = 10;
            println(value=a + b);
        }
     """
    result = compiler.generate(antlr4.InputStream(source))

    assert result == Module(
        [
            Func(
                name="$output_println",
                import_=("System::Output", "println"),
                params=[Param("i32")],
            ),
            Func(
                name="$Main",
                export="Main",
                params=[],
                locals=[Local(type="i32", name="$a"), Local(type="i32", name="$b")],
                instructions=[
                    SetLocal(name="$a", val=Const(type="i32", val="5")),
                    SetLocal(name="$b", val=Const(type="i32", val="10")),
                    Call(
                        name="$output_println",
                        arguments=[
                            BinaryOperation(
                                op="i32.add",
                                left=GetLocal(name="$a"),
                                right=GetLocal(name="$b"),
                            )
                        ],
                    ),
                ],
            ),
        ]
    )


def test_function_call_with_no_arguments():
    source = """
        import System::Output;

        function sayNumber(): void {
            println(value=1337);
        }

        export function Main(): void {
            sayNumber();
        }
     """
    result = compiler.generate(antlr4.InputStream(source))

    assert result == Module(
        [
            Func(
                name="$output_println",
                import_=("System::Output", "println"),
                params=[Param("i32")],
            ),
            Func(
                name="$sayNumber",
                params=[],
                locals=[],
                result=None,
                instructions=[
                    Call(
                        name="$output_println",
                        arguments=[Const(type="i32", val="1337")],
                    )
                ],
            ),
            Func(
                name="$Main",
                export="Main",
                params=[],
                locals=[],
                instructions=[Call(name="$sayNumber", arguments=[])],
            ),
        ]
    )


def test_function_call_with_arguments():
    source = """
        import System::Output;

        function add(x: i32, y: i32): i32 {
            x + y;
        }

        export function Main(): void {
            println(value=add(a=5, b=15));
        }
     """
    result = compiler.generate(antlr4.InputStream(source))

    assert result == Module(
        [
            Func(
                name="$output_println",
                import_=("System::Output", "println"),
                params=[Param("i32")],
            ),
            Func(
                name="$add",
                params=[Param(type="i32", name="$x"), Param(type="i32", name="$y")],
                locals=[],
                result=Result(type="i32"),
                instructions=[
                    BinaryOperation(
                        op="i32.add",
                        left=GetLocal(name="$x"),
                        right=GetLocal(name="$y"),
                    )
                ],
            ),
            Func(
                name="$Main",
                export="Main",
                params=[],
                locals=[],
                instructions=[
                    Call(
                        name="$output_println",
                        arguments=[
                            Call(
                                name="$add",
                                arguments=[
                                    Const(type="i32", val="5"),
                                    Const(type="i32", val="15"),
                                ],
                            )
                        ],
                    )
                ],
            ),
        ]
    )
