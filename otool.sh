# This is how to change the linked library paths within an executable

# beamdyn_driver
target=/Users/rmudafor/Desktop/openfast/install/bin/beamdyn_driver
install_name_tool -change @rpath/libmkl_intel_lp64.dylib /opt/intel/compilers_and_libraries/mac/mkl/lib/libmkl_intel_lp64.dylib  $target
install_name_tool -change @rpath/libmkl_sequential.dylib /opt/intel/compilers_and_libraries/mac/mkl/lib/libmkl_sequential.dylib  $target
install_name_tool -change @rpath/libmkl_core.dylib /opt/intel/compilers_and_libraries/mac/mkl/lib/libmkl_core.dylib  $target

# openfast
target=/Users/rmudafor/Desktop/openfast/install/bin/openfast
install_name_tool -change @rpath/libmkl_intel_lp64.dylib /opt/intel/compilers_and_libraries/mac/mkl/lib/libmkl_intel_lp64.dylib  $target
install_name_tool -change @rpath/libmkl_sequential.dylib /opt/intel/compilers_and_libraries/mac/mkl/lib/libmkl_sequential.dylib  $target
install_name_tool -change @rpath/libmkl_core.dylib /opt/intel/compilers_and_libraries/mac/mkl/lib/libmkl_core.dylib  $target
