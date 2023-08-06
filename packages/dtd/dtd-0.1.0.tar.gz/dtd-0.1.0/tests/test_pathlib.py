import pathlib


def test_ds_store_recognized_without_patch():
    assert pathlib.Path('tests/.DS_Store') in list(pathlib.Path('tests/').iterdir())


def test_ds_store_not_recognized_without_patch():
    import dtd
    dtd.patch_all()
    assert pathlib.Path('tests/.DS_Store') not in list(pathlib.Path('tests/').iterdir())
