# -*- coding: utf-8 -*-
import os
import platform

from conan.packager import ConanMultiPackager

available_versions = ["3.14.3", "3.14.2", "3.14.1", "3.14.0",
                      "3.13.4", "3.13.3", "3.13.2", "3.13.1", "3.13.0",
                      "3.12.4", "3.12.3", "3.12.2", "3.12.1", "3.12.0",
                      "3.11.3", "3.11.2", "3.11.1",
                      "3.10.0",
                      "3.9.0",
                      "3.8.2", "3.8.1", "3.8.0",
                      "3.7.2", "3.7.1", "3.7.0",
                      "3.6.3", "3.6.2", "3.6.1", "3.6.0",
                      "3.5.2",
                      "3.4.3",
                      "3.3.2",
                      "3.2.3",
                      "3.1.3",
                      "3.0.2",
                      "2.8.12"]

if __name__ == "__main__":
    arch = os.environ["CONAN_ARCHS"]
    builder = ConanMultiPackager()

    for version in available_versions:
        # New mode, with version field
        builder.add({"os" : build_shared.get_os(), "arch_build" : arch, "arch": arch}, {}, {}, {}, reference="cmake_installer/%s" % version)
        # Old mode, version as an option
        builder.add({"os" : build_shared.get_os(), "arch_build" : arch, "arch": arch}, {"cmake_installer:version": version}, {}, {}, reference="cmake_installer/1.0")

    builder.run()
