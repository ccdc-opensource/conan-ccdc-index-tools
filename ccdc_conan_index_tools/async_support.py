import asyncio
import sys
import io
from functools import wraps


def async_command(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if asyncio.get_event_loop().is_running():
            loop = asyncio.new_event_loop()
            # future = loop.create_task()
            return loop.run_until_complete(f(*args, **kwargs))
            # return asyncio.ensure_future(future)
        else:
            return asyncio.run(f(*args, **kwargs))
    return wrapper


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
            if log_file:
                log_file.write(buf)
            if return_stdout:
                output.write(buf)
            await asyncio.sleep(0)

    await asyncio.gather(
        _read_stdout(process.stdout, output),
        _read_stderr(process.stderr, output),
    )
    await process.wait()
    return process.returncode, output.getvalue()
