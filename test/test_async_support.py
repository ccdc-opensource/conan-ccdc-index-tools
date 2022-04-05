import io
import sys
import ccdc_conan_index_tools.async_support
import pytest

script = 'import sys; print("out1"); print(""); print("err1", file=sys.stderr); print("out2"); print("", file=sys.stderr); print("err2", file=sys.stderr);'
script_with_exit = script + "sys.exit(12)"


@pytest.mark.asyncio
async def test_run_external_command_default():
    (retcode, output) = await ccdc_conan_index_tools.async_support.run_external_command(
        [sys.executable, "-c", script]
    )
    assert retcode == 0
    assert output == "out1\n\nout2\n"


@pytest.mark.asyncio
async def test_run_external_command_error_code():
    (retcode, output) = await ccdc_conan_index_tools.async_support.run_external_command(
        [sys.executable, "-c", script_with_exit]
    )
    assert retcode == 12
    assert output == "out1\n\nout2\n"


@pytest.mark.asyncio
async def test_run_external_command_additional_output_file():
    additional_output = io.StringIO("")

    (retcode, output) = await ccdc_conan_index_tools.async_support.run_external_command(
        [sys.executable, "-c", script], log_file=additional_output
    )
    assert retcode == 0
    assert output == "out1\n\nout2\n"

    additional_output = additional_output.getvalue()
    assert "err1\n" in additional_output
    assert "err2\n" in additional_output
    assert "out1\n" in additional_output
    assert "out2\n" in additional_output


@pytest.mark.asyncio
async def test_run_external_command_return_err_in_output():
    (retcode, output) = await ccdc_conan_index_tools.async_support.run_external_command(
        [sys.executable, "-c", script], return_stderr=True
    )
    assert retcode == 0
    assert "err1\n" in output
    assert "err2\n" in output
    assert "out1\n" in output
    assert "out2\n" in output


@pytest.mark.asyncio
async def test_run_external_command_return_only_err_in_output():
    (retcode, output) = await ccdc_conan_index_tools.async_support.run_external_command(
        [sys.executable, "-c", script], return_stdout=False, return_stderr=True
    )
    assert retcode == 0
    assert output == "err1\n\nerr2\n"


@pytest.mark.asyncio
async def test_run_external_command_print_to_output(capsys):
    print("--- expect some output here ----")
    (retcode, output) = await ccdc_conan_index_tools.async_support.run_external_command(
        [sys.executable, "-c", script],
        log_to_console=True,
    )
    assert retcode == 0
    assert output == "out1\n\nout2\n"
    print("--- end of expected output ----")
    captured = capsys.readouterr()
    assert "out1\n" in captured.out
    assert "out2\n" in captured.out
    assert "err1\n" in captured.err
    assert "err2\n" in captured.err
