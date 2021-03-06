from conans import ConanFile, CMake, tools


class HelloConan(ConanFile):
    name = "Hello"
    version = "0.1"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Hello here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    requires = "gstreamer/1.0@user/testing3"

    def source(self):
        #self.run("git clone https://github.com/memsharded/hello.git")
        #self.run("cd hello && git checkout static_shared")
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        #tools.replace_in_file("hello/CMakeLists.txt", "PROJECT(MyHello)",
        #                      '''PROJECT(MyHello)
        # #include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
        # #conan_basic_setup()''')
        pass

    def build(self):
        #cmake = CMake(self)
        #cmake.configure(source_folder="hello")
        #cmake.build()
        print self.deps_cpp_info["gstreamer"].rootpath
        args = '--define-variable gstreamer_root=%s' %self.deps_cpp_info["gstreamer"].rootpath
        pkgconfig_exec = 'pkg-config ' + args
        vars = {'PKG_CONFIG' : pkgconfig_exec,
                'PKG_CONFIG_PATH' : "%s/lib/pkgconfig/"%(self.deps_cpp_info["gstreamer"].rootpath)
        }

        with tools.environment_append(vars):
            self.run('pkg-config %s gstreamer-1.0 --libs --cflags' %(args) )
        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        pass
        #self.copy("*.h", dst="include", src="hello")
        #self.copy("*hello.lib", dst="lib", keep_path=False)
        #self.copy("*.dll", dst="bin", keep_path=False)
        #self.copy("*.so", dst="lib", keep_path=False)
        #self.copy("*.dylib", dst="lib", keep_path=False)
        #self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["hello"]

