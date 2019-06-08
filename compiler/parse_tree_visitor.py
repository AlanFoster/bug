from parser.BugParser import BugParser
from parser.BugParserVisitor import BugParserVisitor
from symbol_table import types
from .ast import (
    Program,
    If,
    Function,
    BinaryOperator,
    BinaryOperation,
    FunctionCall,
    Argument,
    Param,
    Import,
    Number,
    Variable,
    Let,
    Return,
    DataDef,
    MemberAccess,
    Trait,
)


def get_binary_operator(op):
    if op.type == BugParser.ADD:
        return BinaryOperator.ADD
    elif op.type == BugParser.MUL:
        return BinaryOperator.MULTIPLY
    elif op.type == BugParser.GT:
        return BinaryOperator.GREATER_THAN
    elif op.type == BugParser.LT:
        return BinaryOperator.LESS_THAN
    elif op.type == BugParser.EQEQ:
        return BinaryOperator.EQUALS
    elif op.type == BugParser.SUB:
        return BinaryOperator.SUBTRACT
    else:
        raise NotImplementedError(f"Binary operator '{op.text}' not implemented.")


class ParseTreeVisitor(BugParserVisitor):
    def __init__(self):
        pass

    # Visit a parse tree produced by BugParser#program.
    def visitProgram(self, ctx: BugParser.ProgramContext):
        imports = self.visit(ctx.importStatements())
        functions = []
        for function in ctx.functionDef():
            functions.append(self.visit(function))
        data_defs = []
        for data in ctx.data():
            data_defs.append(self.visit(data))
        traits = []
        for trait in ctx.trait():
            traits.append(self.visit(trait))

        return Program(
            imports=imports, traits=traits, functions=functions, data_defs=data_defs
        )

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

        return Import(value="System::Output")

    # Visit a parse tree produced by BugParser#functionDef.
    def visitFunctionDef(self, ctx: BugParser.FunctionDefContext):
        function_name = ctx.functionName().getText()
        return_type = ctx.returnTypeName().getText()

        params = []
        if ctx.parameterList():
            for param in ctx.parameterList().params:
                var_name = param.variableName().getText()
                type_ = param.typeName().getText()
                params.append(Param(type=types.Placeholder(type_), name=var_name))
        body = self.visit(ctx.functionBody())

        return Function(
            # Note: The function name is the internally generated name for this module
            name=function_name,
            is_exported=ctx.EXPORT() is not None,
            params=params,
            type=types.Placeholder(text=return_type),
            body=body,
        )

    # Visit a parse tree produced by BugParser#trait.
    def visitTrait(self, ctx: BugParser.TraitContext):
        name = ctx.traitName().getText()

        functions = []
        for function in ctx.traitFunctionDef():
            functions.append(self.visit(function))

        return Trait(
            name=name,
            is_exported=False,
            functions=functions,
            type=types.Placeholder(text=name),
        )

    # Visit a parse tree produced by BugParser#traitName.
    def visitTraitName(self, ctx: BugParser.TraitNameContext):
        raise NotImplementedError()

    # Visit a parse tree produced by BugParser#traitFunctionDef.
    def visitTraitFunctionDef(self, ctx: BugParser.TraitFunctionDefContext):
        function_name = ctx.traitFunctionName().getText()
        return_type = ctx.returnTypeName().getText()

        params = []
        if ctx.parameterList():
            for param in ctx.parameterList().params:
                var_name = param.variableName().getText()
                type_ = param.typeName().getText()
                params.append(Param(type=types.Placeholder(type_), name=var_name))

        return Function(
            name=function_name,
            is_exported=False,
            params=params,
            type=types.Placeholder(text=return_type),
            body=None,
        )

    # Visit a parse tree produced by BugParser#traitFunctionName.
    def visitTraitFunctionName(self, ctx: BugParser.TraitFunctionNameContext):
        raise NotImplementedError()

    # Visit a parse tree produced by BugParser#data.
    def visitData(self, ctx: BugParser.DataContext):
        params = []
        if ctx.dataList():
            for param in ctx.dataList().params:
                var_name = param.variableName().getText()
                type_ = param.typeName().getText()
                params.append(Param(type=types.Placeholder(type_), name=var_name))
        functions = []
        if ctx.functionDef():
            for function in ctx.functionDef():
                functions.append(self.visit(function))

        implements = []
        if ctx.traitName():
            implements.append(ctx.traitName().getText())

        name = ctx.dataName().getText()
        return DataDef(
            name=name,
            implements=implements,
            type=types.Placeholder(text=name),
            is_exported=ctx.EXPORT() is not None,
            params=params,
            functions=functions,
        )

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
        return Return(value=self.visit(ctx.expression()) if ctx.expression() else None)

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
            then_statements=then_statements,
            else_statements=else_statements,
        )

    # Visit a parse tree produced by BugParser#letStatement.
    def visitLetStatement(self, ctx: BugParser.LetStatementContext):
        name = ctx.variableName().getText()
        expression = self.visit(ctx.expression())
        return Let(name=name, value=expression)

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
        operator = get_binary_operator(ctx.operator)
        left = self.visit(ctx.left)
        right = self.visit(ctx.right)

        return BinaryOperation(operator=operator, left=left, right=right)

    # Visit a parse tree produced by BugParser#callExpression.
    def visitCallExpression(self, ctx: BugParser.CallExpressionContext):
        # TODO: The expression should be stored within the call expression, rather than as text
        name = ctx.expression().getText()
        arguments = self.visit(ctx.argumentList()) if ctx.argumentList() else []
        return FunctionCall(name=name, arguments=arguments)

    # Visit a parse tree produced by BugParser#variableNameExpression.
    def visitVariableNameExpression(self, ctx: BugParser.VariableNameExpressionContext):
        name = ctx.variableName().getText()
        return Variable(name=name)

    # Visit a parse tree produced by BugParser#nestedExpression.
    def visitNestedExpression(self, ctx: BugParser.NestedExpressionContext):
        return self.visit(ctx.expression())

    # Visit a parse tree produced by BugParser#unaryExpression.
    def visitUnaryExpression(self, ctx: BugParser.UnaryExpressionContext):
        raise NotImplementedError()

    # Visit a parse tree produced by BugParser#memberDotExpression.
    def visitMemberDotExpression(self, ctx: BugParser.MemberDotExpressionContext):
        value = self.visit(ctx.expression())
        member = ctx.variableName().getText()

        return MemberAccess(value=value, member=member)

    # Visit a parse tree produced by BugParser#literalExpression.
    def visitLiteralExpression(self, ctx: BugParser.LiteralExpressionContext):
        return self.visit(ctx.literal())

    # Visit a parse tree produced by BugParser#literal.
    def visitLiteral(self, ctx: BugParser.LiteralContext):
        if ctx.INTEGER():
            return Number(value=int(ctx.INTEGER().getText()))
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
        variable_name = ctx.variableName().getText()
        expression = self.visit(ctx.expression())

        return Argument(name=variable_name, value=expression)

    # Visit a parse tree produced by BugParser#typeName.
    def visitTypeName(self, ctx: BugParser.TypeNameContext):
        raise NotImplementedError()
