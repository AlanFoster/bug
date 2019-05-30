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
    Import,
    SetGlobal,
    GetGlobal,
    Store,
    Load,
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

    assert result == Module(imports=[], instructions=[])


def test_simple_expression():
    source = """
        import System::Output;

        export function Main(): void {
            println(value=1 + 2 * 3);
        }
     """
    result = get_wasm(source)

    assert result == Module(
        imports=[
            Import(
                name="$output_println",
                import_=("System::Output", "println"),
                params=[Param(type="i32", name=None)],
                result=None,
            )
        ],
        instructions=[
            Func(
                name="$Main",
                export="Main",
                params=[],
                locals=[],
                result=None,
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
            )
        ],
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
    result = get_wasm(source)

    assert result == Module(
        imports=[
            Import(
                name="$output_println",
                import_=("System::Output", "println"),
                params=[Param(type="i32", name=None)],
                result=None,
            )
        ],
        instructions=[
            Func(
                name="$Main",
                export="Main",
                params=[],
                locals=[Local(type="i32", name="$a"), Local(type="i32", name="$b")],
                result=None,
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
            )
        ],
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
    result = get_wasm(source)

    assert result == Module(
        imports=[
            Import(
                name="$output_println",
                import_=("System::Output", "println"),
                params=[Param(type="i32", name=None)],
                result=None,
            )
        ],
        instructions=[
            Func(
                name="$sayNumber",
                params=[],
                locals=[],
                result=None,
                export=None,
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
                result=None,
                instructions=[Call(name="$sayNumber", arguments=[])],
            ),
        ],
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
    result = get_wasm(source)

    assert result == Module(
        imports=[
            Import(
                name="$output_println",
                import_=("System::Output", "println"),
                params=[Param(type="i32", name=None)],
                result=None,
            )
        ],
        instructions=[
            Func(
                name="$add",
                params=[Param(type="i32", name="$x"), Param(type="i32", name="$y")],
                locals=[],
                result=Result(type="i32"),
                export=None,
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
                result=None,
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
        ],
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
    result = get_wasm(source)

    assert result == Module(
        imports=[
            Import(
                name="$output_println",
                import_=("System::Output", "println"),
                params=[Param(type="i32", name=None)],
                result=None,
            )
        ],
        instructions=[
            Func(
                name="$Main",
                export="Main",
                params=[],
                locals=[],
                result=None,
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
            )
        ],
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
    result = get_wasm(source)

    assert result == Module(
        imports=[
            Import(
                name="$output_println",
                import_=("System::Output", "println"),
                params=[Param(type="i32", name=None)],
                result=None,
            )
        ],
        instructions=[
            Func(
                name="$Main",
                export="Main",
                params=[],
                locals=[],
                result=None,
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
            )
        ],
    )


def test_factorial():
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
    result = get_wasm(source)

    assert result == Module(
        imports=[
            Import(
                name="$output_println",
                import_=("System::Output", "println"),
                params=[Param(type="i32", name=None)],
                result=None,
            )
        ],
        instructions=[
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
                result=None,
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
        ],
    )


def test_data_vector():
    source = """
        import System::Output;

        export data Vector(x: i32, y: i32)

        export function Main(): void {

        }
     """
    result = get_wasm(source)

    assert result == Module(
        imports=[
            Import(
                name="$output_println",
                import_=("System::Output", "println"),
                params=[Param(type="i32", name=None)],
                result=None,
            )
        ],
        instructions=[
            Func(
                name="$Vector.new",
                export=None,
                params=[Param(type="i32", name="$x"), Param(type="i32", name="$y")],
                result=Result(type="i32"),
                locals=[],
                instructions=[
                    SetGlobal(
                        name="$self_pointer",
                        val=Call(
                            name="$malloc", arguments=[Const(type="i32", val="2")]
                        ),
                    ),
                    Store(
                        type="i32",
                        location=BinaryOperation(
                            op="i32.add",
                            left=GetGlobal(name="$self_pointer"),
                            right=Const(type="i32", val="0"),
                        ),
                        val=GetLocal(name="$x"),
                    ),
                    Store(
                        type="i32",
                        location=BinaryOperation(
                            op="i32.add",
                            left=GetGlobal(name="$self_pointer"),
                            right=Const(type="i32", val="4"),
                        ),
                        val=GetLocal(name="$y"),
                    ),
                    GetGlobal(name="$self_pointer"),
                ],
            ),
            Func(
                name="$Main",
                export="Main",
                params=[],
                result=None,
                locals=[],
                instructions=[],
            ),
        ],
    )


def test_data_vector_constructor():
    source = """
        import System::Output;

        data Vector(x: i32, y: i32)

        export function Main(): void {
            let vector = Vector(x=10, y=20);
        }
     """
    result = get_wasm(source)

    assert result == Module(
        imports=[
            Import(
                name="$output_println",
                import_=("System::Output", "println"),
                params=[Param(type="i32", name=None)],
                result=None,
            )
        ],
        instructions=[
            Func(
                name="$Vector.new",
                export=None,
                locals=[],
                params=[Param(type="i32", name="$x"), Param(type="i32", name="$y")],
                result=Result(type="i32"),
                instructions=[
                    SetGlobal(
                        name="$self_pointer",
                        val=Call(
                            name="$malloc", arguments=[Const(type="i32", val="2")]
                        ),
                    ),
                    Store(
                        type="i32",
                        location=(
                            BinaryOperation(
                                op="i32.add",
                                left=GetGlobal(name="$self_pointer"),
                                right=Const(type="i32", val="0"),
                            )
                        ),
                        val=GetLocal(name="$x"),
                    ),
                    Store(
                        type="i32",
                        location=(
                            BinaryOperation(
                                op="i32.add",
                                left=GetGlobal(name="$self_pointer"),
                                right=Const(type="i32", val="4"),
                            )
                        ),
                        val=GetLocal(name="$y"),
                    ),
                    GetGlobal(name="$self_pointer"),
                ],
            ),
            Func(
                name="$Main",
                export="Main",
                result=None,
                params=[],
                locals=[Local(type="i32", name="$vector")],
                instructions=[
                    SetLocal(
                        name="$vector",
                        val=Call(
                            name="$Vector.new",
                            arguments=[
                                Const(type="i32", val="10"),
                                Const(type="i32", val="20"),
                            ],
                        ),
                    )
                ],
            ),
        ],
    )


def test_data_vector_with_simple_function():
    source = """
        import System::Output;

        export data Vector(x: i32, y: i32) {
            function length(self: Vector): i32 {
                42;
            }
        }

        export function Main(): void {

        }
     """
    result = get_wasm(source)

    assert result == Module(
        imports=[
            Import(
                name="$output_println",
                import_=("System::Output", "println"),
                params=[Param(type="i32", name=None)],
                result=None,
            )
        ],
        instructions=[
            Func(
                name="$Vector.new",
                export=None,
                params=[Param(type="i32", name="$x"), Param(type="i32", name="$y")],
                result=Result(type="i32"),
                locals=[],
                instructions=[
                    SetGlobal(
                        name="$self_pointer",
                        val=Call(
                            name="$malloc", arguments=[Const(type="i32", val="2")]
                        ),
                    ),
                    Store(
                        type="i32",
                        location=(
                            BinaryOperation(
                                op="i32.add",
                                left=GetGlobal(name="$self_pointer"),
                                right=Const(type="i32", val="0"),
                            )
                        ),
                        val=GetLocal(name="$x"),
                    ),
                    Store(
                        type="i32",
                        location=(
                            BinaryOperation(
                                op="i32.add",
                                left=GetGlobal(name="$self_pointer"),
                                right=Const(type="i32", val="4"),
                            )
                        ),
                        val=GetLocal(name="$y"),
                    ),
                    GetGlobal(name="$self_pointer"),
                ],
            ),
            Func(
                name="$Vector.length",
                export=None,
                params=[Param(type="i32", name="$self")],
                result=Result(type="i32"),
                locals=[],
                instructions=[Const(type="i32", val="42")],
            ),
            Func(
                name="$Main",
                export="Main",
                params=[],
                locals=[],
                result=None,
                instructions=[],
            ),
        ],
    )


def test_data_vector_with_simple_function_call():
    source = """
        import System::Output;

        export data Vector(x: i32, y: i32) {
            function length(self: Vector): i32 {
                42;
            }
        }

        export function Main(): void {
            let vector = Vector(x=10, y=20);
            println(value=vector.length());
        }
     """
    result = get_wasm(source)

    assert result == Module(
        imports=[
            Import(
                name="$output_println",
                import_=("System::Output", "println"),
                params=[Param(type="i32", name=None)],
                result=None,
            )
        ],
        instructions=[
            Func(
                name="$Vector.new",
                export=None,
                params=[Param(type="i32", name="$x"), Param(type="i32", name="$y")],
                result=Result(type="i32"),
                locals=[],
                instructions=[
                    SetGlobal(
                        name="$self_pointer",
                        val=Call(
                            name="$malloc", arguments=[Const(type="i32", val="2")]
                        ),
                    ),
                    Store(
                        type="i32",
                        location=(
                            BinaryOperation(
                                op="i32.add",
                                left=GetGlobal(name="$self_pointer"),
                                right=Const(type="i32", val="0"),
                            )
                        ),
                        val=GetLocal(name="$x"),
                    ),
                    Store(
                        type="i32",
                        location=(
                            BinaryOperation(
                                op="i32.add",
                                left=GetGlobal(name="$self_pointer"),
                                right=Const(type="i32", val="4"),
                            )
                        ),
                        val=GetLocal(name="$y"),
                    ),
                    GetGlobal(name="$self_pointer"),
                ],
            ),
            Func(
                name="$Vector.length",
                export=None,
                params=[Param(type="i32", name="$self")],
                result=Result(type="i32"),
                locals=[],
                instructions=[Const(type="i32", val="42")],
            ),
            Func(
                name="$Main",
                export="Main",
                params=[],
                locals=[Local(type="i32", name="$vector")],
                result=None,
                instructions=[
                    SetLocal(
                        name="$vector",
                        val=Call(
                            name="$Vector.new",
                            arguments=[
                                Const(type="i32", val="10"),
                                Const(type="i32", val="20"),
                            ],
                        ),
                    ),
                    Call(
                        name="$output_println",
                        arguments=[
                            Call(
                                name="$Vector.length",
                                arguments=[GetLocal(name="$vector")],
                            )
                        ],
                    ),
                ],
            ),
        ],
    )


def test_data_vector_with_self_getter_method():
    source = """
        import System::Output;

        export data Vector(x: i32, y: i32) {
            function getX(self: Vector): i32 {
                self.x;
            }
        }

        export function Main(): void {
            let vector = Vector(x=10, y=20);
            println(value=vector.getX());
        }
     """
    result = get_wasm(source)

    assert result == Module(
        imports=[
            Import(
                name="$output_println",
                import_=("System::Output", "println"),
                params=[Param(type="i32", name=None)],
                result=None,
            )
        ],
        instructions=[
            Func(
                name="$Vector.new",
                export=None,
                params=[Param(type="i32", name="$x"), Param(type="i32", name="$y")],
                result=Result(type="i32"),
                locals=[],
                instructions=[
                    SetGlobal(
                        name="$self_pointer",
                        val=Call(
                            name="$malloc", arguments=[Const(type="i32", val="2")]
                        ),
                    ),
                    Store(
                        type="i32",
                        location=(
                            BinaryOperation(
                                op="i32.add",
                                left=GetGlobal(name="$self_pointer"),
                                right=Const(type="i32", val="0"),
                            )
                        ),
                        val=GetLocal(name="$x"),
                    ),
                    Store(
                        type="i32",
                        location=(
                            BinaryOperation(
                                op="i32.add",
                                left=GetGlobal(name="$self_pointer"),
                                right=Const(type="i32", val="4"),
                            )
                        ),
                        val=GetLocal(name="$y"),
                    ),
                    GetGlobal(name="$self_pointer"),
                ],
            ),
            Func(
                name="$Vector.getX",
                export=None,
                params=[Param(type="i32", name="$self")],
                result=Result(type="i32"),
                locals=[],
                instructions=[
                    Load(
                        type="i32",
                        location=BinaryOperation(
                            op="i32.add",
                            left=GetLocal("$self"),
                            right=BinaryOperation(
                                op="i32.mul",
                                left=Const(type="i32", val="0"),
                                right=Const(type="i32", val="4"),
                            ),
                        ),
                    )
                ],
            ),
            Func(
                name="$Main",
                export="Main",
                params=[],
                locals=[Local(name="$vector", type="i32")],
                result=None,
                instructions=[
                    SetLocal(
                        name="$vector",
                        val=Call(
                            name="$Vector.new",
                            arguments=[
                                Const(type="i32", val="10"),
                                Const(type="i32", val="20"),
                            ],
                        ),
                    ),
                    Call(
                        name="$output_println",
                        arguments=[
                            Call(
                                name="$Vector.getX",
                                arguments=[GetLocal(name="$vector")],
                            )
                        ],
                    ),
                ],
            ),
        ],
    )


def test_data_vector_with_self_getter_methods():
    source = """
        import System::Output;

        export data Vector(x: i32, y: i32) {
            function getX(self: Vector): i32 {
                self.x;
            }

            function getY(self: Vector): i32 {
                self.y;
            }
        }

        export function Main(): void {
            let vector = Vector(x=10, y=20);
            println(value=vector.getX());
            println(value=vector.getY());
        }
     """
    result = get_wasm(source)

    assert result == Module(
        imports=[
            Import(
                name="$output_println",
                import_=("System::Output", "println"),
                params=[Param(type="i32", name=None)],
                result=None,
            )
        ],
        instructions=[
            Func(
                name="$Vector.new",
                export=None,
                params=[Param(type="i32", name="$x"), Param(type="i32", name="$y")],
                result=Result(type="i32"),
                locals=[],
                instructions=[
                    SetGlobal(
                        name="$self_pointer",
                        val=Call(
                            name="$malloc", arguments=[Const(type="i32", val="2")]
                        ),
                    ),
                    Store(
                        type="i32",
                        location=(
                            BinaryOperation(
                                op="i32.add",
                                left=GetGlobal(name="$self_pointer"),
                                right=Const(type="i32", val="0"),
                            )
                        ),
                        val=GetLocal(name="$x"),
                    ),
                    Store(
                        type="i32",
                        location=(
                            BinaryOperation(
                                op="i32.add",
                                left=GetGlobal(name="$self_pointer"),
                                right=Const(type="i32", val="4"),
                            )
                        ),
                        val=GetLocal(name="$y"),
                    ),
                    GetGlobal(name="$self_pointer"),
                ],
            ),
            Func(
                name="$Vector.getX",
                export=None,
                params=[Param(type="i32", name="$self")],
                result=Result(type="i32"),
                locals=[],
                instructions=[
                    Load(
                        type="i32",
                        location=BinaryOperation(
                            op="i32.add",
                            left=GetLocal("$self"),
                            right=BinaryOperation(
                                op="i32.mul",
                                left=Const(type="i32", val="0"),
                                right=Const(type="i32", val="4"),
                            ),
                        ),
                    )
                ],
            ),
            Func(
                name="$Vector.getY",
                export=None,
                params=[Param(type="i32", name="$self")],
                result=Result(type="i32"),
                locals=[],
                instructions=[
                    Load(
                        type="i32",
                        location=BinaryOperation(
                            op="i32.add",
                            left=GetLocal("$self"),
                            right=BinaryOperation(
                                op="i32.mul",
                                left=Const(type="i32", val="1"),
                                right=Const(type="i32", val="4"),
                            ),
                        ),
                    )
                ],
            ),
            Func(
                name="$Main",
                export="Main",
                params=[],
                locals=[Local(name="$vector", type="i32")],
                result=None,
                instructions=[
                    SetLocal(
                        name="$vector",
                        val=Call(
                            name="$Vector.new",
                            arguments=[
                                Const(type="i32", val="10"),
                                Const(type="i32", val="20"),
                            ],
                        ),
                    ),
                    Call(
                        name="$output_println",
                        arguments=[
                            Call(
                                name="$Vector.getX",
                                arguments=[GetLocal(name="$vector")],
                            )
                        ],
                    ),
                    Call(
                        name="$output_println",
                        arguments=[
                            Call(
                                name="$Vector.getY",
                                arguments=[GetLocal(name="$vector")],
                            )
                        ],
                    ),
                ],
            ),
        ],
    )


def test_data_vector_with_math():
    source = """
        import System::Output;

        export data Vector(x: i32, y: i32) {
            function getDoubleY(self: Vector): i32 {
                self.y + self.y;
            }
        }

        export function Main(): void {
            let vector = Vector(x=10, y=20);
            println(value=vector.getX());
            println(value=vector.getY());
        }
     """
    result = get_wasm(source)

    assert result == Module(
        imports=[
            Import(
                name="$output_println",
                import_=("System::Output", "println"),
                params=[Param(type="i32", name=None)],
                result=None,
            )
        ],
        instructions=[
            Func(
                name="$Vector.new",
                export=None,
                params=[Param(type="i32", name="$x"), Param(type="i32", name="$y")],
                result=Result(type="i32"),
                locals=[],
                instructions=[
                    SetGlobal(
                        name="$self_pointer",
                        val=Call(
                            name="$malloc", arguments=[Const(type="i32", val="2")]
                        ),
                    ),
                    Store(
                        type="i32",
                        location=(
                            BinaryOperation(
                                op="i32.add",
                                left=GetGlobal(name="$self_pointer"),
                                right=Const(type="i32", val="0"),
                            )
                        ),
                        val=GetLocal(name="$x"),
                    ),
                    Store(
                        type="i32",
                        location=(
                            BinaryOperation(
                                op="i32.add",
                                left=GetGlobal(name="$self_pointer"),
                                right=Const(type="i32", val="4"),
                            )
                        ),
                        val=GetLocal(name="$y"),
                    ),
                    GetGlobal(name="$self_pointer"),
                ],
            ),
            Func(
                name="$Vector.getDoubleY",
                export=None,
                params=[Param(type="i32", name="$self")],
                result=Result(type="i32"),
                locals=[],
                instructions=[
                    BinaryOperation(
                        op="i32.add",
                        left=Load(
                            type="i32",
                            location=BinaryOperation(
                                op="i32.add",
                                left=GetLocal("$self"),
                                right=BinaryOperation(
                                    op="i32.mul",
                                    left=Const(type="i32", val="1"),
                                    right=Const(type="i32", val="4"),
                                ),
                            ),
                        ),
                        right=Load(
                            type="i32",
                            location=BinaryOperation(
                                op="i32.add",
                                left=GetLocal("$self"),
                                right=BinaryOperation(
                                    op="i32.mul",
                                    left=Const(type="i32", val="1"),
                                    right=Const(type="i32", val="4"),
                                ),
                            ),
                        ),
                    )
                ],
            ),
            Func(
                name="$Main",
                export="Main",
                params=[],
                locals=[Local(name="$vector", type="i32")],
                result=None,
                instructions=[
                    SetLocal(
                        name="$vector",
                        val=Call(
                            name="$Vector.new",
                            arguments=[
                                Const(type="i32", val="10"),
                                Const(type="i32", val="20"),
                            ],
                        ),
                    ),
                    Call(
                        name="$output_println",
                        arguments=[
                            Call(
                                name="$Vector.getX",
                                arguments=[GetLocal(name="$vector")],
                            )
                        ],
                    ),
                    Call(
                        name="$output_println",
                        arguments=[
                            Call(
                                name="$Vector.getY",
                                arguments=[GetLocal(name="$vector")],
                            )
                        ],
                    ),
                ],
            ),
        ],
    )
