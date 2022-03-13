import pathlib
from click.testing import CliRunner
from ccdc_conan_index_tools.commands.info import info, package, licence
from ccdc_conan_index_tools.main import CliContext

test_path = pathlib.Path(__file__).parent.absolute()


def test_cli_info():
    runner = CliRunner()
    result = runner.invoke(info, [])
    assert result.exit_code == 0


def test_cli_info_package_yaml():
    runner = CliRunner()
    result = runner.invoke(
        package,
        ["--format", "yaml"],
        obj=CliContext(index=test_path / "happy_index_loading"),
    )
    assert result.exit_code == 0
    assert result.output == "- local-pkg1\n- sample1\n- sample2\n\n"
    # yaml is default
    result = runner.invoke(
        package, [], obj=CliContext(index=test_path / "happy_index_loading")
    )
    assert result.exit_code == 0
    assert result.output == "- local-pkg1\n- sample1\n- sample2\n\n"


def test_cli_info_package_json():
    runner = CliRunner()
    result = runner.invoke(
        package,
        ["--format", "json"],
        obj=CliContext(index=test_path / "happy_index_loading"),
    )
    assert result.exit_code == 0
    assert result.output == '["local-pkg1", "sample1", "sample2"]\n'


def test_cli_info_licence():
    runner = CliRunner()
    result = runner.invoke(
        licence,
        ["--format", "yaml"],
        obj=CliContext(index=test_path / "index_for_licence_checks"),
    )
    assert result.exit_code == 0
    assert (
        result.output
        == "7zip/19.00: ('LGPL-2.1', 'BSD-3-Clause', 'Unrar')\nlocal-with-licence/1.75.0: Apache-2.0\nno-licence/1.75.0: None\n\n"
    )


def test_cli_info_licence_specific():
    runner = CliRunner()
    result = runner.invoke(
        licence,
        ["local-with-licence"],
        obj=CliContext(index=test_path / "index_for_licence_checks"),
    )
    assert result.exit_code == 0
    assert result.output == "local-with-licence/1.75.0: Apache-2.0\n\n"


def test_cli_info_licence_specific_not_in_index():
    runner = CliRunner()
    result = runner.invoke(
        licence,
        ["unknown-package"],
        obj=CliContext(index=test_path / "index_for_licence_checks"),
    )
    assert result.exit_code == 2
    assert "Error: unknown-package is not in the index" in result.output


def test_cli_info_licence_json():
    runner = CliRunner()
    result = runner.invoke(
        licence,
        ["--format", "json"],
        obj=CliContext(index=test_path / "index_for_licence_checks"),
    )
    assert result.exit_code == 0
    assert (
        result.output
        == """{"7zip/19.00": "('LGPL-2.1', 'BSD-3-Clause', 'Unrar')", "local-with-licence/1.75.0": "Apache-2.0", "no-licence/1.75.0": "None"}\n"""
    )
