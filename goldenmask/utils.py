import os
import sys
from typing import Dict, Union, List
from pathlib import Path


def remove_python_files(dir_):
    for py_file in Path(dir_).rglob('*.py'):
            os.remove(str(py_file))


def is_file(file_or_dir):
    if Path(file_or_dir).is_dir():
        file = False
    else:
        file = True
    return file


def get_build_info() -> Dict[str, str]:
    return {
        "python_version": sys.version,
        "build_platform": sys.platform,
    }


def virtualenv_folder(path, names):
    """
    Used for the parameter `ignore` in function `shutil.copytree`.
    Do not copy virtualenv folder.
    """
    subset = []
    for name in names:
        if (Path(path) / name / 'Lib/site-packages').exists():
            subset.append(name)
    return subset


def is_entrypoint(file: Union[str, Path]) -> bool:
    with Path(file).open(encoding='utf8') as f:
        for line in f:
            if line.strip().replace(" ", "") == "if__name__=='__main__':":
                return True
        return False


def rename_so_and_pyd_file(file: Union[str, Path]):
    if sys.platform == 'win32' or sys.platform == 'cygwin':
        suffix = '.pyd'
    else:
        suffix = '.so'
    pyd_files: List[Path] = list(file.parent.glob(f'{file.stem}.*{suffix}'))
    assert pyd_files == 1
    pyd_files[0].rename(file.parent / file.stem / suffix)



