import antlr4


def generate(input_stream: antlr4.InputStream) -> str:
    return """
(module
    (func $output_println (import "System::Output" "println") (param i32))

    (func (export "Main")
        (i32.add
            (i32.const 1)
            (i32.mul
                (i32.const 2)
                (i32.const 3))
        )
        call $output_println
    )
)
"""
