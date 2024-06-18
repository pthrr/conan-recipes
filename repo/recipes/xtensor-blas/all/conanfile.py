from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.tools.files import apply_conandata_patches, export_conandata_patches, get


class xtensor_blasRecipe(ConanFile):
    name = "xtensor-blas"
    package_type = "header-library"
    version = "0.21.0"
    description = "XTENSOR-BLAS: C++ bindings for BLAS with xtensor"
    license = "BSD-3-Clause"
    url = "https://github.com/pthrr/conan-recipes"
    homepage = "https://github.com/xtensor-stack/xtensor-blas"
    topics = ("conan", "xtensor", "blas", "linear-algebra", "tensors", "numpy")
    settings = "os", "compiler", "build_type", "arch"
    requires = "xtensor/0.25.0"
    exports_sources = "CMakeLists.txt"

    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.rm_safe("fPIC")

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def export_sources(self):
        export_conandata_patches(self)

    def source(self):
        get(
            self,
            **self.conan_data["sources"][self.version],
            destination=self.source_folder,
            strip_root=True
        )
        apply_conandata_patches(self)

    def layout(self):
        cmake_layout(self, src_folder="src")

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["xtensor-blas"]
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.set_property("cmake_file_name", "xtensor-blas")
        self.cpp_info.set_property("cmake_target_name", "xtensor-blas")
