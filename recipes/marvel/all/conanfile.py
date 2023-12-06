from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout
from conan.tools.files import apply_conandata_patches, copy, export_conandata_patches, get, rmdir, save, collect_libs, check_sha256
from conan.tools.microsoft import is_msvc, check_min_vs
from conan.tools.scm import Version, Git
import os
import textwrap

required_conan_version = ">=1.53.0"


class MarvelConan(ConanFile):
    name = "marvel"
    description = "NetEase marvel."
    license = "MIT"
    url = "https://gitlab.com/netease-yunxin/yunxin-conan-index"
    homepage = "https://yunxin.163.com/"
    topics = ("marvel", "carshpad")
    package_type = "library"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
    }

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def layout(self):
        cmake_layout(self)

    def build(self):
        os = str(self.settings.os)
        get(self, **self.conan_data["sources"][self.version]
            [os], strip_root=True if os == "Windows" else False)

    def package(self):
        if self.settings.os == 'Macos':
            copy(self, "*", dst=self.package_folder, src=self.build_folder)
        else:
            bin_folder = os.path.join(self.build_folder, "bin")
            copy(self, "*.h", dst=os.path.join(self.package_folder, "include"),
                 src=os.path.join(self.build_folder, "include"), keep_path=False)
            copy(self, "*.*", dst=os.path.join(self.package_folder, "bin"), src=os.path.join(bin_folder,
                 "Win32" if self.settings.arch == "x86" else "x64"), keep_path=False)

    def package_info(self):
        if self.settings.os == "Macos":
            self.cpp_info.frameworkdirs.append(self.package_folder)
            self.cpp_info.includedirs = ["Marvel.framework/Headers"]
            self.cpp_info.frameworks.append("Marvel")
        else:
            self.cpp_info.libdirs = ["lib"]
            self.cpp_info.includedirs = ["include"]
        self.cpp_info.libs = collect_libs(self)
