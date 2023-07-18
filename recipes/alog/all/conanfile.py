from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout
from conan.tools.files import get, copy, collect_libs
from conan.tools.build import check_min_cppstd
import os


class ALogConan(ConanFile):
    name = "alog"
    description = "A high performance, cross platform, log library forked from Mars."
    license = "GNU Public License or the Artistic License"
    homepage = "https://yunxin.163.com/"
    url = "https://gitlab.com/netease-yunxin/yunxin-conan-index"
    topics = ("log", "mars")
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
    }
    short_paths = True

    def validate(self):
        if self.settings.compiler.get_safe("cppstd"):
            check_min_cppstd(self, 11)
        if self.settings.os not in ["Windows", "Macos"]:
            raise ConanInvalidConfiguration(
                f"{self.ref} unsupported platform."
            )
        if self.settings.os == "Windows" and self.settings.arch == "x86":
            raise ConanInvalidConfiguration(
                f"{self.ref} unsupported platform."
            )

    def build(self):
        get(self, **self.conan_data["sources"][self.version][str(self.settings.os)])

    def package(self):
        src_lib_folder = os.path.join(self.build_folder, "lib", str(self.settings.build_type))
        dst_lib_folder = os.path.join(self.package_folder, "lib")
        src_include_folder = os.path.join(self.build_folder, "include")
        dst_include_folder = os.path.join(self.package_folder, "include")
        if self.settings.os == "Windows":
            copy(self, "*.lib", dst=dst_lib_folder, src=src_lib_folder, keep_path=False)
        if self.settings.os == "Macos":
            copy(self, "*.a", dst=dst_lib_folder, src=src_lib_folder, keep_path=False)
        copy(self, "*.h", dst=dst_include_folder, src=src_include_folder)

    def package_info(self):
        self.cpp_info.libdirs = ["lib"]
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.libs = collect_libs(self)
        if self.settings.os == "Macos":
            self.cpp_info.frameworks = ["Foundation"]
