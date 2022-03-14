import subprocess
import shutil
from .build_definition import PackageBuildDefinitions


class ConanCommandException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def conan_command():
    return shutil.which("conan")


def get_conan_output(command_args, conan_user_home=None, conan_logging_level=None):
    env = {
        "NO_COLOR": "1",
        "CONAN_NON_INTERACTIVE": "1",
    }
    if conan_user_home:
        env["CONAN_USER_HOME"] = conan_user_home
    if conan_logging_level:
        env["CONAN_LOGGING_LEVEL"] = conan_logging_level

    ret = subprocess.run(
        args=[conan_command()] + command_args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        env=env,
    )
    if ret.returncode != 0:
        raise ConanCommandException(
            f"Conan command {conan_command()} [{command_args}] returned {ret.returncode}\nStdout: {ret.stdout}\nStderr: {ret.stderr}"
        )
    return ret.stdout


def get_remote_package_licence(
    package, version, remote, conan_user_home=None, conan_logging_level=None
):
    ret = get_conan_output(
        ["inspect", "-r", remote, "-a", "license", f"{package}/{version}@"],
        conan_user_home=conan_user_home,
        conan_logging_level=conan_logging_level,
    )
    lines = [line for line in ret.splitlines() if "license: " in line]
    if not lines:
        return f"No License line in conan info for {package}/{version}@"
    return lines[0].replace("license: ", "")


def get_local_package_licence(
    conanfile_directory,
    conan_user_home=None,
    conan_logging_level=None,
):
    ret = get_conan_output(
        ["inspect", "-a", "license", conanfile_directory],
        conan_user_home=conan_user_home,
        conan_logging_level=conan_logging_level,
    )
    lines = [line for line in ret.splitlines() if "license: " in line]
    if not lines:
        return f"No license line in conan info for conanfile in {conanfile_directory}"
    return lines[0].replace("license: ", "")


def publish_local_recipe(
    conanfile_directory,
    package_name,
    package_version,
    conan_user_home=None,
    conan_logging_level=None,
):
    return get_conan_output(
        ["export", conanfile_directory, f"{package_name}/{package_version}@"],
        conan_user_home=conan_user_home,
        conan_logging_level=conan_logging_level,
    )


def publish_remote_recipe(
    package_name,
    package_version,
    source_repository,
    conan_user_home=None,
    conan_logging_level=None,
):
    return get_conan_output(
        [
            "download",
            f"{package_name}/{package_version}@",
            f"--remote={ source_repository }",
            "--recipe",
        ],
        conan_user_home=conan_user_home,
        conan_logging_level=conan_logging_level,
    )


def build_all_locally(
    definitions: PackageBuildDefinitions,
    versions: list,
    build_types: list,
    platform_combinations: list,
):
    for version in versions:
        for platform_combination in platform_combinations:
            for build_type in build_types:
                build_locally(
                    definitions=definitions,
                    version=version,
                    build_type=build_type,
                    combination=platform_combination,
                )


def build_locally(
    definitions: PackageBuildDefinitions,
    version: str,
    build_type: str,
    combination: str,
):
    pass
