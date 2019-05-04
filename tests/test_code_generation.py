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
                export="Main",
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
                export="Main",
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
