import sys
from readchar import readchar
from readchar.key import CTRL_C, CTRL_D, CTRL_Q, UP, DOWN, LEFT, RIGHT, ESC
from enum import Enum
from typing import List, Set

from .statement_processor import StatementProcessor
from ..py_vm.session import PyVm
from .command_history import CommandHistory

TERMINATE_CODES: Set[str] = {CTRL_D, CTRL_Q}
SPECIAL_CODES: Set[str] = {UP, DOWN, LEFT, RIGHT, ESC}

class Repl:
    """
    This class is responsible for:
    1. Reading from stdin.
    2. Sending valid python characters to the statement_processor (valid meaning not part of a comment)
    3. Eventually, printing to screen as well with syntax highlighting via curses.
    """
    def __init__(self):
        self._line_characters: List[str] = []
        self._statement_processor = StatementProcessor()
        self._vm = PyVm()
        self._command_history = CommandHistory()

    def process_char(self, char: str):
        if self._is_special_character(char):
            return self._process_special_character(char)
        if char == '\n':
            expression = ''.join(self._line_characters)
            self._line_characters = []
            statement = self._statement_processor.process_line(expression)
            if statement:
                self._run_statement(statement)
        else:
            self._line_characters.append(char)
        
        
    def exit(self):
        sys.exit()

    ##############################
    #   Private methods follow   #
    ##############################

    def _run_statement(self, statement: str):
        """
        Accepts a completed statement (generated from the StatementProcessor)
        as input, and runs it.

        Right now, the only two actions to happen on a statement is to
        1. Run it throught the VM
        2. send it to the history manager to be tabulated.
        """
        self._vm.run_py_command(statement)
        # self._command_history.tabulate_command(statement)

    def _is_special_character(self, char: str) -> bool:
        # Special characters are any keystrokes that don't go in the line_characters array.
        # Examples include arrow keys, Escape, Ctrl+C, Ctrl+D, etc.
        # The only exception would be newline. Newline does NOT count as a special character.
        return char in TERMINATE_CODES or char in SPECIAL_CODES

    def _process_special_character(self, char: str):
        if self._is_exit_code(char):
            self.exit()

    def _is_exit_code(self, char: str) -> bool:
        return char in TERMINATE_CODES