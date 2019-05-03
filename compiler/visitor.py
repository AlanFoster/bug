from parser.BugParser import BugParser
from parser.BugParserVisitor import BugParserVisitor
from wasm.model import Module, Func, BinaryOperation, Call, Param, Const


def get_binary_operator(op):
    if op.type == BugParser.ADD:
        return "i32.add"
    elif op.type == BugParser.MUL:
        return "i32.mul"
    else:
        raise NotImplementedError(f"Binary operator '{op}' not implemented.")


class Visitor(BugParserVisitor):

    # Visit a parse tree produced by BugParser#program.
    def visitProgram(self, ctx: BugParser.ProgramContext):
        imports = self.visit(ctx.importStatements())
        functions = [self.visit(function) for function in ctx.functionDef()]

        instructions = []
        instructions += imports
        instructions += functions
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
        body = self.visit(ctx.functionBody())

        return Func(
            export=ctx.functionName().getText() if ctx.EXPORT() else None,
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

    # Visit a parse tree produced by BugParser#forLoop.
    def visitForLoop(self, ctx: BugParser.ForLoopContext):
        raise NotImplementedError()

    # Visit a parse tree produced by BugParser#letStatement.
    def visitLetStatement(self, ctx: BugParser.LetStatementContext):
        raise NotImplementedError()

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
        else:
            raise NotImplementedError(f"{function_name} not supported")
        arguments = self.visit(ctx.argumentList())
        return Call(var=function_name, arguments=arguments)

    # Visit a parse tree produced by BugParser#variableNameExpression.
    def visitVariableNameExpression(self, ctx: BugParser.VariableNameExpressionContext):
        raise NotImplementedError()

    # Visit a parse tree produced by BugParser#nestedExpression.
    def visitNestedExpression(self, ctx: BugParser.NestedExpressionContext):
        raise NotImplementedError()

    # Visit a parse tree produced by BugParser#unaryExpression.
    def visitUnaryExpression(self, ctx: BugParser.UnaryExpressionContext):
        raise NotImplementedError()

    # Visit a parse tree produced by BugParser#literalExpression.
    def visitLiteralExpression(self, ctx: BugParser.LiteralExpressionContext):
        return self.visit(ctx.literal())

    # Visit a parse tree produced by BugParser#literal.
    def visitLiteral(self, ctx: BugParser.LiteralContext):
        if ctx.INTEGER():
            return Const(val_type="i32", val=ctx.INTEGER().getText())
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
