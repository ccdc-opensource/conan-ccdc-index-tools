#!/usr/bin/env python
# -*- coding: utf-8 -*-
from conans import ConanFile

class SampleConan(ConanFile):
    name = "local-header-only-recipe-one-version"
    settings = "os"
    no_copy_source = True
