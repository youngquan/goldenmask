import shutil
from pathlib import Path
from click.testing import CliRunner
from goldenmask.cli import goldenmask
from goldenmask import GOLDENMASK, GOLDENMASK_INFO


def test_compile_one_file(tmp_path: Path, suffix_so_or_pyd):
    file_py: Path = tmp_path / "a.py"
    file_py.write_text("""def a():\n    print('This is file a')\n""")
    runner = CliRunner()
    result = runner.invoke(goldenmask, ['-l', 2, str(file_py)])
    assert result.exit_code == 0
    file_so_or_pyd = file_py.parent / GOLDENMASK / (file_py.stem + suffix_so_or_pyd)
    assert file_so_or_pyd.exists()
    assert len(list(tmp_path.iterdir())) == 2
    assert len(list((tmp_path / GOLDENMASK).iterdir())) == 2
    file_py_cleaned = file_py.parent / GOLDENMASK / file_py.name
    assert not file_py_cleaned.exists()


def test_compile_one_file_and_inplace(tmp_path: Path, suffix_so_or_pyd):
    file_py = tmp_path / "a.py"
    file_py.write_text("def a():\n    print('This is file a')\n")
    runner = CliRunner()
    result = runner.invoke(goldenmask, ['-l', 2, '--inplace', str(file_py)])
    assert result.exit_code == 0
    file_so_or_pyd = tmp_path / (file_py.stem + suffix_so_or_pyd)
    assert file_so_or_pyd.exists()
    assert len(list(tmp_path.iterdir())) == 2
    assert not file_py.exists()


def test_compile_one_dir(tmp_path):
    # shutil.copytree(shared_datadir / 'demo-project', tmp_path / 'demo-project')
    # print(str(shared_datadir / 'demo-project'))
    # print(list((shared_datadir / 'demo-project').iterdir()))
    src = 'E:\\projects\\goldenmask\\tests\\data\\demo-project'
    # des = tmp_path / 'demo-project'
    # des = Path('data/demo-project')
    # shutil.copytree(src, des)
    runner = CliRunner()
    result = runner.invoke(goldenmask, ['-l', 2, src], color=True)
    print(result.output)
    assert result.exit_code == 0


# def test_compile_one_dir(tmp_path, shared_datadir):
#     # shutil.copytree(shared_datadir / 'demo-project', tmp_path / 'demo-project')
#     # print(str(shared_datadir / 'demo-project'))
#     # print(list((shared_datadir / 'demo-project').iterdir()))
#     src = 'E:\\projects\\goldenmask\\tests\\data\\demo-project'
#     des = tmp_path / 'demo-project'
#     shutil.copytree(src, des)
#     runner = CliRunner(charset='gbk')
#     result = runner.invoke(goldenmask, ['-l', 2, str(des)], color=True)
#     assert result.exit_code == 0
#     print(result.output)
#
#
# def test_compile_one_dir_and_inplace(tmp_path):
#     file_num = 2
#     for i in range(file_num):
#         file = tmp_path / (str(i) + '.py')
#         file.write_text(f"print('This is content from file {i}')")
#
#     runner = CliRunner()
#     result = runner.invoke(goldenmask, ['-i', str(tmp_path)])
#     assert result.exit_code == 0
#     for i in range(file_num):
#         file_pyc = tmp_path / (str(i) + '.pyc')
#         assert file_pyc.exists()
#         file_py = tmp_path / (str(i) + '.py')
#         assert not file_py.exists()


def test_compile_one_wheel_package(shared_datadir: Path):
    wheel_file = shared_datadir / 'goldenmask-0.1.2-py3-none-any.whl'
    runner = CliRunner()
    result = runner.invoke(goldenmask, ['-l', 2, str(wheel_file)])
    assert result.exit_code == 0
    result_file = wheel_file.parent / GOLDENMASK / wheel_file.name
    assert result_file.exists()
    assert (result_file.parent / GOLDENMASK_INFO).exists()


def test_compile_one_wheel_package_inplace(shared_datadir: Path):
    wheel_file = shared_datadir / 'goldenmask-0.1.2-py3-none-any.whl'
    runner = CliRunner()
    result = runner.invoke(goldenmask, ['--inplace', '-l', 2, str(wheel_file)])
    assert result.exit_code == 0
    result_file = wheel_file
    assert result_file.exists()
    assert (result_file.parent / GOLDENMASK_INFO).exists()


def test_compile_one_source_package(shared_datadir: Path):
    wheel_file = shared_datadir / 'goldenmask-0.1.2.tar.gz'
    runner = CliRunner()
    result = runner.invoke(goldenmask, ['-l', 2, str(wheel_file)])
    assert result.exit_code == 0
    result_file = wheel_file.parent / GOLDENMASK / wheel_file.name
    assert result_file.exists()
    assert (result_file.parent / GOLDENMASK_INFO).exists()


def test_compile_one_source_package_inplace(shared_datadir: Path):
    wheel_file = shared_datadir / 'goldenmask-0.1.2.tar.gz'
    runner = CliRunner()
    result = runner.invoke(goldenmask, ['--inplace', '-l', 2, str(wheel_file)])
    assert result.exit_code == 0
    result_file = wheel_file
    assert result_file.exists()
    assert (result_file.parent / GOLDENMASK_INFO).exists()
