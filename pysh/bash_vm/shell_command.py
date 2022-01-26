from __future__ import annotations

import subprocess
import os

from typing import List, Dict, Iterator, Optional, Tuple


class ShellCommand:

    def __init__(self, cmd: str):
        self.run_args = [
            "bash", "-c", f'{cmd}'
        ]
        # self.run_args: List[str] = [executable, *args]


    def exec(self, **extra_environ: str) -> ShellCommandOutput:
        result = subprocess.run(self.run_args,
                                stdout=subprocess.PIPE,
                                env={
                                    **os.environ,
                                    **(extra_environ if extra_environ else {})
                                }
                                )
        print("Finished shell command")
        return ShellCommandOutput(str(result.stdout, 'utf-8'), result.returncode)


class ShellCommandOutput:

    def __init__(self, output_body: str, code: int):
        self._code = code
        self._value = output_body

    @property
    def succeeded(self) -> bool:
        return self._code == 0

    @property
    def code(self) -> int:
        return self._code

    @property
    def value(self) -> str:
        return self._value

    def lines(self) -> List[ShellCommandOutput]:
        return [
            ShellCommandOutput(substr, self.code)
            for substr in self.value.splitlines()
            if substr
        ]

    def __iter__(self) -> Iterator[str]:
        return iter(self._split_tokens())

    def __str__(self) -> str:
        return f'<STDOUT value={self.value} code={self.code} >'

    def _split_tokens(self) -> List[str]:
        ret = []
        in_quotes = None
        accumulator: List[str] = []
        for char in self.value:
            if _whitespace(char) and not in_quotes and accumulator:
                ret.append(''.join(accumulator))
                accumulator = []
            elif in_quotes == None and _quotes(char):
                in_quotes = char
            elif in_quotes and in_quotes == char:
                in_quotes = None
                if accumulator:
                    ret.append(''.join(accumulator))
                    accumulator = []
            elif in_quotes and _quotes(char):
                raise ValueError(
                    f"Found unmatched quote characters in string {self.value}")
            else:
                accumulator.append(char)
        return ret


def _quotes(c: str) -> bool:
    return c in ['"', "'"]


def _whitespace(c: str) -> bool:
    return str.isspace(c)
