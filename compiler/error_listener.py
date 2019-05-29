from antlr4.error.ErrorListener import ErrorListener as AntlrErrorListener


class BugException(Exception):
    def __init__(self):
        super().__init__()


class BugSyntaxException(BugException):
    def __init__(self, offending_symbol, line, column, message, e):
        super().__init__()
        self.offending_symbol = offending_symbol
        self.line = line
        self.column = column
        self.message = message
        self.e = e

    def __repr__(self) -> str:
        return f"Syntax error at line {self.line} column {self.column}. {self.message}"

    def __str__(self) -> str:
        return repr(self)


class ErrorListener(AntlrErrorListener):
    def __init__(self):
        super().__init__()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise BugSyntaxException(
            offending_symbol=offendingSymbol, line=line, column=column, message=msg, e=e
        )

    def reportAmbiguity(
        self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs
    ):
        pass

    def reportAttemptingFullContext(
        self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs
    ):
        pass

    def reportContextSensitivity(
        self, recognizer, dfa, startIndex, stopIndex, prediction, configs
    ):
        pass
