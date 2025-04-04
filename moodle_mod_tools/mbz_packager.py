"""Module to package directories into .mbz archives without nesting."""

import os
import tarfile
import contextlib
import tempfile
import shutil
from typing import Optional, ContextManager


def package_mbz(source_dir: str, output_file: str) -> None:
    """Create a .mbz archive from the contents of source_dir without nested subdirectories."""
    with tarfile.open(output_file, "w:gz") as tar:
        for item in os.listdir(source_dir):
            path = os.path.join(source_dir, item)
            tar.add(path, arcname=item)


def decompress_mbz(archive_path: str, output_dir: str) -> None:
    """Decompress a .mbz archive into output_dir."""
    with tarfile.open(archive_path, "r:gz") as tar:
        tar.extractall(path=output_dir)

@contextlib.contextmanager
def with_extracted_tar(input_tar: str, output_tar: Optional[str] = None) -> ContextManager[str]:
    temp_dir = tempfile.mkdtemp()
    try:
        decompress_mbz(input_tar, temp_dir)
        yield temp_dir
        if output_tar:
            package_mbz(temp_dir, output_tar)
    finally:
        shutil.rmtree(temp_dir)
