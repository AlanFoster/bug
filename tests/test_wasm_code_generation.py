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
    If,
    Return,
)
from compiler import compiler


def get_wasm(source: str) -> Module:
    input_stream = antlr4.InputStream(source)
    parse_tree = compiler.get_parse_tree(input_stream)
    ast = compiler.get_ast(parse_tree)
    return compiler.get_wasm(ast)


def test_empty_program():
    source = ""
    result = get_wasm(source)

    assert result == Module([])


def test_simple_expression():
    source = """
        import System::Output;

        export function Main(): void {
            println(value=1 + 2 * 3);
        }
     """
    result = get_wasm(source)

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


def test_if_statement():
    source = """
        import System::Output;

        export function Main(): void {
            if (5 > 10) {
                println(value=1);
            }
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
                    If(
                        condition=BinaryOperation(
                            op="i32.gt_s",
                            left=Const(type="i32", val="5"),
                            right=Const(type="i32", val="10"),
                        ),
                        result=None,
                        then_statements=[
                            Call(
                                name="$output_println",
                                arguments=[Const(type="i32", val="1")],
                            )
                        ],
                        else_statements=None,
                    )
                ],
            ),
        ]
    )


def test_if_else_statement():
    source = """
        import System::Output;

        export function Main(): void {
            if (5 < 10) {
                println(value=1);
            } else {
                println(value=0);
            }
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
                    If(
                        condition=BinaryOperation(
                            op="i32.lt_s",
                            left=Const(type="i32", val="5"),
                            right=Const(type="i32", val="10"),
                        ),
                        result=None,
                        then_statements=[
                            Call(
                                name="$output_println",
                                arguments=[Const(type="i32", val="1")],
                            )
                        ],
                        else_statements=[
                            Call(
                                name="$output_println",
                                arguments=[Const(type="i32", val="0")],
                            )
                        ],
                    )
                ],
            ),
        ]
    )


def test_factorial():
    # TODO: The precedence in this example is wrong. Additional parentheses provided for now.
    source = """
        import System::Output;

        function factorial(n: i32): i32 {
            if (n == 1) {
                return 1;
            } else {
                return n * (factorial(n=n-1));
            }
        }

        export function Main(): void {
            println(value=factorial(n=5));
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
                name="$factorial",
                export=None,
                params=[Param(type="i32", name="$n")],
                locals=[],
                result=Result(type="i32"),
                instructions=[
                    If(
                        condition=BinaryOperation(
                            op="i32.eq",
                            left=GetLocal(name="$n"),
                            right=Const(type="i32", val="1"),
                        ),
                        result=None,
                        then_statements=[Return(expression=Const(type="i32", val="1"))],
                        else_statements=[
                            Return(
                                expression=(
                                    BinaryOperation(
                                        op="i32.mul",
                                        left=GetLocal(name="$n"),
                                        right=(
                                            Call(
                                                name="$factorial",
                                                arguments=[
                                                    BinaryOperation(
                                                        op="i32.sub",
                                                        left=GetLocal(name="$n"),
                                                        right=Const(
                                                            type="i32", val="1"
                                                        ),
                                                    )
                                                ],
                                            )
                                        ),
                                    )
                                )
                            )
                        ],
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
                                name="$factorial",
                                arguments=[Const(type="i32", val="5")],
                            )
                        ],
                    )
                ],
            ),
        ]
    )
