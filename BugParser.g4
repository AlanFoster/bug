parser grammar BugParser;

options { tokenVocab=BugLexer; }

program:
    importStatements*? (data | functionDef)*
    EOF
    ;

importStatements: importStatement;
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
    | expression ';'
    ;

forLoop:
    'for' variableName ',' variableName 'in' expression '{' statements '}' ;

letStatement: 'let' variableName '=' expression ';';

returnTypeName: 'void' | typeName;

parameterList: typedVariable (',' typedVariable)* ;

typedVariable: variableName ':' typeName ;

functionName: IDENTIFIER ;
variableName: IDENTIFIER ;

expression:
    operator=(SUB | NOT) expression
    | left=expression operator=(MUL | DIV) right=expression
    | left=expression operator=(ADD | SUB) right=expression
    | variableName
    | literal
    | expression '(' argumentList? ')' // # CallExpression
    | expression '.' variableName
    | '[' ']'
    | '(' expression ')'
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
