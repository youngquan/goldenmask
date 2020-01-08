from pathlib import Path
from click.testing import CliRunner
from goldenmask.cli import goldenmask


def test_compile_one_file(tmp_path):
    file_py = tmp_path / "a.py"
    file_py.write_text("print('This is file a')")
    runner = CliRunner()
    result = runner.invoke(goldenmask, [str(file_py)])
    assert result.exit_code == 0
    file_pyc = Path(str(file_py) + 'c')
    assert file_pyc.exists()
    assert file_py.exists()


def test_compile_one_file_and_replace(tmp_path):
    file_py = tmp_path / "a.py"
    file_py.write_text("print('This is file a')")
    runner = CliRunner()
    result = runner.invoke(goldenmask, ['-r', str(file_py)])
    assert result.exit_code == 0
    file_pyc = Path(str(file_py) + 'c')
    assert file_pyc.exists()
    print(file_py.exists())
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
        file_pyc = tmp_path / (str(i) + '.pyc')
        assert file_pyc.exists()
        file_py = tmp_path / (str(i) + '.py')
        assert file_py.exists()


def test_compile_one_dir_and_replace(tmp_path):
    file_num = 2
    for i in range(file_num):
        file = tmp_path / (str(i) + '.py')
        file.write_text(f"print('This is content from file {i}')")

    print(tmp_path)
    print(tmp_path.exists())
    runner = CliRunner()
    result = runner.invoke(goldenmask, ['-r', str(tmp_path)])
    assert result.exit_code == 0
    print(tmp_path)
    print(tmp_path.exists())
    
    for i in range(file_num):
        file_pyc = tmp_path / (str(i) + '.pyc')
        assert file_pyc.exists()
        file_py = tmp_path / (str(i) + '.py')
        assert not file_py.exists()