import pathlib
import tempfile
import pytest
from asyncclick.testing import CliRunner
from ccdc_conan_index_tools.commands.info import info, package, licence
from ccdc_conan_index_tools.main import CliContext
from ccdc_conan_index_tools.package_index import PackageIndex

test_path = pathlib.Path(__file__).parent.absolute()
happy_index = PackageIndex(test_path / "happy_index_loading")
index_for_licence_checks = PackageIndex(test_path / "index_for_licence_checks")


@pytest.mark.asyncio
async def test_cli_info():
    runner = CliRunner()
    result = await runner.invoke(info, [])
    assert result.exit_code == 0


@pytest.mark.asyncio
async def test_cli_info_package_yaml():
    runner = CliRunner()
    result = await runner.invoke(
        package,
        ["--format", "yaml"],
        obj=CliContext(
            index=happy_index, conan_logging_level=None, conan_user_home=None
        ),
    )
    assert result.exit_code == 0
    assert result.output == "- local-pkg1\n- sample1\n- sample2\n\n"
    # yaml is default
    result = await runner.invoke(
        package,
        [],
        obj=CliContext(
            index=happy_index, conan_logging_level=None, conan_user_home=None
        ),
    )
    assert result.exit_code == 0
    assert result.output == "- local-pkg1\n- sample1\n- sample2\n\n"


@pytest.mark.asyncio
async def test_cli_info_package_json():
    runner = CliRunner()
    result = await runner.invoke(
        package,
        ["--format", "json"],
        obj=CliContext(
            index=happy_index, conan_logging_level=None, conan_user_home=None
        ),
    )
    assert result.exit_code == 0
    assert result.output == '["local-pkg1", "sample1", "sample2"]\n'


@pytest.mark.asyncio
async def test_cli_info_licence():
    with tempfile.TemporaryDirectory(prefix="cit") as ch:
        runner = CliRunner()
        result = await runner.invoke(
            licence,
            ["--format", "yaml"],
            obj=CliContext(
                index=index_for_licence_checks,
                conan_logging_level=None,
                conan_user_home=ch,
            ),
        )
        assert result.exit_code == 0
        assert (
            result.output
            == "7zip/19.00: ('LGPL-2.1', 'BSD-3-Clause', 'Unrar')\nlocal-with-licence/1.75.0: Apache-2.0\nno-licence/1.75.0: None\n"
        )


@pytest.mark.asyncio
async def test_cli_info_licence_specific():
    with tempfile.TemporaryDirectory(prefix="cit") as ch:
        runner = CliRunner()
        result = await runner.invoke(
            licence,
            ["local-with-licence"],
            obj=CliContext(
                index=index_for_licence_checks,
                conan_logging_level=None,
                conan_user_home=ch,
            ),
        )
        assert result.exit_code == 0
        assert result.output == "local-with-licence/1.75.0: Apache-2.0\n"


@pytest.mark.asyncio
async def test_cli_info_licence_specific_not_in_index():
    with tempfile.TemporaryDirectory(prefix="cit") as ch:
        runner = CliRunner()
        result = await runner.invoke(
            licence,
            ["unknown-package"],
            obj=CliContext(
                index=index_for_licence_checks,
                conan_logging_level=None,
                conan_user_home=ch,
            ),
        )
        assert result.exit_code == 2
        assert "Error: unknown-package is not in the index" in result.output


@pytest.mark.asyncio
async def test_cli_info_licence_json():
    with tempfile.TemporaryDirectory(prefix="cit") as ch:
        runner = CliRunner()
        result = await runner.invoke(
            licence,
            ["--format", "json"],
            obj=CliContext(
                index=index_for_licence_checks,
                conan_logging_level=None,
                conan_user_home=ch,
            ),
        )
        assert result.exit_code == 0
        assert (
            result.output
            == """{"7zip/19.00": "('LGPL-2.1', 'BSD-3-Clause', 'Unrar')", "local-with-licence/1.75.0": "Apache-2.0", "no-licence/1.75.0": "None"}\n"""
        )
