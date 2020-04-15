#!/bin/bash
#
# Utility to determine the function/line number from backtrace information
#
# Requires the library to have been compiled with "-g" flag and preferably
# "-rdynamic" flag (when using GNU GCC)
#

if [ "$#" != 2 ] ; then
    echo "Usage: ${BASH_SOURCE[0]} <libfile> <symbol>"
    exit 1
fi

libname=$1              # Library to lookup the symbol
symbol=$2               # Symbol + offset from backtrace
func_name=${symbol%+*}  # Extract the function/method
offset=${symbol##*+}    # Extract the offset

# Determine the address of the method/function
sym_hex=$(printf "0x%s" $(nm ${libname} | grep ${func_name} | awk '{print $1}'))
# compute the address to lookup
lookup_hex=$(printf "0x%X" $(( ${sym_hex} + ${offset})))

# Print out the file/line info
#On Mac
atos -o ${libname} ${lookup_hex}
#On Linux
#addr2line -e ${libname} ${lookup_hex}
