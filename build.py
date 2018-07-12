import os
import platform

from conan.packager import ConanMultiPackager

available_versions = ["3.11.3", "3.11.2", "3.11.1", "3.10.0", "3.9.0", "3.8.2",
                      "3.8.1", "3.8.0", "3.7.2", "3.7.1",
                      "3.7.0", "3.6.3", "3.6.2", "3.6.1",
                      "3.6.0", "3.5.2", "3.4.3", "3.3.2",
                      "3.2.3", "3.1.3", "3.0.2", "2.8.12"]

if __name__ == "__main__":

    builder = ConanMultiPackager()

    i386 = "CONAN_DOCKER_IMAGE" in os.environ and \
        os.environ["CONAN_DOCKER_IMAGE"].endswith("i386")

    # New mode, with version field
    for version in available_versions:
        # Unknown problem with 3.0.2 on travis
        # Building from sources takes much time so build the very recent 32bit version only
        if (version > "3.0.2" and not i386) or platform.system() == "Windows" or \
                version == available_versions[0]:
            builder.add({}, {}, {}, {}, reference="cmake_installer/%s" % version)

    # Old mode, with options
    for version in available_versions:
        # Unknown problem with 3.0.2 on travis
        # Building from sources takes much time so build the very recent 32bit version only
        if (version > "3.0.2" and not i386) or platform.system() == "Windows" or \
                version == available_versions[0]:
            builder.add({}, {"cmake_installer:version": version}, {}, {}, "cmake_installer/1.0")

    builder.run()
