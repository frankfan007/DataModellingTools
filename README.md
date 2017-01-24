[![Build and Test Status of Data Modelling Tools on Circle CI](https://circleci.com/gh/ttsiodras/DataModellingTools.svg?&style=shield&circle-token=9df10d36b6b4ccd923415a5890155b7bf54b95c5)](https://circleci.com/gh/ttsiodras/DataModellingTools/tree/master)

[![Tommaso Build and Test Status](https://circleci.com/gh/tfabbri/DataModellingTools.svg?style=svg)](https://circleci.com/gh/tfabbri/DataModellingTools/tree/vdm-b-mapper)

TASTE Data Modelling Tools
==========================

These are the tools used by the European Space Agency's [TASTE toolchain](https://taste.tuxfamily.org/)
to automate handling of the Data Modelling. They include more than two
dozen codegenerators that automatically create the 'glue'; the run-time translation
bridges that allow code generated by modelling tools (Simulink, SCADE, OpenGeode, etc)
to "speak" to one another, via ASN.1 marshalling.

For the encoders and decoders of the messages
themselves, TASTE uses [ASN1SCC](https://github.com/ttsiodras/asn1scc) - an ASN.1
compiler specifically engineered for safety-critical environments.

For more details, visit the [TASTE site](https://taste.tuxfamily.org/).

Installation
------------

Linux Dependencies:

    $ sudo apt-get install libxslt1-dev libxml2-dev zlib1g-dev python3-pip

MacOS Dependencies:

    $ brew update
    $ brew upgrade
    $ brew install libxslt python3 lzlib binutils libantlr3c wget
    $ wget -O - -q https://github.com/ttsiodras/DataModellingTools/files/335591/antlr-2.7.7.tar.gz | tar zxvf - ; cd antlr-2.7.7/lib/python ; pip2 install . 

Installation command:

    $ cd DataModellingTools
    $ pip3 install --user --upgrade .

MacOS users:

Add to your `PATH` into the `.bash_profile` file `$HOME/Library/Python/x.y/bin` where `x.y`specifies the current version of Python3 installed.

### For developers

Installation command

    $ pip3 install --user --upgrade --editable .

For developing the tools, the packaged Makefile allow for easy static-analysis
via the dominant Python static analyzers and syntax checkers:

    $ make flake8  # check for pep8 compliance
    $ make pylint  # static analysis with pylint
    $ make mypy    # type analysis with mypy

Contents
--------

What is packaged:

- **commonPy** (*library*)

    Contains the basic API for parsing ASN.1 (via invocation of
    [ASN1SCC](https://github.com/ttsiodras/asn1scc) and simplification of the generated XML AST representation to the Python classes inside `asnAST.py`. The class diagram with the AST classes is [packaged in the code](dmt/commonPy/asnAST.py#L42).

- **asn2aadlPlus** (*utility*)

    Converts the type declarations inside ASN.1 grammars to AADL
    declarations, that are used by [Ocarina](https://github.com/OpenAADL/ocarina)
    to generate the executable containers.

- **asn2dataModel** (*utility*)

    Reads the ASN.1 specification of the exchanged messages, and generates
    the semantically equivalent Modeling tool/Modeling language declarations
    (e.g. SCADE/Lustre, Matlab/Simulink, etc).

    The actual mapping logic exists in plugins, called *A mappers*
    (`simulink_A_mapper.py` handles Simulink/RTW, `scade6_A_mapper.py`
    handles SCADE6, `ada_A_mapper.py` generates Ada types,
    `sqlalchemy_A_mapper.py`, generates SQL definitions via SQLAlchemy, etc)

- **aadl2glueC** (*utility*)

    Reads the AADL specification of the system, and then generates the runtime
    bridge-code that will map the message data structures from those generated
    by [ASN1SCC](https://github.com/ttsiodras/asn1scc) to/from those generated
    by the modeling tool (that is used to functionally model the subsystem -
    e.g. SCADE, ObjectGeode, Matlab/Simulink, C, Ada, etc).

Contact
-------

For bug reports, please use the Issue Tracker; for any other communication,
contact me at:

    Thanassis Tsiodras
    Real-time Embedded Software Engineer
    System, Software and Technology Department
    European Space Agency

    ESTEC
    Keplerlaan 1, PO Box 299
    NL-2200 AG Noordwijk, The Netherlands
    Athanasios.Tsiodras@esa.int | www.esa.int
    T +31 71 565 5332
