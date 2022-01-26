import pathlib
import os
from unittest import TestCase

from pysh.bash_vm.shell_command import ShellCommand, ShellCommandOutput


class TestShellCommand(TestCase):

    def setUp(self):
        self.test_file_path = os.path.join(pathlib.Path(__file__).parent.resolve(), 'test_file.txt')
        with open(self.test_file_path) as f:
            self.test_file_contents: str = f.read()

    def testShellCommandsCanExecuteBashCommands(self):
        catCmd = ShellCommand(f'cat {self.test_file_path}')
        result = catCmd.exec()
        self.assertEqual(result.value, self.test_file_contents)

    def testShellCommandOutputGeneratesIteratorOverLines(self):
        catCmd = ShellCommand(f'cat {self.test_file_path}')
        result = catCmd.exec()
        lines = result.lines()
        expectedLines = self.test_file_contents.split('\n')
        for a, b in zip(expectedLines, lines):
            self.assertEqual(a, b.value)

    def testShellCommandOutputGeneratesIteratorOverTokens(self):
        catCmd = ShellCommand(f'cat {self.test_file_path}')
        result = catCmd.exec()
        for token, expected in zip(result, self.test_file_contents.split()):
            self.assertEqual(token, expected)

    def testShellCommandsHaveSettableEnvironmentVariables(self):
        envCommand = ShellCommand("echo -n $ENV_STATE")
        result = envCommand.exec(ENV_STATE="CurrentState")
        expected = "CurrentState"
        self.assertEqual(result.value, expected)

