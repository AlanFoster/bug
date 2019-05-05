lexer grammar BugLexer;

// keywords
IF: 'if' ;
ELSE: 'else' ;
FOR: 'for' ;
IN: 'in' ;
LET: 'let' ;
DATA: 'data' ;
EXPORT: 'export' ;
IMPORT: 'import' ;
FUNCTION: 'function' ;
RETURN: 'return' ;

VOID: 'void' ;
I32: 'i32';
CHAR: 'char' ;
BOOLEAN: 'boolean' ;

// Separators
LBRACE : '{' -> pushMode(DEFAULT_MODE);
RBRACE : '}' -> popMode;
LPAREN : '(' ;
RPAREN : ')' ;
LBRACK : '[' ;
RBRACK : ']' ;
DOT : '.' ;
COMMA : ',' ;
SEMI : ';' ;
DOUBLE_COLON: '::' ;
COLON: ':' ;
ARROW: '->' ;

// Operators
ADD : '+' ;
SUB : '-' ;
MUL: '*' ;
DIV: '/' ;
AND: '&' ;
OR: '|' ;
LT: '<' ;
GT: '>' ;
EQEQ: '==' ;
EQ: '=' ;
NOT: '~' ;

// Atoms

INTEGER: [0-9]+ ;
IDENTIFIER: [_a-zA-Z] [a-zA-Z0-9_]* ;

OPEN_STRING: '`' -> pushMode(STRING) ;
LINE_COMMENT: ('//' ~( '\r' | '\n' )*) -> channel(HIDDEN) ;
WS: [ \t\n\r]+ -> channel(HIDDEN);

mode STRING;

START_EXPR: '${' -> pushMode(DEFAULT_MODE) ;
END_EXPR: RBRACE -> popMode;
CLOSE_STRING: '`' -> popMode;

TEXT: ~( '`' | '$' )+ ;
