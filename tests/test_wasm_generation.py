from wasm.generate import generate
from wasm.model import Module, Func, BinaryOperation, Call, Param, Const


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
    wasm_result = generate(source)
    snapshot.assert_match(wasm_result)
