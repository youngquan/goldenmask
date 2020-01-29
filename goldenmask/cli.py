import json
import os
from pathlib import Path
from typing import Tuple

import click

from goldenmask import logger
from goldenmask.exceptions import UnsupportedLayerException
from goldenmask.protect import CompileallProtector, CythonProtector
from goldenmask.utils import remove_python_files, get_build_info

# TODO: do i need to add an `--inplace` parameter!
@click.command()
@click.argument('files_or_dirs',
                nargs=-1,
                type=click.Path(exists=True))
@click.option('-l', '--layer',
              type=int,
              default=1,
              help='Level of protection.')
@click.option('-i', '--inplace',
              is_flag=True)
def goldenmask(files_or_dirs: Tuple[click.Path], layer: int, inplace: bool):
    """
    Goldenmask is a tool to protect your python source code easily.
    """
    for file_or_dir in files_or_dirs:
        if not Path(file_or_dir).exists():
            logger.error(f'{file_or_dir} dose not exists!')
            continue
        protector = None
        success = False
        if layer == 1:
            protector = CompileallProtector(file_or_dir, inplace)
            success = protector.protect()
        elif layer == 2:
            protector = CythonProtector(file_or_dir, inplace)
            success = protector.protect()
        else:
            raise UnsupportedLayerException(f"This layer {layer} is not supported now!")

        if protector and success:
            with open(protector.info_file, 'w') as f:
                json.dump(get_build_info(), f, indent="\t")
        else:
            logger.error(f'{file_or_dir} can not be protected, please see the error message!')


