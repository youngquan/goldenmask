from pathlib import Path
from click.testing import CliRunner
from goldenmask.cli import goldenmask
from goldenmask import GOLDENMASK, GOLDENMASK_INFO


def test_compile_one_file(tmp_path: Path):
    file_py = tmp_path / "a.py"
    file_py.write_text("print('This is file a')")
    runner = CliRunner()
    result = runner.invoke(goldenmask, [str(file_py)])
    assert result.exit_code == 0
    file_pyc = file_py.parent / GOLDENMASK / (file_py.name + 'c')
    assert file_pyc.exists()
    assert len(list(tmp_path.iterdir())) == 2
    assert len(list((tmp_path / GOLDENMASK).iterdir())) == 2
    file_py_cleaned = file_py.parent / GOLDENMASK / file_py.name
    assert not file_py_cleaned.exists()


def test_compile_one_file_and_inplace(tmp_path: Path):
    file_py = tmp_path / "a.py"
    file_py.write_text("print('This is file a')")
    runner = CliRunner()
    result = runner.invoke(goldenmask, ['-i', str(file_py)])
    assert result.exit_code == 0
    file_pyc = Path(str(file_py) + 'c')
    assert len(list(tmp_path.iterdir())) == 2
    assert file_pyc.exists()
    assert not file_py.exists()


def test_compile_one_dir(tmp_path):
    file_num = 2
    for i in range(file_num):
        file = tmp_path / (str(i) + '.py')
        file.write_text(f"print('This is content from file {i}')")

    runner = CliRunner()
    result = runner.invoke(goldenmask, [str(tmp_path)])
    assert result.exit_code == 0
    
    for i in range(file_num):
        file_pyc = tmp_path / GOLDENMASK / (str(i) + '.pyc')
        assert file_pyc.exists()
        file_py = tmp_path / GOLDENMASK / (str(i) + '.py')
        assert not file_py.exists()

    assert len(list((tmp_path / GOLDENMASK).iterdir())) == file_num + 1


def test_compile_one_dir_and_inplace(tmp_path):
    file_num = 2
    for i in range(file_num):
        file = tmp_path / (str(i) + '.py')
        file.write_text(f"print('This is content from file {i}')")

    runner = CliRunner()
    result = runner.invoke(goldenmask, ['-i', str(tmp_path)])
    assert result.exit_code == 0
    for i in range(file_num):
        file_pyc = tmp_path / (str(i) + '.pyc')
        assert file_pyc.exists()
        file_py = tmp_path / (str(i) + '.py')
        assert not file_py.exists()

    assert len(list(tmp_path.iterdir())) == file_num + 1


def test_compile_one_wheel_package(shared_datadir: Path):
    wheel_file = shared_datadir / 'goldenmask-0.1.2-py3-none-any.whl'
    runner = CliRunner()
    result = runner.invoke(goldenmask, [str(wheel_file)])
    assert result.exit_code == 0
    result_file = wheel_file.parent / GOLDENMASK / wheel_file.name
    assert result_file.exists()
    assert (result_file.parent / GOLDENMASK_INFO).exists()


def test_compile_one_wheel_package_inplace(shared_datadir: Path):
    wheel_file = shared_datadir / 'goldenmask-0.1.2-py3-none-any.whl'
    runner = CliRunner()
    result = runner.invoke(goldenmask, ['--inplace', str(wheel_file)])
    assert result.exit_code == 0
    result_file = wheel_file
    assert result_file.exists()
    assert (result_file.parent / GOLDENMASK_INFO).exists()


def test_compile_one_source_package(shared_datadir: Path):
    wheel_file = shared_datadir / 'goldenmask-0.1.2.tar.gz'
    runner = CliRunner()
    result = runner.invoke(goldenmask, [str(wheel_file)])
    assert result.exit_code == 0
    result_file = wheel_file.parent / GOLDENMASK / wheel_file.name
    assert result_file.exists()
    assert (result_file.parent / GOLDENMASK_INFO).exists()


def test_compile_one_source_package_inplace(shared_datadir: Path):
    wheel_file = shared_datadir / 'goldenmask-0.1.2.tar.gz'
    runner = CliRunner()
    result = runner.invoke(goldenmask, ['--inplace', str(wheel_file)])
    assert result.exit_code == 0
    result_file = wheel_file
    assert result_file.exists()
    assert (result_file.parent / GOLDENMASK_INFO).exists()
