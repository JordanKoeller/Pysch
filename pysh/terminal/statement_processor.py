from typing import List, Optional


class StatementProcessor:
    """
StatementProcessor

Accepts lines as input, aggregates into statements.

Some Notes:
+ If the statement you are in consists of an indented block, an empty line is used
    to signify the end of the block. In practice, this means the user needs to have one
    empty line to cause the statement to flush and start executing.
+ To support indention blocks, this class needs to track indention level, as well as know
  when the appropriate blank line has been entered to terminate the statement, if an indention
  is present.

Has getters to get:

  + current indention level
  + text of completed statement
  + boolean indicating if the statement is complete or not
    """
    def __init__(self):
        self._statement_lines: List[str] = []
        self._indention_level: int = 0
        self._backtick_count = 0

    def process_line(self, line: str) -> Optional[str]:
        """
        Accepts Lines as input and appends them to an array of lines in the current statement.

        Returns the full statement if this line completes a statement.
        """
        trimmed_line = self._trim_comments(line)
        self._statement_lines.append(line)
        for c in line:
            if c == '`':
                self._backtick_count += 1
        if trimmed_line.endswith(':'):
            self._indention_level += 1
        if self._ends_statement(line):
            return self._flush_statement()
        return None
        


    ##############################
    #   Private methods follow   #
    ##############################

    def _flush_statement(self) -> str:
        """
        This method cleans up the state of the StatementProcessor after a statement
        has been fully formed. Returns the fully formed statement.
        """
        self._indention_level = 0
        self._backtick_count = 0
        ret = '\n'.join(self._statement_lines)
        self._statement_lines = []
        return ret

    def _trim_comments(self, line: str) -> str:
        if '#' in line:
            return line.split('#')[0].rstrip()
        return line.rstrip()

    def _ends_statement(self, line: str) -> bool:
        """
        Checks to see if the passed-in line is sufficient to end the current statement.
        There are a few different things to check.

        A statement is only over if all of the following are met:
        + There is an even number of backticks (no unclosed bash injections)
        + The indention level is zero AND the line is not an emptystring.
        + The indention level is greater than zero AND the passed-in line is an empty line.
        """
        return self._backtick_count % 2 == 0 and (
            (self._indention_level > 0 and line.rstrip() == '') or
            (self._indention_level == 0 and line.rstrip() != ''))