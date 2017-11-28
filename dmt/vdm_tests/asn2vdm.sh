#!/bin/bash

echo "Asn.1 to VDM"
echo "Input file: $1"
echo "Output file: $2"
asn1.exe -customStgAstVersion 4 -customStg $VDM_STG/vdm.stg:$2 $1
