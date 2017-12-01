import os
from conans import tools, ConanFile

available_versions = ["3.9.0", "3.8.2", "3.8.1", "3.8.0",
                      "3.7.2", "3.7.1", "3.7.0", "3.6.3",
                      "3.6.2", "3.6.1", "3.6.0", "3.5.2",
                      "3.4.3", "3.3.2", "3.2.3", "3.1.3",
                      "3.0.2", "2.8.12"]


class CMakeInstallerConan(ConanFile):
    name = "cmake_installer"
    description = "creates cmake binaries package"
    version = "1.0"
    license = "OSI-approved BSD 3-clause"
    url = "http://github.com/lasote/conan-cmake-installer"
    settings = {"os": ["Windows", "Linux", "Macos"],
                "arch": ["x86", "x86_64"]}
    options = {"version": available_versions}
    default_options = "version=3.9.0"
    build_policy = "missing"

    def configure(self):
        if self.settings.os == "Macos" and self.settings.arch == "x86":
            raise Exception("Not supported x86 for OSx")

    def get_filename(self):
        arch = str(self.settings.arch)
        os_id = {"Macos": "Darwin", "Windows": "win32"}.get(str(self.settings.os),
                                                            str(self.settings.os))
        arch_id = {"x86": "i386"}.get(arch, arch) if self.settings.os != "Windows" else "x86"
        if self.settings.os == "Linux" and self.options.version in ("2.8.12", "3.0.2") and \
           self.settings.arch == "x86_64":
            arch_id = "i386"
        if self.settings.os == "Macos" and self.options.version == "2.8.12":
            arch_id = "universal"
        return "cmake-%s-%s-%s" % (self.options.version, os_id, arch_id)

    def build(self):
        minor = str(self.options.version)[0:3]
        ext = "tar.gz" if not self.settings.os == "Windows" else "zip"
        url = "https://cmake.org/files/v%s/%s.%s" % (minor, self.get_filename(), ext)

        # https://cmake.org/files/v3.6/cmake-3.6.0-Linux-i386.tar.gz
        # https://cmake.org/files/v3.6/cmake-3.6.0-Darwin-x86_64.tar.gz
        # https://cmake.org/files/v3.5/cmake-3.5.2-win32-x86.zip

        dest_file = "file.tgz" if self.settings.os != "Windows" else "file.zip"
        self.output.info("Downloading: %s" % url)
        tools.download(url, dest_file, verify=False)
        tools.unzip(dest_file)

    def package(self):
        if self.settings.os == "Macos":
            self.copy("*", dst="", src=os.path.join(self.get_filename(), "CMake.app", "Contents"))
        else:
            self.copy("*", dst="", src=self.get_filename())

    def package_info(self):
        if self.package_folder is not None:
            self.env_info.path.append(os.path.join(self.package_folder, "bin"))
            self.env_info.CMAKE_ROOT = self.package_folder
            mod_path = os.path.join(self.package_folder, "share", "cmake-%s" % str(self.options.version)[0:3],
                                    "Modules")
            self.env_info.CMAKE_MODULE_PATH = mod_path
            if not os.path.exists(mod_path):
                raise Exception("Module path not found: %s" % mod_path)
