from typing import Generator
from contextlib import contextmanager

from FileReaderInterface import FileReaderInterface


class MyFileReader(FileReaderInterface):
    @contextmanager
    def read_file(self, file_name: str, buffer_size: int):
        """Read file by chunks using context manager."""
        with open(file_name, 'r') as f:
            def generator() -> Generator[str, None, None]:
                while True:
                    chunk = f.read(buffer_size)
                    if not chunk:
                        break
                    yield chunk
            yield generator()
