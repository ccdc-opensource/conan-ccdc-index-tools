#!/usr/bin/env python
# -*- coding: utf-8 -*-
from conans import ConanFile


class SampleConan(ConanFile):
    name = "local-recipe-build-types-zlib-profile"
    settings = "os"
    no_copy_source = True
