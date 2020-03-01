import subprocess
import sys
from pathlib import Path

project_code_dir = "goldenmask"
bin_path = Path(sys.executable).parent

isort_cmd = (
    f"{bin_path / 'isort'} --recursive  --force-single-line-imports "
    f"--thirdparty {project_code_dir} --apply {project_code_dir} tests scripts"
)
subprocess.run(isort_cmd, shell=True, check=True)

autoflake_cmd = (
    f"{bin_path / 'autoflake'} --remove-all-unused-imports --recursive --remove-unused-variables "
    f"--in-place {project_code_dir} tests scripts --exclude=__init__.py"
)
subprocess.run(autoflake_cmd, shell=True, check=True)

black_cmd = f"{bin_path / 'black'} {project_code_dir} tests scripts"
subprocess.run(black_cmd, shell=True, check=True)

isort_cmd = (
    f"{bin_path / 'isort'} --multi-line=3 --trailing-comma --force-grid-wrap=0 --combine-as --line-width 88 "
    f"--recursive --thirdparty {project_code_dir} --apply {project_code_dir} tests scripts"
)
subprocess.run(isort_cmd, shell=True, check=True)
