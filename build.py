import platform

from conan.packager import ConanMultiPackager

available_versions = ["3.9.0", "3.8.2", "3.7.2", "3.6.3",
                      "3.5.2", "3.4.3", "3.3.2", "3.2.3", "3.1.3", "3.0.2",
                      "2.8.12"]

if __name__ == "__main__":
    builder = ConanMultiPackager()
    for version in available_versions:
        # Unknown problem with 3.0.2 on travis
        if version <= "3.0.2" or platform.system() != "Linux":
            builder.add({}, {"cmake_installer:version": version}, {}, {})
    builder.run()
