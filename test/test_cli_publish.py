import pathlib
import tempfile
import pytest
from asyncclick.testing import CliRunner
from ccdc_conan_index_tools.commands.publish import publish, package, recipe
from ccdc_conan_index_tools.main import CliContext
from ccdc_conan_index_tools.package_index import PackageIndex
from ccdc_conan_index_tools.conan_commands import get_conan_output

test_path = pathlib.Path(__file__).parent.absolute()
index_for_recipe_publication = PackageIndex(test_path / "index_for_recipe_publication")


@pytest.mark.asyncio
async def test_cli_publish():
    runner = CliRunner()
    result = await runner.invoke(publish, [])
    assert result.exit_code == 0


@pytest.mark.asyncio
async def test_cli_publish_local_recipe_local():
    runner = CliRunner()
    with tempfile.TemporaryDirectory(prefix="cit") as ch:
        result = await runner.invoke(
            recipe,
            ["local-recipe"],
            obj=CliContext(
                index=index_for_recipe_publication,
                conan_user_home=ch,
                conan_logging_level=None,
            ),
        )
        assert result.exit_code == 0
        assert "Publishing local recipe local-recipe/1.75.0@" in result.output
        search_output = await get_conan_output(["search"], conan_user_home=ch)
        print(search_output)
        assert "local-recipe" in search_output
        assert "7zip/19.00" not in search_output


@pytest.mark.asyncio
async def test_cli_publish_remote_recipe():
    runner = CliRunner()
    with tempfile.TemporaryDirectory(prefix="cit") as ch:
        result = await runner.invoke(
            recipe,
            ["7zip", "19.00"],
            obj=CliContext(
                index=index_for_recipe_publication,
                conan_user_home=ch,
                conan_logging_level=None,
            ),
        )
        assert result.exit_code == 0
        assert "Publishing recipe 7zip/19.00@ from conancenter" in result.output
        search_output = await get_conan_output(["search"], conan_user_home=ch)
        print(search_output)
        assert "local-recipe" not in search_output
        assert "7zip/19.00" in search_output


@pytest.mark.asyncio
async def test_cli_publish_all_recipes():
    runner = CliRunner()
    with tempfile.TemporaryDirectory(prefix="cit") as ch:
        result = await runner.invoke(
            recipe,
            [],
            obj=CliContext(
                index=index_for_recipe_publication,
                conan_user_home=ch,
                conan_logging_level=None,
            ),
        )
        assert result.exit_code == 0
        assert "Publishing recipe 7zip/19.00@ from conancenter" in result.output
        assert "Publishing local recipe local-recipe/1.75.0@" in result.output
        search_output = await get_conan_output(["search"], conan_user_home=ch)
        print(search_output)
        assert "local-recipe" in search_output
        assert "7zip/19.00" in search_output


@pytest.mark.asyncio
async def test_cli_publish_local_recipe_remote_repo():
    runner = CliRunner()
    with tempfile.TemporaryDirectory(prefix="cit") as ch:
        result = await runner.invoke(
            recipe,
            ["local-recipe", "--destination-repository", "pr-repo-something"],
            obj=CliContext(
                index=index_for_recipe_publication,
                conan_user_home=ch,
                conan_logging_level=None,
            ),
        )
        assert result.exit_code == 0
        assert result.output == "Publishing local recipe local-recipe/1.75.0@\n"
