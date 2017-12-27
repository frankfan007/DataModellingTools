#!/bin/bash
# Utility function 
pathadd() {
    if [ -d "$1" ] && [[ ":$PATH" != *":$1:"* ]]; then
        echo 'export PATH=$PATH:'${1} >> $HOME/$BASHRC
    fi
}

OPTIND=1
install_dir=""


while getopts "h?vf:" opt; do
    case "$opt" in
    h|\?)
        echo "Installation of mapping functions support"
        exit 0
        ;;
    f)  INSTALL_DIR=$OPTARG
        ;;
    esac
done

shift $((OPTIND-1))
[ "$1" = "--" ] && shift

if [ ! "${INSTALL_DIR}" ]
then
    echo "OVERTURE INSTALL_DIR ARGUMENT EMPTY"
    exit 1
fi

echo "INSTALL_DIR=${install_dir}" 

BASHRC=".bashrc"
cd ${INSTALL_DIR}

# Dependencies
if [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then 
    if [ -e ${HOME}/.profile ]; then 
        touch "${HOME}/.profile"
    fi
    sudo apt-get update
    sudo apt-get install mono-devel fsharp antlr
    sudo apt-get install libxslt1-dev libxml2-dev zlib1g-dev python3-pip git python-antlr
    wget -O -q https://github.com/ttsiodras/DataModellingTools/files/335591/antlr-2.7.7.tar.gz | targ -zxvf
    cd antlr-2.7.7/lib/python 
    sudo pip2 install .

elif [ "$(uname)" == "Darwin" ]; then
    BASHRC=".bash_profile"
    brew update
    brew upgrade
    brew install libxslt python python3 lzlib binutils libantlr3c wget
    wget -O -q https://github.com/ttsiodras/DataModellingTools/files/335591/antlr-2.7.7.tar.gz | targ -zxvf
    cd antlr-2.7.7/lib/python 
    sudo pip2 install .
fi

# ASN.1 compiler 
git clone https://github.com/ttsiodras/asn1scc
cd asn1scc 
xbuild /p:TargetFrameworkVersion="v4.5"
PWD=$(pwd)
mv "$(pwd)/Asn1f2/bin/Debug/Asn1f2.exe" "$(pwd)/Asn1f2/bin/Debug/asn1.exe"
pathadd "${PWD}/Asn1f2/bin/Debug"  
echo "export VDM_STG=${PWD}/Asn1f2/Debug/bin/vdm.stg" >> $HOME/$BASHRC
cd ../

# VDM-mapper repository clone
git clone -b vdm-b-mapper https://github.com/tfabbri/DataModellingTools
cd DataModellingTools
PWD=$(pwd)
pip3 install --user --upgrade .
pathadd "${HOME}/.local/bin"
pathadd "${PWD}/dmt/vdm_tests/"
cd ../

echo "Restart your shell to complete the installation"
