import os
import subprocess
import shutil
import stat
from multiprocessing import Process

def rm_mkdir_cd(directory):
    # if the build directory exists, delete it
    if os.path.isdir(directory):
        shutil.rmtree(directory, ignore_errors=True)

    # create and move into the build directory
    os.makedirs(directory)
    os.chdir(directory)

def compile_cmake_project(
        project_directory,
        build_directory="build",
        cmake_generator="Visual Studio 15 2017",
        architecture=None,
        cmake_flags=None,
        cmake_build_type="Release",
        target="ALL_BUILD"):

    # move into the project build directory
    os.chdir(project_directory)
    rm_mkdir_cd(build_directory)

    # configure with CMake
    if architecture is not None:
        cmake_generator += " " + architecture
    command = ["cmake", "..", "-G" + cmake_generator]
    if cmake_flags is not None:
        command += cmake_flags
    subprocess.run(command)

    # build with CMake
    subprocess.run(["cmake", "--build", ".", "--config", cmake_build_type, "--target", target])
    subprocess.run(["cmake", "--build", ".", "--config", cmake_build_type, "--target", target])

def compile_openfast(openfast_directory, cmake_generator="Visual Studio 15 2017"):
    # compile OpenFAST in all build types and precisions as a statically linked executable
    p32 = Process(
        target=compile_cmake_project,
        args=(openfast_directory,),
        kwargs={
            "build_directory": "build32",
            "cmake_generator": cmake_generator,
            "cmake_flags": ["-DDOUBLE_PRECISION=OFF"]
        }
    )
    p64 = Process(
        target=compile_cmake_project,
        args=(openfast_directory,),
        kwargs={
            "build_directory": "build64",
            "cmake_generator": cmake_generator,
            "architecture": "Win64",
            "cmake_flags": ["-DDOUBLE_PRECISION=OFF"]
        }
    )
    p64_double = Process(
        target=compile_cmake_project,
        args=(openfast_directory,),
        kwargs={
            "build_directory": "build64_double",
            "cmake_generator": cmake_generator,
            "architecture": "Win64",
        }
    )
    p32.start()
    p64.start()
    p64_double.start()
    p32.join()
    p64.join()
    p64_double.join()

def compile_maplib(openfast_directory, cmake_generator="Visual Studio 15 2017"):
    # reconfigure cmake with dynamic linking and compile the map dll
    compile_cmake_project(
        openfast_directory,
        build_directory="build32",
        cmake_generator=cmake_generator,
        cmake_flags=["-DDOUBLE_PRECISION=OFF", "-DBUILD_SHARED_LIBS=ON"],
        target="mapcpplib"
    )
    compile_cmake_project(
        openfast_directory,
        build_directory="build64",
        cmake_generator=cmake_generator,
        architecture="Win64",
        cmake_flags=["-DDOUBLE_PRECISION=OFF", "-DBUILD_SHARED_LIBS=ON"],
        target="mapcpplib"
    )

def compile_discon(discon_directory, cmake_generator="Visual Studio 15 2017"):
    p32 = Process(
        target=compile_cmake_project,
        args=(discon_directory,),
        kwargs={
            "build_directory":"build32",
            "cmake_generator": cmake_generator
        }
    )
    p64 = Process(
        target=compile_cmake_project,
        args=(discon_directory,),
        kwargs={
            "build_directory":"build64",
            "cmake_generator": cmake_generator,
            "architecture":"Win64",
        }
    )
    p32.start()
    p64.start()
    p32.join()
    p64.join()

def package_openfast(openfast_directory, target_directory, cmake_build_type="Release"):
    os.chdir(target_directory)
    shutil.copyfile(
        os.path.join(openfast_directory, "build32", "glue-codes", "openfast", cmake_build_type, "openfast.exe"), 
        os.path.join("openfast_Win32.exe")
    )
    shutil.copyfile(
        os.path.join(openfast_directory, "build64", "glue-codes", "openfast", cmake_build_type, "openfast.exe"), 
        os.path.join("openfast_x64.exe")
    )
    shutil.copyfile(
        os.path.join(openfast_directory, "build64_double", "glue-codes", "openfast", cmake_build_type, "openfast.exe"), 
        os.path.join("openfast_x64_Double.exe")
    )

def package_maplib(openfast_directory, target_directory, cmake_build_type="Release"):
    os.chdir(target_directory)
    shutil.copyfile(
        os.path.join(openfast_directory, "build32", "modules-ext", "map", cmake_build_type, "mapcpplib.dll"), 
        os.path.join("MAP_Win32.dll")
    )
    shutil.copyfile(
        os.path.join(openfast_directory, "build64", "modules-ext", "map", cmake_build_type, "mapcpplib.dll"), 
        os.path.join("MAP_x64.dll")
    )

def package_discon(discon_parent, target_directory, cmake_build_type="Release"):
    os.chdir(target_directory)

    win32 = os.path.join("DISCON_DLLS", "Win32")
    bit64 = os.path.join("DISCON_DLLS", "64bit")
    os.makedirs(win32)
    os.makedirs(bit64)

    shutil.copyfile(
        os.path.join(discon_parent, "DISCON", "build32", cmake_build_type, "DISCON.dll"),
        os.path.join(win32, "DISCON.dll")
    )
    shutil.copyfile(
        os.path.join(discon_parent, "DISCON_ITI", "build32", cmake_build_type, "DISCON_ITIBarge.dll"),
        os.path.join(win32, "DISCON_ITIBarge.dll")
    )
    shutil.copyfile(
        os.path.join(discon_parent, "DISCON_OC3", "build32", cmake_build_type, "DISCON_OC3Hywind.dll"),
        os.path.join(win32, "DISCON_OC3Hywind.dll")
    )
    shutil.copyfile(
        os.path.join(discon_parent, "DISCON", "build64", cmake_build_type, "DISCON.dll"),
        os.path.join(bit64, "DISCON.dll")
    )
    shutil.copyfile(
        os.path.join(discon_parent, "DISCON_ITI", "build64", cmake_build_type, "DISCON_ITIBarge.dll"),
        os.path.join(bit64, "DISCON_ITIBarge.dll")
    )
    shutil.copyfile(
        os.path.join(discon_parent, "DISCON_OC3", "build64", cmake_build_type, "DISCON_OC3Hywind.dll"),
        os.path.join(bit64, "DISCON_OC3Hywind.dll")
    )

if __name__=="__main__":
    tag = "v2.1.0"
    openfast_directory = "C:/Users/rmudafor/Development/openfast"
    target_directory = "C:/Users/rmudafor/Development/{}".format(tag)

    # make a fresh target directory
    if os.path.isdir(target_directory):
        shutil.rmtree(target_directory, ignore_errors=True)
    os.makedirs(target_directory)

    # checkout the tag in git
    os.chdir(openfast_directory)
    subprocess.run(["git", "checkout", tag])

    # compile openfast and put in target directory
    compile_openfast(openfast_directory)
    package_openfast(openfast_directory, target_directory)

    # compile MAP and put in target directory
    compile_maplib(openfast_directory)
    package_maplib(openfast_directory, target_directory)

    discon_parent = os.path.join(openfast_directory, "reg_tests/r-test/glue-codes/openfast/5MW_Baseline/ServoData/")
    compile_discon(os.path.join(discon_parent, "DISCON"))
    compile_discon(os.path.join(discon_parent, "DISCON_ITI"))
    compile_discon(os.path.join(discon_parent, "DISCON_OC3"))
    package_discon(discon_parent, target_directory)
