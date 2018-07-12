import os
from conans import tools, ConanFile
from conans import __version__ as conan_version
from conans.model.version import Version
from conans.errors import ConanException, NotFoundException

available_versions = ["3.11.3", "3.11.2", "3.11.1", "3.10.0", "3.9.0", "3.8.2",
                      "3.8.1", "3.8.0", "3.7.2", "3.7.1",
                      "3.7.0", "3.6.3", "3.6.2", "3.6.1",
                      "3.6.0", "3.5.2", "3.4.3", "3.3.2",
                      "3.2.3", "3.1.3", "3.0.2", "2.8.12"]


class CMakeInstallerConan(ConanFile):
    name = "cmake_installer"
    description = "creates cmake binaries package"
    license = "OSI-approved BSD 3-clause"
    url = "http://github.com/lasote/conan-cmake-installer"
    if conan_version < Version("1.0.0"):
        settings = {"os": ["Windows", "Linux", "Macos"],
                    "arch": ["x86", "x86_64"]}
    else:
        settings = "os_build", "arch_build"
    options = {"version": available_versions}
    default_options = "version=" + [v for v in available_versions if "-" not in v][0]
    build_policy = "missing"

    def minor_version(self):
        return ".".join(str(self.cmake_version).split(".")[:2])

    def config_options(self):
        if self.version >= Version("2.8"):  # Means CMake version
            self.options.remove("version")

    def configure(self):
        if self.os == "Macos" and self.arch == "x86":
            raise Exception("Not supported x86 for OSx")

    @property
    def arch(self):
        return self.settings.get_safe("arch_build") or self.settings.get_safe("arch")

    @property
    def os(self):
        return self.settings.get_safe("os_build") or self.settings.get_safe("os")

    @property
    def cmake_version(self):
        if "version" in self.options:
            return str(self.options.version)
        else:
            return self.version

    def get_filename(self):
        os_id = {"Macos": "Darwin", "Windows": "win32"}.get(str(self.os),
                                                            str(self.os))
        arch_id = {"x86": "i386"}.get(self.arch, self.arch) if self.os != "Windows" else "x86"
        if self.os == "Linux" and self.cmake_version in ("2.8.12", "3.0.2") and \
           self.arch == "x86_64":
            arch_id = "i386"
        if self.os == "Macos" and self.cmake_version == "2.8.12":
            arch_id = "universal"
        return "cmake-%s-%s-%s" % (self.cmake_version, os_id, arch_id)

    def get_filename_src(self):
        return "cmake-%s" % self.cmake_version

    def build(self):
        minor = self.minor_version()
        ext = "tar.gz" if not self.os == "Windows" else "zip"
        dest_file = "file.tgz" if self.os != "Windows" else "file.zip"
        try:
            url = "https://cmake.org/files/v%s/%s.%s" % (minor, self.get_filename(), ext)

            # https://cmake.org/files/v3.6/cmake-3.6.0-Linux-i386.tar.gz
            # https://cmake.org/files/v3.6/cmake-3.6.0-Darwin-x86_64.tar.gz
            # https://cmake.org/files/v3.5/cmake-3.5.2-win32-x86.zip

            self.output.info("Downloading: %s" % url)
            tools.download(url, dest_file, verify=False)
            tools.unzip(dest_file)
        except NotFoundException:
            if self.settings.get_safe("os_build") == "Windows":
                raise ConanException("Building from sources under Windows is not supported")

            url = "https://cmake.org/files/v%s/%s.%s" % (minor, self.get_filename_src(), ext)

            # https://cmake.org/files/v3.6/cmake-3.6.0.tar.gz

            self.output.info("Downloading: %s" % url)
            tools.download(url, dest_file, verify=False)
            tools.unzip(dest_file)

            with tools.chdir(self.get_filename_src()):
                self.run("./bootstrap --prefix=%s" % os.path.join(self.build_folder, self.get_filename()))
                self.run("make")
                self.run("make install")

    def package(self):
        if self.os == "Macos":
            appname = "CMake.app" if self.version != "2.8.12" else "CMake 2.8-12.app"
            self.copy("*", dst="", src=os.path.join(self.get_filename(), appname, "Contents"))
        else:
            self.copy("*", dst="", src=self.get_filename())

    def package_info(self):
        if self.package_folder is not None:
            minor = self.minor_version()
            self.env_info.path.append(os.path.join(self.package_folder, "bin"))
            self.env_info.CMAKE_ROOT = self.package_folder
            mod_path = os.path.join(self.package_folder, "share", "cmake-%s" % minor, "Modules")
            self.env_info.CMAKE_MODULE_PATH = mod_path
            if not os.path.exists(mod_path):
                raise Exception("Module path not found: %s" % mod_path)
