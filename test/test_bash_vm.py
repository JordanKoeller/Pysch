import pathlib
import os
from unittest import TestCase

from pysh.bash_vm.shell_command import ShellCommand, ShellCommandOutput


class TestShellCommand(TestCase):

    def setUp(self):
        self.test_file_path = os.path.join(pathlib.Path(__file__).parent.resolve(), 'test_file.txt')
        with open(self.test_file_path) as f:
            self.test_file_contents = f.read()

    def testShellCommandsCanExecuteBashCommands(self):
        catCmd = ShellCommand("echo", "LOOK AT THIS GRAPH")
        result = catCmd.exec()
        self.assertEqual(result.value, "LOOK AT THIS GRAPH")

