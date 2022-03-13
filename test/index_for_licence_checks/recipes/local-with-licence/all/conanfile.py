#!/usr/bin/env python
# -*- coding: utf-8 -*-
from conans import ConanFile


class SampleConan(ConanFile):
    name = "local-recipe-with-licence"
    settings = "os"
    no_copy_source = True
    license = "Apache-2.0"
