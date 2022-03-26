import pathlib
import pytest
from asyncclick.testing import CliRunner
from ccdc_conan_index_tools.main import cli
from ccdc_conan_index_tools.package_index import PackageIndex

test_path = pathlib.Path(__file__).parent.absolute()
happy_index = PackageIndex(test_path / "happy_index_loading")


@pytest.mark.asyncio
async def test_cli():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = await runner.invoke(cli, [])
        assert result.exit_code == 0


@pytest.mark.asyncio
async def test_cli_with_index():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = await runner.invoke(
            cli,
            ["--index", str((test_path / "happy_index_loading").absolute()), "info"],
        )
        assert result.exit_code == 0


@pytest.mark.asyncio
async def test_cli_with_invalid_index_path():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = await runner.invoke(
            cli, ["--index", str((test_path / "no_such_index").absolute()), "info"]
        )
        assert result.exit_code == 2
        assert "Cannot find a valid package index in" in result.output
