#!/usr/bin/env python
#
# Copyright (C) 2015 Analog Devices, Inc.
# Author: Paul Cercueil <paul.cercueil@analog.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.

import sys

if sys.version_info[0] < 3:
    from distutils.core import setup
    from distutils.command.install import install

    config = dict()
else:
    from setuptools import setup
    from setuptools.command.install import install

    config = dict(long_description_content_type="text/markdown")

description = "Library for interfacing with Linux IIO devices"

try:
    with open("/tmp/libiio-push/bindings/python/README.md", "r") as fh:
        long_description = fh.read()
except:
    long_description = description


def find_recursive(folder, filename):
    import os

    for root, dirs, files in os.walk(folder):
        for file in files:
            if file == filename:
                return os.path.join(root, file)


class InstallWrapper(install):
    """Before installing we check if the
    libiio library is actually installed"""

    def run(self):
        self._check_libiio_installed()
        # Run the standard PyPi copy
        install.run(self)

    def _check_libiio_installed(self):
        from platform import system as _system
        from ctypes import CDLL as _cdll
        from ctypes.util import find_library

        if "Windows" in _system():
            _iiolib = "libiio.dll"
        else:
            # Non-windows, possibly Posix system
            _iiolib = "iio"
        try:
            import os

            destdir = os.getenv("DESTDIR", "")
            if destdir:
                destdir = os.path.join("/tmp/libiio-push/build", destdir)
                fulllibpath = find_recursive(destdir, "libiio.so")
                _lib = _cdll(fulllibpath, use_errno=True, use_last_error=True)
            else:
                _lib = _cdll(find_library(_iiolib), use_errno=True, use_last_error=True)
            if not _lib._name:
                raise OSError
        except OSError:
            msg = "The libiio library could not be found.\n\
            libiio needs to be installed first before the python bindings.\n\
            The latest release can be found on GitHub:\n\
            https://github.com/analogdevicesinc/libiio/releases"
            raise Exception(msg)


config.update(
    dict(
        name="pylibiio",
        version="0.21",
        maintainer="Analog Devices, Inc",
        maintainer_email="travis.collins@analog.com",
        description=description,
        long_description=long_description,
        url="https://github.com/analogdevicesinc/libiio",
        py_modules=["iio"],
        cmdclass={"install": InstallWrapper},
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
            "Operating System :: OS Independent",
        ],
    )
)


setup(**config)
