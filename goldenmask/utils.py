import os
import sys
from typing import Dict, Union, List
from pathlib import Path
import fnmatch
import re

from goldenmask import GOLDENMASK


def remove_python_files(dir_):
    for py_file in Path(dir_).rglob('*.py'):
            os.remove(str(py_file))


def is_file(file_or_dir):
    if Path(file_or_dir).is_file():
        file = True
    else:
        file = False
    return file


def get_build_info() -> Dict[str, str]:
    return {
        "python_version": sys.version,
        "build_platform": sys.platform,
    }


def virtualenv_folder(path, names):
    """
    Used for the parameter `ignore` in function `shutil.copytree`.
    Do not copy virtualenv folder and `__goldenmask__`.
    """
    subset = [GOLDENMASK, '__pycache__', '.idea', '.git', '.svn', '.vscode', '.eggs', '*.egg-info',
              '.pytest_cache', 'tests']
    for name in names:
        if (Path(path) / name / 'Lib/site-packages').exists():
            subset.append(name)
    return subset


def is_entrypoint(file: Union[str, Path]) -> bool:
    with Path(file).open(encoding='utf8') as f:
        for line in f:
            # print(line)
            if (line.strip().replace(" ", "") == "if__name__=='__main__':" or
                    line.strip().replace(" ", "") == 'if__name__=="__main__":'):
                return True
        return False


def rename_so_and_pyd_file(file: Union[str, Path]):
    if sys.platform == 'win32' or sys.platform == 'cygwin':
        suffix = '.pyd'
    else:
        suffix = '.so'
    pyd_files: List[Path] = list(file.parent.glob(f'{file.stem}.*{suffix}'))
    # print(file)
    # print(pyd_files)
    # assert len(pyd_files) > 1
    if pyd_files:
        pyd_files[0].rename(file.parent / (file.stem + suffix))


class Ignore:
    def __init__(self, directory: Path, ignore_file_name: str='.goldenmaskignore'):
        self.dir = directory
        self.ignore_file = self.dir / ignore_file_name
        if not self.ignore_file.exists():
            self.ignore_file = Path('.goldenmaskignore')
        ignore_pattern_set = set()

        with self.ignore_file.open(encoding='utf8') as f:
            for line in f:
                if line.startswith('#') or not line.strip():
                    continue
                else:
                    ignore_pattern_set.add(line.strip())
        self.patterns = ignore_pattern_set
        # TODO: whether the path of the virtual environment needs to be detected
        self.python_ignore_folders = ["venv/", "env/", ".venv", ".env", "ENV/", "env.bak/", "venv.bak/", "tests/"]

    def search(self, fullname: str) -> bool:
        relative_path = Path(fullname).relative_to(self.dir)
        for ignore_pattern in self.python_ignore_folders:
            # TODO： make sure that `ignore_pattern.encode('unicode_escape').decode()` is unnecessary!
            if re.match(ignore_pattern, relative_path.as_posix()):
                return True
        return False

    def copy(self, path, names):
        """
        Used for the parameter `ignore` in function `shutil.copytree`.
        Do not copy virtualenv folder and `__goldenmask__`.
        """
        subset = [GOLDENMASK, '__pycache__', '.idea', '.git', '.svn', '.vscode', '.eggs', '*.egg-info',
                  '.pytest_cache', 'tests']
        for name in names:
            if (Path(path) / name / 'Lib/site-packages').exists():
                subset.append(name)
        return subset

    def virtualenv_folders(self):
        folders = []
        for name in self.dir.iterdir():
            if name.is_dir():
                if (self.dir / name / 'Lib/site-packages').exists():
                    folders.append(str(name))
        return folders



