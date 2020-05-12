# -*- coding: utf-8 -*-
import os
from conans import tools, ConanFile, CMake
from conans import __version__ as conan_version
from conans.model.version import Version
from conans.errors import ConanInvalidConfiguration, NotFoundException, ConanException

available_versions = ["3.16.3", "3.16.2", "3.16.1", "3.16.0",
                      "3.15.5", "3.15.4", "3.15.3", "3.15.2", "3.15.1", "3.15.0",
                      "3.14.7", "3.14.6", "3.14.5", "3.14.4", "3.14.3", "3.14.2", "3.14.1", "3.14.0",
                      "3.13.4", "3.13.3", "3.13.2", "3.13.1", "3.13.0",
                      "3.12.4", "3.12.3", "3.12.2", "3.12.1", "3.12.0",
                      "3.11.4", "3.11.3", "3.11.2", "3.11.1", "3.11.0",
                      "3.10.3", "3.10.2", "3.10.1", "3.10.0",
                      "3.9.6", "3.9.5", "3.9.4", "3.9.3", "3.9.2", "3.9.1", "3.9.0",
                      "3.8.2", "3.8.1", "3.8.0",
                      "3.7.2", "3.7.1", "3.7.0",
                      "3.6.3", "3.6.2", "3.6.1", "3.6.0",
                      "3.5.2", "3.5.1", "3.5.0",
                      "3.4.3", "3.4.2", "3.4.1", "3.4.0",
                      "3.3.2", "3.3.1", "3.3.0",
                      "3.2.3", "3.2.2", "3.2.1", "3.2.0",
                      "3.1.3", "3.1.2", "3.1.1", "3.1.0",
                      "3.0.2", "3.0.1", "3.0.0",
                      "2.8.12"]

class CMakeInstallerConan(ConanFile):
    name = "cmake_installer"
    description = "creates cmake binaries package"
    license = "BSD-3-clause"
    url = "https://github.com/conan-community/conan-cmake-installer"
    author = "Conan Community"
    homepage = "https://github.com/Kitware/CMake"
    topics = ("conan", "cmake", "build", "installer")
    settings = "os_build", "arch_build", "compiler", "arch"
    options = {"version": available_versions}
    default_options = {"version": [v for v in available_versions if "-" not in v][0]}
    generators = "cmake"
    exports = "LICENSE"
    exports_sources = "CMakeLists.txt"

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _arch(self):
        return self.settings.get_safe("arch_build") or self.settings.get_safe("arch")

    @property
    def _os(self):
        return self.settings.get_safe("os_build") or self.settings.get_safe("os")

    @property
    def _cmake_version(self):
        if "version" in self.options:
            return str(self.options.version)
        else:
            return self.version

    def _minor_version(self):
        return ".".join(str(self._cmake_version).split(".")[:2])

    def _get_filename(self):
        os_id = {"Macos": "Darwin", "Windows": "win32"}.get(str(self._os),
                                                            str(self._os))
        arch_id = {"x86": "i386"}.get(self._arch, self._arch) if self._os != "Windows" else "x86"
        if self._os == "Linux" and self._cmake_version in ("2.8.12", "3.0.2") and \
           self._arch == "x86_64":
            arch_id = "i386"
        if self._os == "Macos" and self._cmake_version == "2.8.12":
            arch_id = "universal"
        return "cmake-%s-%s-%s" % (self._cmake_version, os_id, arch_id)

    def _get_filename_src(self):
        return "cmake-%s" % self._cmake_version

    def _build_from_source(self):
        return os.path.exists(os.path.join(self.build_folder, self._source_subfolder, "configure"))

    def config_options(self):
        if self.version >= Version("2.8"):  # Means CMake version
            del self.options.version

    def configure(self):
        self.output.warn("[DEPRECATED] Package cmake_installer/{0}@conan/stable is being deprecated. "
                         "Change yours to require cmake/{0} instead".format(self.version))
        if self._os == "Macos" and self._arch == "x86":
            raise ConanInvalidConfiguration("Not supported x86 for OSx")

    def _download_source(self):
        minor = self._minor_version()
        ext = "tar.gz" if not self._os == "Windows" else "zip"
        dest_file = "file.tgz" if self._os != "Windows" else "file.zip"
        unzip_folder = self._get_filename()

        def download_cmake(url, dest_file, unzip_folder):
            self.output.info("Downloading: %s" % url)
            tools.get(url, filename=dest_file, verify=False)
            os.rename(unzip_folder, self._source_subfolder)

        try:
            url = "https://cmake.org/files/v%s/%s.%s" % (minor, self._get_filename(), ext)
            download_cmake(url, dest_file, unzip_folder)
        except NotFoundException:
            if self.settings.get_safe("os_build") == "Windows":
                raise ConanInvalidConfiguration("Building from sources under Windows is not supported")
            url = "https://cmake.org/files/v%s/%s.%s" % (minor, self._get_filename_src(), ext)
            unzip_folder = self._get_filename_src()
            download_cmake(url, dest_file, unzip_folder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["CMAKE_BOOTSTRAP"] = False
        if self.settings.os_build == "Linux":
            cmake.definitions["OPENSSL_USE_STATIC_LIBS"] = True
            cmake.definitions["CMAKE_EXE_LINKER_FLAGS"] = "-lz"
        cmake.configure(source_dir=self._source_subfolder)
        return cmake

    def build(self):
        self._download_source()
        if self._build_from_source():
            if self.settings.os_build == "Linux":
                tools.replace_in_file(os.path.join(self._source_subfolder, "Utilities", "cmcurl", "CMakeLists.txt"),
                                    "list(APPEND CURL_LIBS ${OPENSSL_LIBRARIES})",
                                    "list(APPEND CURL_LIBS ${OPENSSL_LIBRARIES} -ldl -lpthread)")
            self.settings.arch = self.settings.arch_build  # workaround for cross-building to get the correct arch during the build
            cmake = self._configure_cmake()
            cmake.build()

    def package_id(self):
        self.info.include_build_settings()
        if self.settings.os_build == "Windows":
            del self.info.settings.arch_build # same build is used for x86 and x86_64
        del self.info.settings.arch
        del self.info.settings.compiler

    def package(self):
        if self._build_from_source():
            self.copy("Copyright.txt", dst="licenses", src=self._source_subfolder)
            cmake = self._configure_cmake()
            cmake.install()
        else:
            if self._os == "Macos":
                appname = "CMake.app" if self._cmake_version != "2.8.12" else "CMake 2.8-12.app"
                self.copy("*", dst="", src=os.path.join(self._source_subfolder, appname, "Contents"))
            else:
                self.copy("*", dst="", src=self._source_subfolder)
                self.copy("Copyright.txt", dst="licenses", src=os.path.join(self._source_subfolder, "doc", "cmake"))

    def package_info(self):
        if self.package_folder is not None:
            minor = self._minor_version()
            self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
            self.env_info.CMAKE_ROOT = self.package_folder
            mod_path = os.path.join(self.package_folder, "share", "cmake-%s" % minor, "Modules")
            self.env_info.CMAKE_MODULE_PATH = mod_path
            if not os.path.exists(mod_path):
                raise ConanException("Module path not found: %s" % mod_path)
        else:
            self.output.warn("No package folder have been created.")
