import subprocess
import conans

class ConanFileInst(conans.ConanFile):
    name = "cmake_installer_test"
    requires = "cmake_installer/0.1@demo/test_package"

    def build(self):
        pass

    def test(self):
        try:
            subprocess.check_output("cmake --version")
        except FileNotFoundError as e:
            self.output.error("%s package test failed" % self.name)
        else:
            self.output.success("%s package test passed" % self.name)
