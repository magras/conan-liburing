from conans import ConanFile, AutoToolsBuildEnvironment


class Liburing(ConanFile):

    name = "liburing"
    version = "0.6"
    license = "MIT"
    homepage = "https://github.com/axboe/liburing"
    description = (
        "liburing provides helpers to setup and teardown io_uring instances, "
        "and also a simplified interface for applications that don't need (or "
        "want) to deal with the full kernel side implementation."
    )

    author = "magras"
    url = "https://github.com/magras/conan-liburing"

    generators = "pkg_config"
    settings = "os", "compiler", "build_type", "arch"
    scm = {
        "type": "git",
        "url": "{}.git".format(homepage),
        "revision": "liburing-{}".format(version)
    }

    _autotools = None

    def _configure_autotools(self):
        if not self._autotools:
            self._autotools = AutoToolsBuildEnvironment(self)
            self._autotools.configure()
        return self._autotools

    def build(self):
        autotools = self._configure_autotools()
        autotools.make()

    def package(self):
        autotools = self._configure_autotools()
        autotools.install()

    def package_info(self):
        self.cpp_info.libs = ["liburing.so"]
