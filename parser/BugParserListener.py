# Generated from BugParser.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .BugParser import BugParser
else:
    from BugParser import BugParser

# This class defines a complete listener for a parse tree produced by BugParser.
class BugParserListener(ParseTreeListener):

    # Enter a parse tree produced by BugParser#program.
    def enterProgram(self, ctx:BugParser.ProgramContext):
        pass

    # Exit a parse tree produced by BugParser#program.
    def exitProgram(self, ctx:BugParser.ProgramContext):
        pass


    # Enter a parse tree produced by BugParser#importStatements.
    def enterImportStatements(self, ctx:BugParser.ImportStatementsContext):
        pass

    # Exit a parse tree produced by BugParser#importStatements.
    def exitImportStatements(self, ctx:BugParser.ImportStatementsContext):
        pass


    # Enter a parse tree produced by BugParser#importStatement.
    def enterImportStatement(self, ctx:BugParser.ImportStatementContext):
        pass

    # Exit a parse tree produced by BugParser#importStatement.
    def exitImportStatement(self, ctx:BugParser.ImportStatementContext):
        pass


    # Enter a parse tree produced by BugParser#functionDef.
    def enterFunctionDef(self, ctx:BugParser.FunctionDefContext):
        pass

    # Exit a parse tree produced by BugParser#functionDef.
    def exitFunctionDef(self, ctx:BugParser.FunctionDefContext):
        pass


    # Enter a parse tree produced by BugParser#data.
    def enterData(self, ctx:BugParser.DataContext):
        pass

    # Exit a parse tree produced by BugParser#data.
    def exitData(self, ctx:BugParser.DataContext):
        pass


    # Enter a parse tree produced by BugParser#dataName.
    def enterDataName(self, ctx:BugParser.DataNameContext):
        pass

    # Exit a parse tree produced by BugParser#dataName.
    def exitDataName(self, ctx:BugParser.DataNameContext):
        pass


    # Enter a parse tree produced by BugParser#dataList.
    def enterDataList(self, ctx:BugParser.DataListContext):
        pass

    # Exit a parse tree produced by BugParser#dataList.
    def exitDataList(self, ctx:BugParser.DataListContext):
        pass


    # Enter a parse tree produced by BugParser#functionBody.
    def enterFunctionBody(self, ctx:BugParser.FunctionBodyContext):
        pass

    # Exit a parse tree produced by BugParser#functionBody.
    def exitFunctionBody(self, ctx:BugParser.FunctionBodyContext):
        pass


    # Enter a parse tree produced by BugParser#statements.
    def enterStatements(self, ctx:BugParser.StatementsContext):
        pass

    # Exit a parse tree produced by BugParser#statements.
    def exitStatements(self, ctx:BugParser.StatementsContext):
        pass


    # Enter a parse tree produced by BugParser#statement.
    def enterStatement(self, ctx:BugParser.StatementContext):
        pass

    # Exit a parse tree produced by BugParser#statement.
    def exitStatement(self, ctx:BugParser.StatementContext):
        pass


    # Enter a parse tree produced by BugParser#returnStatement.
    def enterReturnStatement(self, ctx:BugParser.ReturnStatementContext):
        pass

    # Exit a parse tree produced by BugParser#returnStatement.
    def exitReturnStatement(self, ctx:BugParser.ReturnStatementContext):
        pass


    # Enter a parse tree produced by BugParser#statementExpression.
    def enterStatementExpression(self, ctx:BugParser.StatementExpressionContext):
        pass

    # Exit a parse tree produced by BugParser#statementExpression.
    def exitStatementExpression(self, ctx:BugParser.StatementExpressionContext):
        pass


    # Enter a parse tree produced by BugParser#forLoop.
    def enterForLoop(self, ctx:BugParser.ForLoopContext):
        pass

    # Exit a parse tree produced by BugParser#forLoop.
    def exitForLoop(self, ctx:BugParser.ForLoopContext):
        pass


    # Enter a parse tree produced by BugParser#ifStatement.
    def enterIfStatement(self, ctx:BugParser.IfStatementContext):
        pass

    # Exit a parse tree produced by BugParser#ifStatement.
    def exitIfStatement(self, ctx:BugParser.IfStatementContext):
        pass


    # Enter a parse tree produced by BugParser#letStatement.
    def enterLetStatement(self, ctx:BugParser.LetStatementContext):
        pass

    # Exit a parse tree produced by BugParser#letStatement.
    def exitLetStatement(self, ctx:BugParser.LetStatementContext):
        pass


    # Enter a parse tree produced by BugParser#returnTypeName.
    def enterReturnTypeName(self, ctx:BugParser.ReturnTypeNameContext):
        pass

    # Exit a parse tree produced by BugParser#returnTypeName.
    def exitReturnTypeName(self, ctx:BugParser.ReturnTypeNameContext):
        pass


    # Enter a parse tree produced by BugParser#parameterList.
    def enterParameterList(self, ctx:BugParser.ParameterListContext):
        pass

    # Exit a parse tree produced by BugParser#parameterList.
    def exitParameterList(self, ctx:BugParser.ParameterListContext):
        pass


    # Enter a parse tree produced by BugParser#typedVariable.
    def enterTypedVariable(self, ctx:BugParser.TypedVariableContext):
        pass

    # Exit a parse tree produced by BugParser#typedVariable.
    def exitTypedVariable(self, ctx:BugParser.TypedVariableContext):
        pass


    # Enter a parse tree produced by BugParser#functionName.
    def enterFunctionName(self, ctx:BugParser.FunctionNameContext):
        pass

    # Exit a parse tree produced by BugParser#functionName.
    def exitFunctionName(self, ctx:BugParser.FunctionNameContext):
        pass


    # Enter a parse tree produced by BugParser#variableName.
    def enterVariableName(self, ctx:BugParser.VariableNameContext):
        pass

    # Exit a parse tree produced by BugParser#variableName.
    def exitVariableName(self, ctx:BugParser.VariableNameContext):
        pass


    # Enter a parse tree produced by BugParser#binaryExpression.
    def enterBinaryExpression(self, ctx:BugParser.BinaryExpressionContext):
        pass

    # Exit a parse tree produced by BugParser#binaryExpression.
    def exitBinaryExpression(self, ctx:BugParser.BinaryExpressionContext):
        pass


    # Enter a parse tree produced by BugParser#callExpression.
    def enterCallExpression(self, ctx:BugParser.CallExpressionContext):
        pass

    # Exit a parse tree produced by BugParser#callExpression.
    def exitCallExpression(self, ctx:BugParser.CallExpressionContext):
        pass


    # Enter a parse tree produced by BugParser#variableNameExpression.
    def enterVariableNameExpression(self, ctx:BugParser.VariableNameExpressionContext):
        pass

    # Exit a parse tree produced by BugParser#variableNameExpression.
    def exitVariableNameExpression(self, ctx:BugParser.VariableNameExpressionContext):
        pass


    # Enter a parse tree produced by BugParser#nestedExpression.
    def enterNestedExpression(self, ctx:BugParser.NestedExpressionContext):
        pass

    # Exit a parse tree produced by BugParser#nestedExpression.
    def exitNestedExpression(self, ctx:BugParser.NestedExpressionContext):
        pass


    # Enter a parse tree produced by BugParser#unaryExpression.
    def enterUnaryExpression(self, ctx:BugParser.UnaryExpressionContext):
        pass

    # Exit a parse tree produced by BugParser#unaryExpression.
    def exitUnaryExpression(self, ctx:BugParser.UnaryExpressionContext):
        pass


    # Enter a parse tree produced by BugParser#literalExpression.
    def enterLiteralExpression(self, ctx:BugParser.LiteralExpressionContext):
        pass

    # Exit a parse tree produced by BugParser#literalExpression.
    def exitLiteralExpression(self, ctx:BugParser.LiteralExpressionContext):
        pass


    # Enter a parse tree produced by BugParser#literal.
    def enterLiteral(self, ctx:BugParser.LiteralContext):
        pass

    # Exit a parse tree produced by BugParser#literal.
    def exitLiteral(self, ctx:BugParser.LiteralContext):
        pass


    # Enter a parse tree produced by BugParser#string.
    def enterString(self, ctx:BugParser.StringContext):
        pass

    # Exit a parse tree produced by BugParser#string.
    def exitString(self, ctx:BugParser.StringContext):
        pass


    # Enter a parse tree produced by BugParser#stringPart.
    def enterStringPart(self, ctx:BugParser.StringPartContext):
        pass

    # Exit a parse tree produced by BugParser#stringPart.
    def exitStringPart(self, ctx:BugParser.StringPartContext):
        pass


    # Enter a parse tree produced by BugParser#argumentList.
    def enterArgumentList(self, ctx:BugParser.ArgumentListContext):
        pass

    # Exit a parse tree produced by BugParser#argumentList.
    def exitArgumentList(self, ctx:BugParser.ArgumentListContext):
        pass


    # Enter a parse tree produced by BugParser#argument.
    def enterArgument(self, ctx:BugParser.ArgumentContext):
        pass

    # Exit a parse tree produced by BugParser#argument.
    def exitArgument(self, ctx:BugParser.ArgumentContext):
        pass


    # Enter a parse tree produced by BugParser#typeName.
    def enterTypeName(self, ctx:BugParser.TypeNameContext):
        pass

    # Exit a parse tree produced by BugParser#typeName.
    def exitTypeName(self, ctx:BugParser.TypeNameContext):
        pass


