
import os
import shutil
import subprocess
from multiprocessing import Process

def remove_dir(directory):
    if os.path.isdir(directory):
        shutil.rmtree(directory, ignore_errors=True)

def rm_mkdir_cd(directory):
    remove_dir(directory)
    os.makedirs(directory)
    os.chdir(directory)

def clone_openfast(target_repo_url, target_branch="master", project_directory=None):
    remove_dir(project_directory)
    subprocess.run(
        [
            "git",
            "clone",
            "--recursive",
            "-b",
            "{}".format(target_branch),
            "{}".format(target_repo_url),
            "{}".format(project_directory)
        ]
    )

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
    subprocess.run(
        ["cmake", "--build", ".", "--config", cmake_build_type, "--target", target],
        check=True
    )

def execute_rtest(project_directory, binary="openfast.exe", machine="windows", compiler="intel", tolerance="1e-5"):
    os.chdir(os.path.join(project_directory, "reg_tests"))
    command = [
        "python",
        "manualRegressionTest.py",
        os.path.join("..", "install", "bin", binary),
        machine,
        compiler,
        tolerance
    ]
    subprocess.run(command, check=True)

def update_baselines(project_directory, machine="windows", compiler="intel"):
    os.chdir(os.path.join(project_directory, "reg_tests", "r-test"))
    command = [
        "python",
        "updateBaselineSolutions.py",
        os.path.join("glue-codes", "openfast", "CaseList.md"),
        os.path.join("..", "..", "build", "reg_tests", "glue-codes", "openfast"),
        os.path.join("glue-codes", "openfast"),
        "macos",
        "gnu"   
    ]
    subprocess.run(command, check=True)

if __name__=="__main__":
    ## Configuration
    target_repo_url = "https://github.com/bjonkman/openfast"
    target_branch = "f/Airfoil-interp"
    local_directory_name = "/Users/rmudafor/Desktop/openfast_bonnie"
    ##

    # Clone the reporitory
    clone_openfast(
        target_repo_url,
        target_branch=target_branch,
        project_directory=local_directory_name
    )

    # Compile OpenFAST with CMake
    compile_cmake_project(
        local_directory_name,
        cmake_generator="Unix Makefiles",
        cmake_flags=["-DBUILD_TESTING=ON"],
        target="install"
    )

    # Run the regression tests
    execute_rtest(
        local_directory_name,
        machine="macos",
        compiler="gnu"
    )

    # Update the baseline solutions
    update_baselines(
        local_directory_name,
        machine="macos",
        compiler="gnu"
    )
