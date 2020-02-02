import compileall
import os
import re
import shutil
from pathlib import Path

# from distutils.core import setup
from setuptools import setup
from Cython.Build import cythonize
from Cython.Compiler import Options

from goldenmask import logger
from goldenmask.utils import is_file, remove_python_files, virtualenv_folder, is_entrypoint, rename_so_and_pyd_file

Options.docstrings = False

IGNORE_FOLDERS_RE = (r"[/\\][.]svn[/\\]|[/\\][.]git[/\\]|[/\\]env[/\\]|[/\\]venv[/\\]|[/\\]tests[/\\]|"
                     r"[/\\]Lib[/\\]|[/\\]site-packages[/\\]")


class BaseProtector:
    def __init__(self, file_or_dir, inplace):
        self.file_or_dir = Path(file_or_dir)
        self.is_file = is_file(file_or_dir)
        self.inplace = inplace
        if self.is_file:
            if self.inplace:
                self.file = self.file_or_dir
            else:
                self.file = self.file_or_dir.parent / '__goldenmask__' / self.file_or_dir.name
                if self.file.exists():
                    os.remove(self.file)
                else:
                    try:
                        self.file.parent.mkdir()
                    except FileExistsError:
                        pass
                shutil.copy(self.file_or_dir, self.file)
            self.info_file = self.file.parent / '.goldenmask'
            self.build_temp = self.file.parent / 'build-goldenmask'
        else:
            if self.inplace:
                self.dir = self.file_or_dir
            else:
                self.dir = Path(file_or_dir) / '__goldenmask__'
                if self.dir.exists():
                    # TODO: may be I should try to speed !
                    shutil.rmtree(self.dir)
                shutil.copytree(self.file_or_dir, self.dir, ignore=virtualenv_folder)
            self.info_file = self.dir / '.goldenmask'
            self.build_temp = self.dir / 'build-goldenmask'


class CompileallProtector(BaseProtector):

    def __init__(self, file_or_dir, inplace=False):
        super().__init__(file_or_dir, inplace)

    def protect(self):
        if self.is_file:
            success = compileall.compile_file(self.file, force=True, legacy=True, optimize=2, quiet=1)
            if success:
                os.remove(self.file)
        else:
            if self.inplace:
                # TODO: how about write a class with an method named search
                rx = re.compile(IGNORE_FOLDERS_RE)
            else:
                rx = None
            success = compileall.compile_dir(self.dir, force=True, legacy=True, optimize=2, quiet=1,
                                             rx=rx,
                                             workers=os.cpu_count())
            if success:
                remove_python_files(self.dir)
        return success


class CythonProtector(BaseProtector):

    def __init__(self, file_or_dir, inplace=False):
        super().__init__(file_or_dir, inplace)

    def protect(self):
        success = True
        if self.is_file:
            success = True
            ext_modules = cythonize(
                str(self.file),
                compiler_directives={'language_level': 3}
            )
            try:
                os.chdir(str(self.file.parent))
                setup(ext_modules=ext_modules, script_args=["build_ext", "--inplace"])
            except Exception as e:
                logger.warning(f'Can not build file {self.file} using Cython, we will try to use Compileall!')
                logger.warning(e)
                protector = CompileallProtector(self.file, inplace=True)
                success = protector.protect()
            if success:
                self.clean(self.file)
                shutil.rmtree(self.file.parent / 'build')
            return success
        else:
            python_files_normal = []
            for file in Path(self.dir).rglob('*.py'):
                if re.compile(IGNORE_FOLDERS_RE).search(str(file)):
                    # exclude folder .svn .git env venv Lib site-packages
                    continue
                if ((file.stem.startswith('__') and file.stem.endswith('__')) or
                        is_entrypoint(file) or
                        file.name == 'setup.py'):
                    protector = CompileallProtector(file, inplace=True)
                    success = protector.protect()
                    if not success:
                        break
                else:
                    python_files_normal.append(str(file))

            ext_modules = cythonize(
                python_files_normal,
                compiler_directives={'language_level': 3},
                quiet=True,
                force=True
            )
            try:
                os.chdir(str(self.dir))
                setup(ext_modules=ext_modules,
                      script_args=["build_ext", "--inplace"])
            except Exception as e:
                logger.error(e)
                success = False

            if success:
                for file in python_files_normal:
                    self.clean(Path(file))
                shutil.rmtree(self.dir / 'build')

        return success

    @staticmethod
    def clean(file: Path):
        file.unlink()
        file_c = file.parent / (file.stem + '.c')
        if file_c.exists():
            file_c.unlink()
        rename_so_and_pyd_file(file)


