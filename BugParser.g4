parser grammar BugParser;

options { tokenVocab=BugLexer; }

program:
    importStatements (data | functionDef)*
    EOF
    ;

importStatements: importStatement*;
importStatement: 'import' variableName ('::' variableName)* ';' ;

functionDef:
    'export'? 'function' functionName '(' parameterList? ')' ':' returnTypeName '{' functionBody '}'
    ;

data:
    'export'? 'data' dataName '(' dataList ')'
        ('{' functionDef* '}') ?
    ;

dataName: IDENTIFIER ;

dataList: typedVariable (',' typedVariable)* ;

functionBody: statements ;

statements: statement*;

statement:
    forLoop
    | letStatement
    | statementExpression
    ;

statementExpression: expression ';' ;

forLoop:
    'for' variableName ',' variableName 'in' expression '{' statements '}' ;

letStatement: 'let' variableName '=' expression ';';

returnTypeName: 'void' | typeName;

parameterList: params+=typedVariable (',' params+=typedVariable)* ;

typedVariable: variableName ':' typeName ;

functionName: IDENTIFIER ;
variableName: IDENTIFIER ;

expression:
    operator=(SUB | NOT) expression                         # unaryExpression
    | left=expression operator=(MUL | DIV) right=expression # binaryExpression
    | left=expression operator=(ADD | SUB) right=expression # binaryExpression
    | left=expression operator=(LT | GT) right=expression   # binaryExpression
    | left=expression operator=AND right=expression         # binaryExpression
    | left=expression operator=OR right=expression          # binaryExpression
    | left=expression operator=EQ right=expression          # binaryExpression
    | variableName                                          # variableNameExpression
    | literal                                               # literalExpression
    | expression '(' argumentList? ')'                      # callExpression
    | '(' expression ')'                                    # nestedExpression
    ;
//    | expression '.' variableName                           #

literal:
    INTEGER
    | string
    ;

string: OPEN_STRING stringPart* CLOSE_STRING;

stringPart:
    TEXT
    | START_EXPR expression RBRACE
    ;

argumentList: argument (',' argument)* ;

argument: variableName '=' expression ;

typeName:
    I32
    | CHAR
    | BOOLEAN
    | IDENTIFIER
    ;
