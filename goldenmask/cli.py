import json
from pathlib import Path
from typing import Tuple

import click
from goldenmask import logger
from goldenmask.exceptions import UnsupportedLayerException
from goldenmask.protect import CompileallProtector, CythonProtector
from goldenmask.utils import get_build_info


# TODO: do i need to add an `--inplace` parameter ?
@click.command()
@click.argument("files_or_dirs", nargs=-1, type=click.Path(exists=True))
@click.option(
    "-l",
    "--layer",
    type=int,
    default=1,
    metavar="<int>",
    help="Level of protection: 1 - compileall; 2 - cython.",
)
@click.option(
    "-i", "--inplace", is_flag=True, help="Whether compile python files in place."
)
@click.option(
    "--no_smart",
    is_flag=True,
    help="This will copy and compile everything you specified.",
)
def goldenmask(
    files_or_dirs: Tuple[click.Path], layer: int, inplace: bool, no_smart: bool
):
    """Goldenmask is a tool to protect your python source code easily.

    FILES_OR_DIRS can be python files, wheel packages,source packages or dirs contain python files.
    """
    for file_or_dir in files_or_dirs:
        if not Path(str(file_or_dir)).exists():  # type: ignore
            logger.error(f"{file_or_dir} dose not exists!")
            continue
        if layer == 1:
            protector = CompileallProtector(str(file_or_dir), inplace, no_smart)
            success = protector.protect()
        elif layer == 2:
            protector = CythonProtector(str(file_or_dir), inplace, no_smart)
            success = protector.protect()
        else:
            raise UnsupportedLayerException(f"This layer {layer} is not supported now!")

        if protector and success:
            with open(protector.info_file, "w") as f:
                json.dump(get_build_info(), f, indent="\t")
        else:
            logger.error(
                f"{file_or_dir} can not be protected, please see the error message!"
            )
