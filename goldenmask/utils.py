import os
import shutil
import sys
import tarfile
import tempfile
import zipfile
from shutil import rmtree
from typing import Dict, Union, List, Tuple
from pathlib import Path
import re

from goldenmask import GOLDENMASK, logger
from goldenmask.exceptions import UnsupportedFileError



def remove_python_files(dir_):
    for py_file in Path(dir_).rglob('*.py'):
        os.remove(str(py_file))


def is_file(file_or_dir):
    if Path(file_or_dir).is_file():
        file = True
    else:
        file = False
    return file


def get_file_type(file: str) -> Tuple[bool, bool, bool]:
    """Use file's suffix to determine its type.
    Args:
        file: filename or file path string

    Returns:
        A tuple like (is_pyfile, is_wheel, is_tarball)
    """

    def is_pyfile(file: str) -> bool:
        if file.endswith('.py'):
            return True
        else:
            return False

    def is_tarball(file: str) -> bool:
        if file.endswith('.tar.gz'):
            return True
        else:
            return False

    def is_wheel(file: str) -> bool:
        if file.endswith('.whl'):
            return True
        else:
            return False

    return is_pyfile(file), is_wheel(file), is_tarball(file)


def unpack(file: Path) -> Path:
    tmp_dir = Path(tempfile.mkdtemp(prefix="goldenmask-")).resolve()
    if str(file).endswith('.tar.gz'):
        with tarfile.open(file) as tar:
            tar.extractall(tmp_dir)
    elif str(file).endswith('whl'):
        with zipfile.ZipFile(file) as wheel:
            wheel.extractall(tmp_dir)
    else:
        raise UnsupportedFileError(f"{file} can not be unpack, only support '.py', '.tar.gz' and '.whl' now")
    return tmp_dir


def pack(unpacked_dir: Path, source_file: Path, inplace: bool) -> Path:

    archive_file = unpacked_dir / source_file.name
    if str(source_file).endswith('.whl'):
        with zipfile.ZipFile(archive_file, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for file in unpacked_dir.rglob('*'):
                # archive has already existed.
                if file.name != source_file.name:
                    zip_file.write(file, arcname=file.relative_to(unpacked_dir))
    else:
        with tarfile.open(str(archive_file), "w:gz") as tar:
            for file in unpacked_dir.rglob('*'):
                if file.name != source_file.name:
                    tar.add(file, arcname=file.relative_to(unpacked_dir))

    if inplace:
        result_file = source_file
        shutil.move(archive_file, result_file)
    else:
        # TODO: This should be reconsidered!!!!
        result_file = source_file.parent / '__goldenmask__' / source_file.name
        if result_file.exists():
            os.remove(result_file)
        else:
            try:
                result_file.parent.mkdir()
            except FileExistsError:
                pass
        shutil.move(archive_file, result_file)

    return result_file


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
    def __init__(self, directory: Path, ignore_file_name: str = '.goldenmaskignore'):
        self.dir = directory
        self.ignore_file = self.dir / ignore_file_name

        if not self.ignore_file.exists():
            self.ignore_file = Path(__file__).parent / '.goldenmaskignore'

        ignore_patterns = []
        with self.ignore_file.open(encoding='utf8') as f:
            for line in f:
                if line.startswith('#') or not line.strip():
                    continue
                else:
                    ignore_patterns.append(line.strip().strip("/"))
        # patterns under root dir will not be copied
        # TODO: This should be moved may be
        self.ignore_patterns = ignore_patterns
        # python files under these dirs will not be compiled

    def search(self, fullname: str) -> bool:
        # TODO: whether to capture the exceptions!
        relative_path = Path(fullname).relative_to(self.dir)
        python_ignore_folders = ["tests/"] + [folder + '/' for folder in self.get_virtualenv_folders()]
        if 'site-packages' in str(relative_path):
            return True
        for ignore_pattern in python_ignore_folders:
            # TODO： make sure that `ignore_pattern.encode('unicode_escape').decode()` is unnecessary!
            if re.match(ignore_pattern, relative_path.as_posix()):
                return True
        return False

    def copy(self, path: str, names: List[str]):
        """
        Used for the parameter `ignore` in function `shutil.copytree`.
        Do not copy virtualenv folder and `__goldenmask__`.
        """
        if path == str(self.dir):
            subset = self.ignore_patterns
        else:
            subset = [GOLDENMASK, '__pycache__', '.idea', '.git', '.svn', '.vscode', '.eggs', '*.egg-info',
                      '.pytest_cache', 'tests']
        for name in names:
            if (Path(path) / name / 'Lib/site-packages').exists():
                subset.append(name)
        return subset

    def get_virtualenv_folders(self):
        virtualenv_folders = []
        for name in self.dir.iterdir():
            if name.is_dir():
                if (self.dir / name / 'Lib/site-packages').exists():
                    virtualenv_folders.append(str(name))
        return virtualenv_folders

