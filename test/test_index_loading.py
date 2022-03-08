import os
from ccdc_conan_index_tools.package_index import PackageIndex

happy_index_dir = os.path.join(os.path.dirname(__file__), "happy_index_loading")


def test_happy_index_loading():
    happy_idx = PackageIndex(happy_index_dir)
    assert happy_idx.directory == happy_index_dir
    assert happy_idx.is_valid
    assert os.path.isfile(happy_idx.defaults_file)
    assert os.path.isdir(happy_idx.recipes_directory)
    assert happy_idx.package_names == ["local-pkg1", "sample1", "sample2"]
    sample1defs = happy_idx.definitions_for("sample1")
    assert sample1defs is not None
    assert sample1defs.name == "sample1"

    local1defs = happy_idx.definitions_for("local-pkg1")
    assert local1defs is not None
    assert local1defs.name == "local-pkg1"

    assert happy_idx.definitions_for("ignored_dir") is None
    assert happy_idx.definitions_for("ignored") is None
