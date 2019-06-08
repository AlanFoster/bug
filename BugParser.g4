parser grammar BugParser;

options { tokenVocab=BugLexer; }

program:
    importStatements (trait | data | functionDef)*
    EOF
    ;

importStatements: importStatement*;
importStatement: 'import' variableName ('::' variableName)* ';' ;

functionDef:
    'export'? 'function' functionName '(' parameterList? ')' ':' returnTypeName '{' functionBody '}'
    ;

trait:
    'trait' traitName '{' traitFunctionDef* '}' ;

traitName: IDENTIFIER ;

traitFunctionDef:
    'function' traitFunctionName '(' parameterList ')' ':' returnTypeName ';' ;

traitFunctionName: IDENTIFIER ;

data:
    'export'? 'data' dataName '(' dataList? ')'
        ('implements' traitName) ?
        ('{' functionDef* '}') ?
    ;

dataName: IDENTIFIER ;

dataList: params+=typedVariable (',' params+=typedVariable)* ;

functionBody: statements ;

statements: statement*;

statement:
    forLoop
    | ifStatement
    | letStatement
    | statementExpression
    | returnStatement
    ;

returnStatement: 'return' expression ? ';' ;

statementExpression: expression ';' ;

forLoop:
    'for' variableName ',' variableName 'in' expression '{' statements '}' ;

ifStatement:
    'if' '(' condition=expression ')' '{' then_statements=statements '}'
    ('else' '{' else_statements=statements '}') ?
    ;

letStatement: 'let' variableName '=' expression ';';

returnTypeName: 'void' | typeName;

parameterList: params+=typedVariable (',' params+=typedVariable)* ;

typedVariable: variableName ':' typeName ;

functionName: IDENTIFIER ;
variableName: IDENTIFIER ;

expression:
    expression '.' variableName                             # memberDotExpression
    | expression '(' argumentList? ')'                      # callExpression
    | operator=(SUB | NOT) expression                       # unaryExpression
    | left=expression operator=(MUL | DIV) right=expression # binaryExpression
    | left=expression operator=(ADD | SUB) right=expression # binaryExpression
    | left=expression operator=(LT | GT) right=expression   # binaryExpression
    | left=expression operator=AND right=expression         # binaryExpression
    | left=expression operator=OR right=expression          # binaryExpression
    | left=expression operator=EQEQ right=expression        # binaryExpression
    | variableName                                          # variableNameExpression
    | literal                                               # literalExpression
    | '(' expression ')'                                    # nestedExpression
    ;

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
