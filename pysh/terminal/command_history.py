import os
from collections import deque
import atexit

class CommandHistory:

    def __init__(self, num_lines: int = 1000):
        self.history_file_path = os.path.expanduser('~/.pysh_history')
        with open(self.history_file_path) as history_file:
            self.history = self.history_file.read().splitlines()
            self.history = deque(self.history)
            self.num_lines = num_lines
            self._cleanup = lambda: _cleanup_file(self.history_file_path)
            atexit.register(func)


    def add_command(self, command: str):
        self.history.append(command)
        if len(self.history) > self.num_lines:
            self.history.popleft()

def _cleanup_file(file_path: str, history: List[str]) -> None:
    os.remove(file_path)
    with open(file_path, 'w+') as file:
        file.write('\n'.join(history))