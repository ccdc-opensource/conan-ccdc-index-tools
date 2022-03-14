import os
import click
from typing import Dict, List
from .build_definition import PackageBuildDefinitions


class PackageIndex:
    def __init__(self, index_dir):
        self._index_dir = index_dir
        self._names = None
        if not os.path.isdir(self.recipes_directory):
            raise FileNotFoundError(f"Missing {self.recipes_directory}")

    @property
    def is_valid(self):
        return (
            os.path.isdir(self.directory)
            and os.path.isfile(self.defaults_file)
            and os.path.isdir(self.recipes_directory)
        )

    @property
    def directory(self):
        return self._index_dir

    @property
    def defaults_file(self):
        return os.path.join(self._index_dir, "index-defaults.yml")

    @property
    def recipes_directory(self):
        return os.path.join(self._index_dir, "recipes")

    @property
    def package_names(self):
        if self._names:
            return self._names
        self._names = []
        for f in os.listdir(self.recipes_directory):
            if f.endswith(".yml"):
                self._names.append(f.replace(".yml", ""))
            if os.path.isdir(
                os.path.join(self.recipes_directory, f)
            ) and os.path.isfile(os.path.join(self.recipes_directory, f, "config.yml")):
                self._names.append(f)
        self._names = sorted(self._names)
        return self._names

    def definitions_for(self, pkg):
        yml_file = os.path.join(self.recipes_directory, f"{pkg}.yml")
        local_config_yml_file = os.path.join(self.recipes_directory, pkg, "config.yml")
        if os.path.isfile(yml_file):
            try:
                return PackageBuildDefinitions.from_yaml(
                    self.defaults_file, self.recipes_directory, f"{pkg}.yml"
                )
            except Exception as e:
                click.echo(e, err=True)
                raise Exception(f"Cannot read package definition in {yml_file}")
        if os.path.isfile(local_config_yml_file):
            return PackageBuildDefinitions.from_local_recipe_directory(
                self.defaults_file, os.path.join(self.recipes_directory, pkg)
            )
        return None
