"""
Tests for ensuring that the compiler works end to end, rather than testing
an individual layer in isolation.
"""
import antlr4
from compiler.compiler import generate
from tests.helpers.wasm import assert_valid_wat
from wasm.printer import pretty_print


def compile(source: str):
    input_stream = antlr4.InputStream(source)
    return pretty_print(generate(input_stream))


def test_simple_expression(snapshot):
    source = """
        import System::Output;

        export function Main(): void {
            println(value=1 + 2 * 3);
        }
     """
    result = compile(source)
    assert_valid_wat(result)
    snapshot.assert_match(result)


def test_data_vector_with_complex_function(snapshot):
    source = """
        import System::Output;

        export data Vector(x: i32, y: i32) {
            function add(self: Vector, other: Vector): Vector {
                Vector(
                    x = self.x + other.x,
                    y = self.y + other.y
                );
            }

            function getX(self: Vector): i32 {
                self.x;
            }

            function getY(self: Vector): i32 {
                self.y;
            }
        }

        export function Main(): void {
            let vectorA = Vector(x=3, y=6);
            let vectorB = Vector(x=5, y=3);
            let vectorC = vectorA.add(other=vectorB);
            println(value=vectorC.getX());
            println(value=vectorC.getY());
        }
    """
    result = compile(source)
    assert_valid_wat(result)
    snapshot.assert_match(result)
