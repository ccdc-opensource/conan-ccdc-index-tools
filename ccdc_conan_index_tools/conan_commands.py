import subprocess
import shutil


class ConanCommandException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def conan_command():
    return shutil.which("conan")


def get_conan_output(command_args):
    ret = subprocess.run(
        args=[conan_command()] + command_args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    if ret.returncode != 0:
        raise ConanCommandException(
            f"Conan command {conan_command()} [{command_args}] returned {ret.returncode}\nStdout: {ret.stdout}\nStderr: {ret.stderr}"
        )
    return ret.stdout


def get_remote_package_licence(package, version, remote):
    ret = get_conan_output(
        ["inspect", "-r", remote, "-a", "license", f"{package}/{version}@"]
    )
    lines = [line for line in ret.splitlines() if "license: " in line]
    if not lines:
        return f"No License line in conan info for {package}/{version}@"
    return lines[0].replace("license: ", "")


def get_local_package_licence(conanfile_directory):
    ret = get_conan_output(["inspect", "-a", "license", conanfile_directory])
    lines = [line for line in ret.splitlines() if "license: " in line]
    if not lines:
        return f"No license line in conan info for conanfile in {conanfile_directory}"
    return lines[0].replace("license: ", "")
