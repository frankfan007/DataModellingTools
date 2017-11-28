#!/bin/bash

# A POSIX variable
OPTIND=1  # Reset in case getopts has been used previously in the shell.

# Initialize our own variables:
output_dir="./out_dir"
input_file=""

while getopts "h?i:o:" opt; do
    case "$opt" in
    h|\?)
        show_help
        exit 0
        ;;
    i)  input_file=$OPTARG
        ;;
    o)  output_dir=$OPTARG
        ;;
    esac
done

shift $((OPTIND-1))

[ "$1" = "--" ] && shift


if [[ ! -e $output_dir ]]; then
    mkdir -p $output_dir
elif [[ ! -d $output_dir ]]; then
    echo "$output_dir already exists but is not a directory" 1>&2
fi

echo "input_file=$input_file, output_dir='$output_dir', Leftovers: $@"

echo "Generation of piece of code required..."
asn2aadlPlus  $input_file  DataView.aadl
asn2aadlVDM   $input_file  vdm_temp_architeture.aadl
aadl2glueC -o $output_dir  vdm_temp_architeture.aadl DataView.aadl
asn1.exe -c -uPER -typePrefix "asn1Scc" -o $output_dir $input_file 
rm DataView.aadl vdm_temp_architeture.aadl
