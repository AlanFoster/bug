import antlr4
from wasm.model import Module, Func, BinaryOperation, Call, Param, Const


def generate(input_stream: antlr4.InputStream) -> str:
    return Module(
        [
            Func(
                name="$output_println",
                import_=("System::Output", "println"),
                params=[Param("i32")],
            ),
            Func(
                export="Main",
                instructions=[
                    BinaryOperation(
                        op="i32.add",
                        left=[Const(val_type="i32", val="1")],
                        right=[
                            BinaryOperation(
                                op="i32.mul",
                                left=[Const(val_type="i32", val="2")],
                                right=[Const(val_type="i32", val="3")],
                            )
                        ],
                    ),
                    Call(var="$output_println"),
                ],
            ),
        ]
    )
