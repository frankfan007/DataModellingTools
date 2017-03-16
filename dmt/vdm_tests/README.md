VDM Test directory
------------------

- DataTypes.asn Definition of datatypes
- DataView.aadl File generated from DataTypes.asn through asn2aadlPlus
- vdm-tests.aadl Simple AADL architecture to test the VDM B_mapper, now this file can be generated through the script `asn2aadlVDM` part of DataModellingTools installation
- output/tester Directory containing the VDM2C Native Library and testing code


Run the code generation:

`$ ./gen_mapping.sh -i asn_input_file -o output_dir`

The directory `output` contains an example of simple test code to verify the correcteness of the generated code:

```
$ cd output 
$ mkdir build  
$ cd build  
$ cmake ../  
$ make  
```

Run the generated code to test the B_mapper:

`$ ./exe/exe`  

Generate convert functions
--------------------------

This VDM B_mapper can be used for the generation the *convert* functions between ASN.1 and `vdm2c` C code for project outside the TASTE environment. To do this, in the following are listed the operations to follow:

1. Definition of the data type format in ASN.1 (e.g. `DataTypes.asn`)
2. Conversion of the ASN.1 definition `DataTypes.asn` into VDMPP, to this launch the `asn2vdm.sh` script:

`$ asn2vdm.sh DataTypes.asn DataTypes.vdmpp`

3. Launch the `vdm2c` for generating the C code from the VDMPP file (e.g. `DataTypes.vdmpp`) and copy the generated code into `output_dir`

4. Generate the AADL file required from the framework for the generation of the mapping functions between the TVP and ASN.1;
the generated AADL architecture is characterized by the following structure: 
    - SUBPROGRAM containing for each type defined in the ASN.1 file (e.g. `DataTypes.asn`) one input parameter and one output parameter as reported below (type `NewType`):
    - SUBPROGRAM IMPLEMENTATION describing the implementation in the source language VDM.

`$ asn2aadlVDM DataTypes.asn VDM_architecture.aadl`


```
SUBPROGRAM mysub
FEATURES
    my_in_NewType:IN PARAMETER DataView::NewType {encoding=>UPER;};
    my_out_NewType::OUT PARAMETER DataView::NewType {encoding=>UPER;};
END mysub

SUBPROGRAM IMPLEMENTATION mysub.Vdm
PROPERTIES
    FV_Name => "mysub_fv_Vdm";
    Source_Language => Vdm;
END mysub.Vdm
```

5. Generation of the mapping function between the TVP and ASN.1 C representation

`$ aadl2glueC -o output_dir vdm_architecture.aadl DataView.aadl`

Summary of the TASTE utilities involved in the process:
```
$ asn2aadlPlus DataTypes.asn DataView.aadl
$ asn2aadlVDM  DataTypes.asn vdm_architecture.aadl
$ aadl2glueC -o output_dir vdm_architecture.aadl DataView.aadl
$ asn1.exe -c -uPER -typePrefix "asn1Scc" -o output_dir DataTypes.asn
```
