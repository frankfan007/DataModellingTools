VDM Test directory
------------------

    - DataTypes.asn Definition of datatypes
    - DataView.aadl File generated from DataTypes.asn through asn2aadlPlus
    - vdm-tests.aadl Simple AADL architecture to test the B\_mappers

Run the code generation:

`aadl2glueC -o outputDir vdm_tests.aadl DataView.aadl`



