#!/bin/bash

if [ -e ${HOME}/.profile ]; then 
    touch "${HOME}/.profile"
fi


# Utility function 

pathadd() {
    echo "Adding $1 to PATH"
    if [ -d "$1" ] && [[ ":$PATH" != *":$1:"* ]]; then
        echo "Added $1 to PATH"
        #$PATH="${PATH:+"$PATH:"}$1"
        echo 'export PATH=$PATH:'${1} >> $HOME/.profile
    fi
}

# Dependencies
sudo apt-get install libxslt1-dev libxml2-dev zlib1g-dev python3-pip git python-antlr

# ASN.1 compiler 
sudo apt-get install mono-devel fsharp antlr
git clone https://github.com/ttsiodras/asn1scc
cd asn1scc 
xbuild /p:TargetFrameworkVersion="v4.5"
mv "$(pwd)/Asn1f2/bin/Debug/Asn1f2.exe" "$(pwd)/Asn1f2/bin/Debug/asn1.exe"
pathadd "$(pwd)/Asn1f2/bin/Debug"  
echo 'export VDM_STG=$(pwd)/Asn1f2/Debug/bin/vdm.stg' >> ~/.profile
cd ../

# VDM-mapper repository clone
git clone -b vdm-b-mapper https://github.com/tfabbri/DataModellingTools
cd DataModellingTools
pip3 install --user --upgrade .
pathadd "${HOME}/.local/bin"
pathadd "$(pwd)/dmt/vdm_tests/"
cd ../

if grep -q "source .profile" $HOME/.bashrc; then 
    echo 'source .profile' >> ~/.bashrc
fi

echo "Restart your shell to complete the installation" 
