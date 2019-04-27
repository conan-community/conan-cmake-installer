# -*- coding: utf-8 -*-
import os
from six import StringIO
from conans import ConanFile


class ConanFileInst(ConanFile):

    def build(self):
        pass

    def test(self):
        output = StringIO()
        cmake_path = os.path.join(self.deps_cpp_info["cmake_installer"].rootpath, "bin", "cmake")
        self.run("{} --version".format(cmake_path), output=output, run_environment=True)
        self.output.info("Installed: %s" % str(output.getvalue()))
        if self.requires["cmake_installer"].ref.version != "1.0":
            ver = str(self.requires["cmake_installer"].ref.version)
        else:
            ver = str(self.options["cmake_installer"].version)

        value = str(output.getvalue())
        cmake_version = value.split('\n')[0]
        self.output.info("Expected value: {}".format(ver))
        self.output.info("Detected value: {}".format(cmake_version))
        assert(ver in cmake_version)
