from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout
from conan.tools.files import get, copy
from conan.tools.build import check_min_cppstd
import os


class NetEaseIMConan(ConanFile):
    name = "roomkit"
    description = "NetEase Yunxin roomkit C++ SDK"
    license = "GNU Public License or the Artistic License"
    homepage = "https://yunxin.163.com/"
    url = "https://gitlab.com/netease-yunxin/yunxin-conan-index"
    topics = ("im", "nim", "nertc", "netease im", "netease", "roomkit", "neroom")
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False]
    }
    default_options = {
        "shared": False,
        "fPIC": True
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
                f"{self.ref} unsupported architecture."
            )

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def build(self):
        get(self, **self.conan_data["sources"][self.version][str(self.settings.os)])

    def package(self):
        src_lib_folder = os.path.join(self.build_folder, "lib")
        dst_lib_folder = os.path.join(self.package_folder, "lib")
        src_bin_folder = os.path.join(self.build_folder, "bin")
        dst_bin_folder = os.path.join(self.package_folder, "bin")
        src_include_folder = os.path.join(self.build_folder, "include")
        dst_include_folder = os.path.join(self.package_folder, "include")
        src_res_folder = os.path.join(self.build_folder, "resource")
        dst_res_folder = os.path.join(self.package_folder, "resource")
        if self.settings.os == "Windows":
            copy(self, "necrashpad_handler.exe", dst=dst_bin_folder, src=src_bin_folder)
            copy(self, "h_available.dll", dst=dst_bin_folder, src=src_bin_folder)
            copy(self, "necrashpad.dll", dst=dst_bin_folder, src=src_bin_folder)
            copy(self, "nertc_sdk.dll", dst=dst_bin_folder, src=src_bin_folder)
            copy(self, "NERtcAiDenoise.dll", dst=dst_bin_folder, src=src_bin_folder)
            copy(self, "NERtcAiHowling.dll", dst=dst_bin_folder, src=src_bin_folder)
            copy(self, "NERtcAudio3D.dll", dst=dst_bin_folder, src=src_bin_folder)
            copy(self, "NERtcBeauty.dll", dst=dst_bin_folder, src=src_bin_folder)
            copy(self, "NERtcFaceDetect.dll", dst=dst_bin_folder, src=src_bin_folder)
            copy(self, "NERtcFaceEnhance.dll", dst=dst_bin_folder, src=src_bin_folder)
            copy(self, "NERtcnn.dll", dst=dst_bin_folder, src=src_bin_folder)
            copy(self, "NERtcPersonSegment.dll", dst=dst_bin_folder, src=src_bin_folder)
            copy(self, "NERtcScreenShareEnhance.dll", dst=dst_bin_folder, src=src_bin_folder)
            copy(self, "NERtcSuperResolution.dll", dst=dst_bin_folder, src=src_bin_folder)
            copy(self, "NERtcVideoDenoise.dll", dst=dst_bin_folder, src=src_bin_folder)
            copy(self, "nim_chatroom.dll", dst=dst_bin_folder, src=src_bin_folder)
            copy(self, "nim.dll", dst=dst_bin_folder, src=src_bin_folder)
            copy(self, "protoopp.dll", dst=dst_bin_folder, src=src_bin_folder)
            if self.settings.build_type == "Debug":
                copy(self, "roomkitd.dll", dst=dst_bin_folder, src=src_bin_folder)
                copy(self, "roomkitd.lib", dst=dst_lib_folder, src=src_lib_folder)
            else:
                copy(self, "roomkit.dll", dst=dst_bin_folder, src=src_bin_folder)
                copy(self, "roomkit.lib", dst=dst_lib_folder, src=src_lib_folder)

        if self.settings.os == "Macos":
            copy(self, "libh_available.dylib", dst=dst_lib_folder, src=src_lib_folder)
            copy(self, "libnim_chatroom.dylib", dst=dst_lib_folder, src=src_lib_folder)
            copy(self, "libnim.dylib", dst=dst_lib_folder, src=src_lib_folder)
            if self.settings.build_type == "Debug":
                copy(self, "libroomkitd.dylib", dst=dst_lib_folder, src=src_lib_folder)
            else:
                copy(self, "libroomkit.dylib", dst=dst_lib_folder, src=src_lib_folder)
            copy(self, "*.framework/*", dst=dst_lib_folder, src=src_lib_folder)
        copy(self, "*.h", dst=dst_include_folder, src=src_include_folder)
        copy(self, "*", dst=dst_res_folder, src=src_res_folder)

    def package_info(self):
        self.cpp_info.libdirs = ["lib"]
        self.cpp_info.includedirs = ["include", "include/nertc"]
        library_postfix = ""
        if self.settings.build_type == "Debug":
            library_postfix = "d"
        self.cpp_info.libs.append("roomkit{}".format(library_postfix))
