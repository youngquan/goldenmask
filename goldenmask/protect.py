import compileall
import os
import shutil
from pathlib import Path
# from distutils.core import setup
from setuptools import setup
from Cython.Build import cythonize
from Cython.Compiler import Options

from goldenmask import logger
from goldenmask.utils import is_file, remove_python_files, virtualenv_folder, is_entrypoint, rename_so_and_pyd_file

Options.docstrings = False


class BaseProtector:
    def __init__(self, file_or_dir, inplace):
        self.file_or_dir = Path(file_or_dir)
        self.is_file = is_file(file_or_dir)
        if self.is_file:
            if inplace:
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
            self.dir = Path(file_or_dir) / '__goldenmask__'
            if self.dir.exists():
                shutil.rmtree(self.dir)
            shutil.copytree(self.file_or_dir, self.dir, ignore=virtualenv_folder)
            self.build_temp = self.dir / 'build-goldenmask'
            self.info_file = self.dir / '.goldenmask'


class CompileallProtector(BaseProtector):

    def __init__(self, file_or_dir, inplace=False):
        super().__init__(file_or_dir, inplace)

    def protect(self):
        if self.is_file:
            success = compileall.compile_file(self.file, force=True, legacy=True, optimize=2, quiet=1)
            if success:
                os.remove(self.file)
            else:
                return success
        else:
            success = compileall.compile_dir(self.dir, force=True, legacy=True, optimize=2, quiet=1,
                                             workers=os.cpu_count())
            if success:
                remove_python_files(self.dir)
            else:
                return success
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
                setup(ext_modules=ext_modules, script_args=["build_ext", "--inplace", "-t", self.build_temp])
            except Exception as e:
                success = False
                pass
            if success:
                self.clean(self.file)
                shutil.rmtree(self.build_temp)
            return success
        else:
            # normal means python files except files like (double underline files、setup.py、manage.py、setup.py etc)
            python_files_normal = []
            python_files_abnormal = []
            for file in Path(self.dir).rglob('*.py'):
                if ((file.name.startswith('__') and file.name.endswith('__')) or
                        is_entrypoint(file) or
                        file.name == 'setup.py'):
                    python_files_abnormal.append(str(file))
                else:
                    python_files_normal.append(file)
            ext_modules = cythonize(
                python_files_normal,
                compiler_directives={'language_level': 3},
                quiet=True,
                force=True
            )
            try:
                setup(ext_modules=ext_modules,
                      script_args=["build_ext", "--inplace", "-t", self.build_temp, "-j", os.cpu_count()])
            except Exception as e:
                success = False
                pass
            if success:
                for file in python_files_abnormal:
                    protector = CompileallProtector(file)
                    success = protector.protect()
                    if not success:
                        break

            if success:
                for file in Path(self.dir).rglob('*.py'):
                    self.clean(file)
                shutil.rmtree(self.build_temp)
        return success

    @staticmethod
    def clean(file: Path):
        file.unlink()
        (file.parent / file.stem / '.c').unlink()
        rename_so_and_pyd_file(file)

