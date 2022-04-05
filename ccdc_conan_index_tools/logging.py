import os
from contextlib import contextmanager


def is_running_under_teamcity():
    return "TEAMCITY_VERSION" in os.environ


def is_running_under_gha():
    return "GITHUB_ACTIONS" in os.environ


def is_running_under_azure_pipelines():
    return "TF_BUILD" in os.environ


@contextmanager
def log_section(name):
    if is_running_under_teamcity():
        print(f"##teamcity[blockOpened name='{name}']")
    elif is_running_under_gha():
        print(f"::group::{name}")
    elif is_running_under_azure_pipelines():
        print(f"##[group]{name}")
    else:
        print(f"==START=== {name} =========")
    try:
        yield
    finally:
        if is_running_under_teamcity():
            print(f"##teamcity[blockClosed name='{name}']")
        elif is_running_under_gha():
            print(f"::endgroup::")
        elif is_running_under_azure_pipelines():
            print(f"##[endgroup]")
        else:
            print(f"==END===== {name} =========\n\n\n")
