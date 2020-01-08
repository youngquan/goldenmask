import compileall
import os
from pathlib import Path
from typing import Tuple

import click

@click.command()
@click.argument('files_or_dirs',
                nargs=-1,
                type=click.Path(exists=True))
@click.option('-r', '--replace',
              is_flag=True,
              help='Replace the source file.')
def goldenmask(files_or_dirs: Tuple[click.Path], replace: bool):
    """
    Goldenmask is a tool to protect your python source code easily.
    """
    for file_or_dir in files_or_dirs:

        if Path(file_or_dir).is_dir():
            is_dir = True
        else:
            is_dir = False        
        if is_dir:
            compileall.compile_dir(file_or_dir, force=True, legacy=True, optimize=2)
        else:
            compileall.compile_file(file_or_dir, force=True, legacy=True, optimize=2)
        
        if replace:
            if is_dir:
                for py_file in Path(file_or_dir).glob('*.py'):
                    os.remove(py_file)
            else:
                os.remove(file_or_dir)
