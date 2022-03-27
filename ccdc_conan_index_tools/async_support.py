import asyncio
import sys
import io
from functools import wraps


async def run_external_command(
    args,
    cwd=None,
    env=None,
    log_file=None,
    log_to_console=False,
    return_stdout=True,
    return_stderr=False,
):
    process = await asyncio.create_subprocess_exec(
        *args,
        cwd=cwd,
        env=env,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    output = io.StringIO("")

    async def _read_stderr(stderr, output):
        while True:
            buf = await stderr.readline()
            if not buf:
                break
            buf = buf.decode(errors="replace")
            if log_to_console:
                sys.stderr.write(buf)
                sys.stderr.flush()
            if log_file:
                log_file.write(buf)
            if return_stderr:
                output.write(buf)
            await asyncio.sleep(0)

    async def _read_stdout(stdout, output):
        while True:
            buf = await stdout.readline()
            if not buf:
                break
            buf = buf.decode(errors="replace")
            if log_to_console:
                sys.stdout.write(buf)
                sys.stdout.flush()
            if log_file:
                log_file.write(buf)
            if return_stdout:
                output.write(buf)
            await asyncio.sleep(0)

    await asyncio.gather(
        _read_stdout(process.stdout, output),
        _read_stderr(process.stderr, output),
    )
    await asyncio.wait([process.wait()])
    return process.returncode, output.getvalue()
