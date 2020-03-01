import compileall
import multiprocessing
import os
import shutil
import sys
from distutils.core import setup
from pathlib import Path

from Cython.Build import cythonize
from Cython.Compiler import Options
from goldenmask import GOLDENMASK, logger
from goldenmask.exceptions import NoPythonFiles
from goldenmask.utils import (
    Ignore,
    get_file_type,
    is_entrypoint,
    pack,
    remove_python_files,
    rename_so_and_pyd_file,
    unpack,
)

Options.docstrings = False


class BaseProtector:
    def __init__(self, source_path: str, inplace: bool, no_smart: bool) -> None:
        self.source_path = Path(source_path)
        self.is_pyfile, self.is_wheel, self.is_tarball, self.is_dir = get_file_type(
            str(self.source_path)
        )
        if not self.is_dir:
            if not any((self.is_pyfile, self.is_wheel, self.is_tarball)):
                logger.error(
                    f"This {self.source_path} can not be protect now! "
                    f"Only files end with '.py', '.tar.gz' or '.whl' can be protect!"
                )
                sys.exit()
        self.inplace = inplace
        self.no_smart = no_smart

        if self.is_pyfile:
            if self.inplace:
                self.file = self.source_path
            else:
                self.file = (
                    self.source_path.parent / "__goldenmask__" / self.source_path.name
                )
                if self.file.exists():
                    os.remove(self.file)
                else:
                    try:
                        self.file.parent.mkdir()
                    except FileExistsError:
                        pass
                shutil.copy(self.source_path, self.file)
            self.info_file = self.file.parent / ".goldenmask"
            self.build_temp = self.file.parent / "build-goldenmask"
        elif self.is_dir:
            if self.inplace:
                self.dir = self.source_path
            else:
                self.dir = Path(source_path) / "__goldenmask__"
                if self.dir.exists():
                    # TODO: may be I should try to speed !
                    shutil.rmtree(self.dir)
                if self.no_smart:
                    shutil.copytree(self.source_path, self.dir)
                else:
                    shutil.copytree(
                        self.source_path, self.dir, ignore=Ignore(self.dir).copy
                    )
            self.info_file = self.dir / ".goldenmask"
            self.build_temp = self.dir / "build-goldenmask"
        else:

            tmp_directory = unpack(self.source_path)
            if self.is_wheel:
                self.dir = tmp_directory
            if self.is_tarball:
                self.dir = list(tmp_directory.iterdir())[0]
            self.no_smart = True
            if self.inplace:
                self.info_file = self.source_path.parent / ".goldenmask"
            else:
                self.info_file = self.source_path.parent / GOLDENMASK / ".goldenmask"
            self.build_temp = self.dir / "build-goldenmask"


class CompileallProtector(BaseProtector):
    def __init__(
        self, source_path: str, inplace: bool = False, no_smart: bool = False
    ) -> None:
        super().__init__(source_path, inplace, no_smart)

    def protect(self):
        if self.is_pyfile:
            success = compileall.compile_file(
                self.file, force=True, legacy=True, optimize=2, quiet=1
            )
            if success:
                os.remove(self.file)
        else:
            if self.is_dir:
                # Below is needed, because when the option inplace is not true, virtual env folder has already
                # been ignored when pasting them.
                if self.inplace and not self.no_smart:
                    rx = Ignore(self.dir)
                else:
                    rx = None
            else:
                rx = None

            success = compileall.compile_dir(
                self.dir,
                force=True,
                legacy=True,
                optimize=2,
                quiet=1,
                rx=rx,
                workers=os.cpu_count(),
            )
            if success:
                remove_python_files(self.dir)

            if self.is_wheel or self.is_tarball:
                _ = pack(self.dir, self.source_path, self.inplace)
                shutil.rmtree(self.dir, ignore_errors=True)
        return success


class CythonProtector(BaseProtector):
    def __init__(
        self, source_path: str, inplace: bool = False, no_smart: bool = False
    ) -> None:
        super().__init__(source_path, inplace, no_smart)

    def protect(self):
        success = False
        if self.is_pyfile:
            success = True
            ext_modules = cythonize(
                str(self.file), compiler_directives={"language_level": 3}
            )
            try:
                setup(
                    ext_modules=ext_modules,
                    script_args=[
                        "build_ext",
                        "-b",
                        str(self.file.parent),
                        "-t",
                        str(self.build_temp),
                    ],
                )
            except Exception as e:
                logger.warning(
                    f"Can not build file {self.file} using Cython, we will try to use Compileall!"
                )
                logger.warning(e)
                protector = CompileallProtector(self.file, inplace=True)
                success = protector.protect()
            if success:
                self.clean(self.file)
                shutil.rmtree(self.build_temp)
            return success
        else:
            python_files_normal = []
            for file in Path(self.dir).rglob("*.py"):
                if Ignore(self.dir).search(str(file)) and not self.no_smart:
                    continue
                # TODO: It seems that there are many files that can not be compiled using Cython.
                if (
                    (file.stem.startswith("__") and file.stem.endswith("__"))
                    or is_entrypoint(file)
                    or file.name == "setup.py"
                ):
                    protector = CompileallProtector(str(file), inplace=True)
                    success = protector.protect()
                    if not success:
                        break
                else:
                    python_files_normal.append(str(file))

            if not python_files_normal:
                logger.error(
                    f"There is no python files to build using Cython in folder {self.dir}"
                )
                raise NoPythonFiles()
            ext_modules = cythonize(
                python_files_normal,
                compiler_directives={"language_level": 3},
                quiet=True,
                force=True,
                nthreads=multiprocessing.cpu_count(),
            )
            try:
                setup(
                    ext_modules=ext_modules,
                    script_args=[
                        "build_ext",
                        "-b",
                        str(self.dir),
                        "-t",
                        str(self.build_temp),
                    ],
                )
            except Exception as e:
                logger.error(e)
                success = False

            if success:
                for file in python_files_normal:
                    self.clean(Path(file))
                shutil.rmtree(self.build_temp)

            if self.is_wheel or self.is_tarball:
                _ = pack(self.dir, self.source_path, self.inplace)
                shutil.rmtree(self.dir, ignore_errors=True)

        return success

    @staticmethod
    def clean(file: Path):
        file.unlink()
        file_c = file.with_suffix(".c")
        if file_c.exists():
            file_c.unlink()
        rename_so_and_pyd_file(file)
