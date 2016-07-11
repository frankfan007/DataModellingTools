#!/bin/bash

echo "Generation of piece of code required..."

asn2aadlPlus DataTypes.asn DataView.aadl
aadl2glueC -o output/tester vdm_tests.aadl DataView.aadl
asn1.exe -c -uPER -typePrefix "asn1Scc" -o output/tester DataTypes.asn
