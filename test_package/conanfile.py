import StringIO
import conans


class ConanFileInst(conans.ConanFile):

    def build(self):
        pass

    def test(self):
        output = StringIO.StringIO()
        self.run("cmake --version", output=output)
        assert(str(self.options["cmake_installer"].version) in str(output.getvalue()))
        self.output.info("Installed: %s" % str(output.getvalue()))
