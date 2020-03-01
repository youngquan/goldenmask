from pathlib import Path

from goldenmask.utils import pack, unpack


def test_unpack_and_pack_wheel_file_inplace(shared_datadir: Path):
    wheel_file = shared_datadir / "goldenmask-0.1.2-py3-none-any.whl"
    unpacked_dir = unpack(wheel_file)
    assert unpacked_dir
    assert len(list(unpacked_dir.iterdir())) == 2
    packed_file = pack(unpacked_dir, wheel_file, inplace=True)
    assert packed_file == wheel_file
    unpacked_dir_again = unpack(packed_file)
    # packed_file.unlink()
    assert set(child.name for child in unpacked_dir.iterdir()) == set(
        child.name for child in unpacked_dir_again.iterdir()
    )


def test_unpack_and_pack_gztar_file_inplace(shared_datadir: Path):
    gztar_file = shared_datadir / "goldenmask-0.1.2.tar.gz"
    unpacked_dir = unpack(gztar_file)
    assert unpacked_dir
    assert len(list(unpacked_dir.iterdir())) == 1
    packed_file = pack(unpacked_dir, gztar_file, inplace=True)
    assert packed_file == gztar_file
    unpacked_dir_again = unpack(packed_file)
    # packed_file.unlink()
    assert set(child.name for child in unpacked_dir.iterdir()) == set(
        child.name for child in unpacked_dir_again.iterdir()
    )
