import antlr4
from wasm.model import Module, Func, BinaryOperation, Call, Param, Const
from compiler import compiler


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
                instructions=[
                    Call(
                        var="$output_println",
                        arguments=[
                            BinaryOperation(
                                op="i32.add",
                                left=Const(val_type="i32", val="1"),
                                right=BinaryOperation(
                                    op="i32.mul",
                                    left=Const(val_type="i32", val="2"),
                                    right=Const(val_type="i32", val="3"),
                                ),
                            )
                        ],
                    )
                ],
            ),
        ]
    )
