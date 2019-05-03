import antlr4
from compiler import compiler


def test_simple_expression():
    source = """
        import System::Output;

        export function Main(): void {
            Output.println(value=1 + 2 * 3);
        }
     """
    result = compiler.generate(antlr4.InputStream(source))
    assert (
        result
        == """
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
    )
