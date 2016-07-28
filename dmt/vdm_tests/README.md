VDM Test directory
------------------

    - DataTypes.asn Definition of datatypes
    - DataView.aadl File generated from DataTypes.asn through asn2aadlPlus
    - vdm-tests.aadl Simple AADL architecture to test the VDM B_mapper
    - output/tester Directory containing the VDM2C Native Library and testing code


Run the code generation:

`$ aadl2glueC -o output/tester vdm_tests.aadl DataView.aadl`

Compile the generated code:

`$ cd output`  
`$ mkdir build`  
`$ cd build`  
`$ cmake ../`  
`$ make`  

Run the generated code to test the B_mapper:

`$ ./tester/tester`



