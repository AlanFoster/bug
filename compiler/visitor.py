from compiler.symbol_table import EmptySymbolTable, Symbol, SymbolType
from parser.BugParser import BugParser
from parser.BugParserVisitor import BugParserVisitor
from wasm.model import (
    Module,
    Func,
    BinaryOperation,
    Call,
    Param,
    Const,
    SetLocal,
    GetLocal,
    Local,
    Result,
    If,
    Nop,
    Return,
)


def get_binary_operator(op):
    if op.type == BugParser.ADD:
        return "i32.add"
    elif op.type == BugParser.MUL:
        return "i32.mul"
    elif op.type == BugParser.GT:
        return "i32.gt_s"
    elif op.type == BugParser.LT:
        return "i32.lt_s"
    elif op.type == BugParser.EQEQ:
        return "i32.eq"
    elif op.type == BugParser.SUB:
        return "i32.sub"
    else:
        raise NotImplementedError(f"Binary operator '{op.text}' not implemented.")


class Visitor(BugParserVisitor):
    def __init__(self):
        self.symbol_table: EmptySymbolTable = EmptySymbolTable()

    # Visit a parse tree produced by BugParser#program.
    def visitProgram(self, ctx: BugParser.ProgramContext):
        self.symbol_table = self.symbol_table.enter_scope()

        imports = self.visit(ctx.importStatements())

        functions = []
        for function in ctx.functionDef():
            functions.append(self.visit(function))

        instructions = []
        instructions += imports
        instructions += functions
        self.symbol_table = self.symbol_table.exit_scope()
        return Module(instructions=instructions)

    # Visit a parse tree produced by BugParser#importStatements.
    def visitImportStatements(self, ctx: BugParser.ImportStatementsContext):
        statements = [
            self.visit(import_statement) for import_statement in ctx.importStatement()
        ]
        return statements

    # Visit a parse tree produced by BugParser#importStatement.
    def visitImportStatement(self, ctx: BugParser.ImportStatementContext):
        if ctx.getText() != "importSystem::Output;":
            raise NotImplementedError(
                f"Import statement '${ctx.getText()}' not yet supported."
            )

        return Func(
            name="$output_println",
            import_=("System::Output", "println"),
            params=[Param("i32")],
        )

    # Visit a parse tree produced by BugParser#functionDef.
    def visitFunctionDef(self, ctx: BugParser.FunctionDefContext):
        # Place the current function into the symbol table so that it can be called by
        # other functions later, or recursively if required.
        function_name = ctx.functionName().getText()
        return_type = ctx.returnTypeName().getText()
        function_symbol = Symbol(
            name=function_name, type=return_type, kind=SymbolType.FUNC
        )
        self.symbol_table.add(function_symbol)

        self.symbol_table = self.symbol_table.enter_scope()

        # Populate the required params into the symbol table before compiling the function body
        params = []
        if ctx.parameterList():
            for param in ctx.parameterList().params:
                var_name = param.variableName().getText()
                type_ = param.typeName().getText()
                symbol = Symbol(name=var_name, type=type_, kind=SymbolType.PARAM)
                self.symbol_table.add(symbol)
                params.append(Param(type=symbol.type, name=symbol.generated_name))
        body = self.visit(ctx.functionBody())

        # Note, locals will be populated after visiting the function body
        locals_ = []
        for symbol in self.symbol_table.locals():
            locals_.append(Local(type=symbol.type, name=symbol.generated_name))
        self.symbol_table = self.symbol_table.exit_scope()

        return Func(
            # Note: The function name is the internally generated name for this module
            name=function_symbol.generated_name,
            # Note: The export name is the original function name
            export=function_name if ctx.EXPORT() else None,
            params=params,
            result=None if return_type == "void" else Result(type=return_type),
            locals=locals_,
            instructions=body,
        )

    # Visit a parse tree produced by BugParser#data.
    def visitData(self, ctx: BugParser.DataContext):
        raise NotImplementedError()

    # Visit a parse tree produced by BugParser#dataName.
    def visitDataName(self, ctx: BugParser.DataNameContext):
        raise NotImplementedError()

    # Visit a parse tree produced by BugParser#dataList.
    def visitDataList(self, ctx: BugParser.DataListContext):
        raise NotImplementedError()

    # Visit a parse tree produced by BugParser#functionBody.
    def visitFunctionBody(self, ctx: BugParser.FunctionBodyContext):
        statements = self.visit(ctx.statements())
        return statements

    # Visit a parse tree produced by BugParser#statements.
    def visitStatements(self, ctx: BugParser.StatementsContext):
        statements = [self.visit(statement) for statement in ctx.statement()]
        return statements

    # Visit a parse tree produced by BugParser#statement.
    def visitStatement(self, ctx: BugParser.StatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by BugParser#returnStatement.
    def visitReturnStatement(self, ctx: BugParser.ReturnStatementContext):
        return Return(
            expression=self.visit(ctx.expression()) if ctx.expression() else Nop()
        )

    # Visit a parse tree produced by BugParser#statementExpression.
    def visitStatementExpression(self, ctx: BugParser.StatementExpressionContext):
        return self.visit(ctx.expression())

    # Visit a parse tree produced by BugParser#forLoop.
    def visitForLoop(self, ctx: BugParser.ForLoopContext):
        raise NotImplementedError()

    # Visit a parse tree produced by BugParser#ifStatement.
    def visitIfStatement(self, ctx: BugParser.IfStatementContext):
        condition = self.visit(ctx.condition)
        then_statements = self.visit(ctx.then_statements)
        else_statements = (
            self.visit(ctx.else_statements) if ctx.else_statements else None
        )
        return If(
            condition=condition,
            # TODO: The result type will have to be inferred correctly
            result=Result(type="i32"),
            then_statements=then_statements,
            else_statements=else_statements,
        )

    # Visit a parse tree produced by BugParser#letStatement.
    def visitLetStatement(self, ctx: BugParser.LetStatementContext):
        expression = self.visit(ctx.expression())
        varable_name = ctx.variableName().getText()
        # TODO: Assignments should infer the expression type / support explicit types: `let a: i32 = expression;`
        type_ = "i32"
        symbol = Symbol(name=varable_name, type=type_, kind=SymbolType.LOCAL)
        self.symbol_table.add(symbol)

        return SetLocal(name=symbol.generated_name, val=expression)

    # Visit a parse tree produced by BugParser#returnTypeName.
    def visitReturnTypeName(self, ctx: BugParser.ReturnTypeNameContext):
        raise NotImplementedError()

    # Visit a parse tree produced by BugParser#parameterList.
    def visitParameterList(self, ctx: BugParser.ParameterListContext):
        raise NotImplementedError()

    # Visit a parse tree produced by BugParser#typedVariable.
    def visitTypedVariable(self, ctx: BugParser.TypedVariableContext):
        raise NotImplementedError()

    # Visit a parse tree produced by BugParser#functionName.
    def visitFunctionName(self, ctx: BugParser.FunctionNameContext):
        raise NotImplementedError()

    # Visit a parse tree produced by BugParser#variableName.
    def visitVariableName(self, ctx: BugParser.VariableNameContext):
        raise NotImplementedError()

    # Visit a parse tree produced by BugParser#binaryExpression.
    def visitBinaryExpression(self, ctx: BugParser.BinaryExpressionContext):
        operation = get_binary_operator(ctx.operator)
        left = self.visit(ctx.left)
        right = self.visit(ctx.right)

        return BinaryOperation(op=operation, left=left, right=right)

    # Visit a parse tree produced by BugParser#callExpression.
    def visitCallExpression(self, ctx: BugParser.CallExpressionContext):
        function_name = ctx.expression().getText()
        # Note: This will need to use a real symbol table in the future
        if function_name == "println":
            function_name = "$output_println"
        elif self.symbol_table.has(function_name):
            symbol = self.symbol_table.get(function_name)
            if symbol.kind is not SymbolType.FUNC:
                raise NotImplementedError(f"{function_name} is not a function")

            function_name = symbol.generated_name
        else:
            raise NotImplementedError(f"{function_name} not supported")
        arguments = self.visit(ctx.argumentList()) if ctx.argumentList() else []
        return Call(name=function_name, arguments=arguments)

    # Visit a parse tree produced by BugParser#variableNameExpression.
    def visitVariableNameExpression(self, ctx: BugParser.VariableNameExpressionContext):
        variable_name = ctx.variableName().getText()
        symbol = self.symbol_table.get(variable_name)

        return GetLocal(name=symbol.generated_name)

    # Visit a parse tree produced by BugParser#nestedExpression.
    def visitNestedExpression(self, ctx: BugParser.NestedExpressionContext):
        return self.visit(ctx.expression())

    # Visit a parse tree produced by BugParser#unaryExpression.
    def visitUnaryExpression(self, ctx: BugParser.UnaryExpressionContext):
        raise NotImplementedError()

    # Visit a parse tree produced by BugParser#literalExpression.
    def visitLiteralExpression(self, ctx: BugParser.LiteralExpressionContext):
        return self.visit(ctx.literal())

    # Visit a parse tree produced by BugParser#literal.
    def visitLiteral(self, ctx: BugParser.LiteralContext):
        if ctx.INTEGER():
            return Const(type="i32", val=ctx.INTEGER().getText())
        else:
            raise NotImplementedError(f"literal {ctx.getText()} not implemented")

    # Visit a parse tree produced by BugParser#string.
    def visitString(self, ctx: BugParser.StringContext):
        raise NotImplementedError()

    # Visit a parse tree produced by BugParser#stringPart.
    def visitStringPart(self, ctx: BugParser.StringPartContext):
        raise NotImplementedError()

    # Visit a parse tree produced by BugParser#argumentList.
    def visitArgumentList(self, ctx: BugParser.ArgumentListContext):
        arguments = [self.visit(argument) for argument in ctx.argument()]
        return arguments

    # Visit a parse tree produced by BugParser#argument.
    def visitArgument(self, ctx: BugParser.ArgumentContext):
        # Note: In the future, these variable names will map to the correct argument order
        _variable_name = ctx.variableName().getText()
        expression = self.visit(ctx.expression())

        return expression

    # Visit a parse tree produced by BugParser#typeName.
    def visitTypeName(self, ctx: BugParser.TypeNameContext):
        raise NotImplementedError()
