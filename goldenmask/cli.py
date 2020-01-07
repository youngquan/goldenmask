import compileall
import os
import shutil
from pathlib import Path
from typing import Tuple

import click
# from click import Path

@click.command()
@click.argument('files_or_dirs',nargs=-1, type=click.Path(exists=True))
@click.option('-r', '--replace', is_flag=True)
def goldenmask(files_or_dirs: Tuple[click.Path], replace: bool):
    for file_or_dir in files_or_dirs:

        if Path(file_or_dir).is_dir():
            is_dir = True
        else:
            is_dir = False
        
        if is_dir:
            compileall.compile_dir(file_or_dir, legacy=True, optimize=2)
        else:
            compileall.compile_file(file_or_dir, legacy=True, optimize=2)
        
        if replace:
            if is_dir:
                shutil.rmtree(file_or_dir)
            else:
                os.remove(file_or_dir)

        
