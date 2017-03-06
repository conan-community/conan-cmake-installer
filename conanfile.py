from conans import ConanFile, CMake, tools
import os


class CMakeInstallerConan(ConanFile):
    name = "cmake_installer"
    version = "0.1"
    license = "MIT"
    url = "http://github.com/lasote/conan-cmake-installer"
    settings = {"os": ["Windows", "Linux", "Macos"], "arch": ["x86", "x86_64"]}
    options = {"version": ["3.6.2", "3.6.1", "3.6.0", "3.5.2", "3.4.3", "3.3.2", 
                           "3.2.3", "3.1.3", "3.0.2", "2.8.12"]}
    default_options = "version=3.6.0"
    build_policy = "missing"
    
    
    def config(self):
        if self.settings.os == "Macos" and self.settings.arch == "x86":
            raise Exception("Not supported x86 for OSx")

    def get_filename(self):
        os = {"Macos": "Darwin", "Windows": "win32"}.get(str(self.settings.os), str(self.settings.os))
        arch = {"x86": "i386"}.get(str(self.settings.arch), 
                                   str(self.settings.arch)) if self.settings.os != "Windows" else "x86"
        if self.settings.os == "Linux" and self.options.version in ("2.8.12", "3.0.2") and self.settings.arch == "x86_64":
            arch = "i386"
        return "cmake-%s-%s-%s" % (self.options.version, os, arch)
    
    def build(self):
        keychain = "%s_%s_%s" % (self.settings.os,
                                 self.settings.arch,
                                 str(self.options.version))
        minor = str(self.options.version)[0:3]
        ext = "tar.gz" if not self.settings.os == "Windows" else "zip"
        url = "https://cmake.org/files/v%s/%s.%s" % (minor, self.get_filename(), ext)

#       https://cmake.org/files/v3.6/cmake-3.6.0-Linux-i386.tar.gz
#       https://cmake.org/files/v3.6/cmake-3.6.0-Darwin-x86_64.tar.gz
#       https://cmake.org/files/v3.5/cmake-3.5.2-win32-x86.zip

        dest_file = "file.tgz" if self.settings.os != "Windows" else "file.zip"
        self.output.warn("Downloading: %s" % url)
        tools.download(url, dest_file, verify=False)
        tools.unzip(dest_file)
    
    def package(self):
        if self.settings.os == "Macos":
            self.copy("*", dst="", src=os.path.join(self.get_filename(), "CMake.app", "Contents"))
        else:
            self.copy("*", dst="", src=self.get_filename())

    def package_info(self):
        self.env_info.path.append(os.path.join(self.package_folder, "bin"))
