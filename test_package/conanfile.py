# -*- coding: utf-8 -*-
from six import StringIO
from conans import ConanFile


class ConanFileInst(ConanFile):

    def build(self):
        pass

    def test(self):
        output = StringIO()
        self.run("cmake --version", output=output, run_environment=True)
        self.output.info("Installed: %s" % str(output.getvalue()))
        if self.requires["cmake_installer"].ref.version != "1.0":
            ver = str(self.requires["cmake_installer"].ref.version)
        else:
            ver = str(self.options["cmake_installer"].version)


        value = str(output.getvalue())
        self.output.info(value)
        self.output.info(ver)
        assert(ver in value)
