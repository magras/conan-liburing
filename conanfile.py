from conan import ConanFile
from conan.tools.gnu import Autotools
from conan.tools.scm import Git


class Liburing(ConanFile):

    name = "liburing"
    version = "2.3"
    license = "MIT"
    homepage = "https://github.com/axboe/liburing"
    description = (
        "liburing provides helpers to setup and teardown io_uring instances, "
        "and also a simplified interface for applications that don't need (or "
        "want) to deal with the full kernel side implementation."
    )

    author = "magras"
    url = "https://github.com/magras/conan-liburing"

    settings = "os", "compiler", "build_type", "arch"
    generators = "AutotoolsToolchain"

    def source(self):
        git = Git(self)
        git.clone(
            f"{self.homepage}.git",
            target=".",
            args=["--depth=1", f"--branch=liburing-{self.version}"]
        )

    def layout(self):
        self.cpp.package.libs = ["uring"]

    def _filter_configure_args(self, autotools):
        """
        Remove flags unrecognized by liburing:
          --bindir --sbindir --oldincludedir
        """

        def is_known_option(arg):
            return arg.startswith((
                "--prefix=",
                "--includedir=",
                "--libdir=",
                "--libdevdir=",
                "--mandir=",
                "--datadir=",
                "--cc=",
                "--cxx=",
                "--nolibc"))

        args = map(lambda a: a.strip("'"), autotools._configure_args.split(" "))
        args = filter(is_known_option, args)
        autotools._configure_args = " ".join(f"'{a}'" for a in args)

    def build(self):
        autotools = Autotools(self)
        self._filter_configure_args(autotools)
        autotools.configure()
        autotools.make()

    def package(self):
        autotools = Autotools(self)
        autotools.install()
