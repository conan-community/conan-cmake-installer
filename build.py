import platform

from conan.packager import ConanMultiPackager

available_versions = ["3.10.0", "3.9.0", "3.8.2",
                      "3.8.1", "3.8.0", "3.7.2", "3.7.1",
                      "3.7.0", "3.6.3", "3.6.2", "3.6.1",
                      "3.6.0", "3.5.2", "3.4.3", "3.3.2",
                      "3.2.3", "3.1.3", "3.0.2", "2.8.12"]

if __name__ == "__main__":

    # New mode, with version field
    for version in available_versions:
        builder = ConanMultiPackager(reference="cmake_installer/%s" % version)
        # Unknown problem with 3.0.2 on travis
        if version > "3.0.2" or platform.system() == "Windows":
            builder.add({}, {}, {}, {})
            builder.run()

    # Old mode, with options
    builder = ConanMultiPackager(reference="cmake_installer/1.0")
    for version in available_versions:
        # Unknown problem with 3.0.2 on travis
        if version > "3.0.2" or platform.system() == "Windows":
            builder.add({}, {"cmake_installer:version": version}, {}, {})
    builder.run()

