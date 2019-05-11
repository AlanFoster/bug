# Generated from BugParser.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .BugParser import BugParser
else:
    from BugParser import BugParser

# This class defines a complete generic visitor for a parse tree produced by BugParser.

class BugParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by BugParser#program.
    def visitProgram(self, ctx:BugParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BugParser#importStatements.
    def visitImportStatements(self, ctx:BugParser.ImportStatementsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BugParser#importStatement.
    def visitImportStatement(self, ctx:BugParser.ImportStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BugParser#functionDef.
    def visitFunctionDef(self, ctx:BugParser.FunctionDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BugParser#data.
    def visitData(self, ctx:BugParser.DataContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BugParser#dataName.
    def visitDataName(self, ctx:BugParser.DataNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BugParser#dataList.
    def visitDataList(self, ctx:BugParser.DataListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BugParser#functionBody.
    def visitFunctionBody(self, ctx:BugParser.FunctionBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BugParser#statements.
    def visitStatements(self, ctx:BugParser.StatementsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BugParser#statement.
    def visitStatement(self, ctx:BugParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BugParser#returnStatement.
    def visitReturnStatement(self, ctx:BugParser.ReturnStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BugParser#statementExpression.
    def visitStatementExpression(self, ctx:BugParser.StatementExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BugParser#forLoop.
    def visitForLoop(self, ctx:BugParser.ForLoopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BugParser#ifStatement.
    def visitIfStatement(self, ctx:BugParser.IfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BugParser#letStatement.
    def visitLetStatement(self, ctx:BugParser.LetStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BugParser#returnTypeName.
    def visitReturnTypeName(self, ctx:BugParser.ReturnTypeNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BugParser#parameterList.
    def visitParameterList(self, ctx:BugParser.ParameterListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BugParser#typedVariable.
    def visitTypedVariable(self, ctx:BugParser.TypedVariableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BugParser#functionName.
    def visitFunctionName(self, ctx:BugParser.FunctionNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BugParser#variableName.
    def visitVariableName(self, ctx:BugParser.VariableNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BugParser#binaryExpression.
    def visitBinaryExpression(self, ctx:BugParser.BinaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BugParser#callExpression.
    def visitCallExpression(self, ctx:BugParser.CallExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BugParser#variableNameExpression.
    def visitVariableNameExpression(self, ctx:BugParser.VariableNameExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BugParser#nestedExpression.
    def visitNestedExpression(self, ctx:BugParser.NestedExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BugParser#unaryExpression.
    def visitUnaryExpression(self, ctx:BugParser.UnaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BugParser#literalExpression.
    def visitLiteralExpression(self, ctx:BugParser.LiteralExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BugParser#memberDotExpression.
    def visitMemberDotExpression(self, ctx:BugParser.MemberDotExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BugParser#literal.
    def visitLiteral(self, ctx:BugParser.LiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BugParser#string.
    def visitString(self, ctx:BugParser.StringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BugParser#stringPart.
    def visitStringPart(self, ctx:BugParser.StringPartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BugParser#argumentList.
    def visitArgumentList(self, ctx:BugParser.ArgumentListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BugParser#argument.
    def visitArgument(self, ctx:BugParser.ArgumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BugParser#typeName.
    def visitTypeName(self, ctx:BugParser.TypeNameContext):
        return self.visitChildren(ctx)



del BugParser