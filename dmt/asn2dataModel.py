#!/usr/bin/env python3
# vim: set expandtab ts=8 sts=4 shiftwidth=4
#
# (C) Semantix Information Technologies.
#
# Copyright 2014-2015 IB Krates <info@krates.ee>
#       QGenc code generator integration
#
# Semantix Information Technologies is licensing the code of the
# Data Modelling Tools (DMT) in the following dual-license mode:
#
# Commercial Developer License:
#       The DMT Commercial Developer License is the suggested version
# to use for the development of proprietary and/or commercial software.
# This version is for developers/companies who do not want to comply
# with the terms of the GNU Lesser General Public License version 2.1.
#
# GNU LGPL v. 2.1:
#       This version of DMT is the one to use for the development of
# applications, when you are willing to comply with the terms of the
# GNU Lesser General Public License version 2.1.
#
# Note that in both cases, there are no charges (royalties) for the
# generated code.
#
'''
Model Translator

This is one of the code generators that Semantix developed for
the European research project ASSERT. It is now enhanced in the
context of Data Modelling and Data Modelling Tuning projects.

It reads the ASN.1 specification of the exchanged messages, and
generates the semantically equivalent ModelingTool/ModelingLanguage
declarations (e.g. SCADE/Lustre, Matlab/Simulink statements, etc).
'''
import os
import sys
import copy
from importlib import import_module

from typing import Dict, Tuple, Any  # NOQA pylint: disable=unused-import

from .commonPy import configMT, asnParser, cleanupNodes, verify
from .commonPy.utility import inform, panic
from .commonPy.asnParser import Filename, Typename, AST_Lookup, AST_TypesOfFile, AST_Leaftypes  # NOQA pylint: disable=unused-import
from .commonPy.asnAST import AsnNode  # NOQA pylint: disable=unused-import

from . import A_mappers  # NOQA pylint:disable=unused-import


def usage(argsToTools: Dict[str, str]) -> None:
    '''Print usage instructions.'''
    msg = 'Usage: %s <options> input1.asn1 [input2.asn1]...\nWhere options are:\n'
    msg += '\t-verbose\t\tDisplay more debug output\n'
    msg += '\t-o dirname\t\tDirectory to place generated files\nAnd one of:\n'
    for opt in sorted(argsToTools.keys()):
        msg += '\t-' + opt + ' (for ' + argsToTools[opt][0].upper() + argsToTools[opt][1:] + ')\n'
    panic(msg % sys.argv[0])


def main() -> None:
    if "-v" in sys.argv:
        import pkg_resources  # pragma: no cover
        version = pkg_resources.require("dmt")[0].version  # pragma: no cover
        print("asn2dataModel v" + str(version))  # pragma: no cover
        sys.exit(1)  # pragma: no cover

    argsToTools = {
        'toOG': 'OG',
        'toSCADE5': 'SCADE5',
        'toSCADE6': 'SCADE6',
        'toSIMULINK': 'Simulink',
        'toC': 'C',
        'toCPP': 'C',
        'toRTDS': 'RTDS',
        'toAda': 'ada',
        'toPython': 'python',
        'toSMP2': 'smp2',
        'toQGenAda': 'qgenada',
        'toQGenC': 'qgenc',
        'toSQL': 'sql',
        'toSqlalchemy': 'sqlalchemy'
    }
    for i in os.listdir(os.path.dirname(os.path.abspath(A_mappers.__file__))):
        if '_A_mapper' in i and i.endswith('.py'):
            target = i.split('_')[0]
            if target.lower() not in [x.lower() for x in argsToTools.values()]:
                argsToTools['to' + target.capitalize()] = target  # pragma: no cover

    toolSelected = {}
    for i in argsToTools:
        toolSelected[i] = False

    if sys.argv.count("-o") != 0:
        idx = sys.argv.index("-o")
        try:
            configMT.outputDir = os.path.normpath(sys.argv[idx + 1]) + os.sep
        except:   # pragma: no cover
            usage(argsToTools)  # pragma: no cover
        del sys.argv[idx]
        del sys.argv[idx]
        if not os.path.isdir(configMT.outputDir):
            panic("'%s' is not a directory!\n" % configMT.outputDir)  # pragma: no cover
    if "-verbose" in sys.argv:
        configMT.verbose = True
        sys.argv.remove("-verbose")
    for i in argsToTools:
        if "-" + i in sys.argv:
            toolSelected[i] = True
            sys.argv.remove("-" + i)

    if len(sys.argv) < 2:
        usage(argsToTools)

    # One of the tools must be selected!
    if not any(toolSelected[i] for i in argsToTools):
        usage(argsToTools)  # pragma: no cover

    for f in sys.argv[1:]:
        if not os.path.isfile(f):
            panic("'%s' is not a file!\n" % f)  # pragma: no cover

    uniqueFilenames = list(set(sys.argv[1:]))
    asnParser.ParseAsnFileList(uniqueFilenames)

    uniqueASNfiles = {}  # type: Dict[Filename, Tuple[AST_Lookup, List[AsnNode], AST_Leaftypes]]
    for asnFile in uniqueFilenames:
        tmpNames = {}  # type: AST_Lookup
        for name in asnParser.g_typesOfFile[asnFile]:
            tmpNames[name] = asnParser.g_names[name]

        uniqueASNfiles[asnFile] = (
            copy.copy(tmpNames),                            # map Typename to type definition class from asnAST
            copy.copy(asnParser.g_astOfFile[asnFile]),    # list of nameless type definitions
            copy.copy(asnParser.g_leafTypeDict))   # map from Typename to leafType

        inform("Checking that all base nodes have mandatory ranges set in %s..." % asnFile)
        for node in list(tmpNames.values()):
            verify.VerifyRanges(node, asnParser.g_names)

    if configMT.debugParser:
        sys.exit(0)  # pragma: no cover

    loadedBackends = {}  # type: Dict[Filename, Any]

    # If some AST nodes must be skipped (for any reason), go learn about them
    badTypes = cleanupNodes.DiscoverBadTypes()

    # For each ASN.1 grammar file referenced in the system level description
    for arg, modelingLanguage in argsToTools.items():
        if not toolSelected[arg]:
            continue
        backendFilename = "." + modelingLanguage.lower() + "_A_mapper.py"
        inform("Parsing %s...", backendFilename)
        try:
            backend = import_module(backendFilename[:-3], 'dmt.A_mappers')  # pragma: no cover
            if backendFilename[:-3] not in loadedBackends:
                loadedBackends[backendFilename[:-3]] = 1
                if configMT.verbose:
                    backend.Version()
        except ImportError as err:  # pragma: no cover
            panic("Failed to load backend (%s): %s" % (backendFilename, str(err)))  # pragma: no cover

        # Esp. for C, we want to pass the complete list of ASN.1 files to ASN1SCC,
        # instead of working per type:
        if modelingLanguage.lower() in ["c", "ada", "smp2", "qgenc", "qgenada"]:
            if 'OnStartup' in dir(backend):
                backend.OnStartup(modelingLanguage, list(uniqueASNfiles.keys()), configMT.outputDir, badTypes)
            if 'OnShutdown' in dir(backend):
                backend.OnShutdown(badTypes)
            continue  # bug in coverage.py...  # pragma: no cover

        # Work on each ASN.1 file's types
        for asnFile in uniqueASNfiles:
            if 'OnStartup' in dir(backend):
                backend.OnStartup(modelingLanguage, asnFile, configMT.outputDir, badTypes)

            leafTypeDict = uniqueASNfiles[asnFile][2]

            inform("Executing mappings for types inside %s...", asnFile)
            names = uniqueASNfiles[asnFile][0]
            for nodeTypename in sorted(names):
                # Check if this type must be skipped
                if nodeTypename in badTypes:
                    continue
                node = names[nodeTypename]
                inform("Processing %s (%s)...", nodeTypename, modelingLanguage)

                # First, make sure we know what leaf type this node is
                assert nodeTypename in leafTypeDict

                leafType = leafTypeDict[nodeTypename]
                # If it is a base type,
                if leafType in ['BOOLEAN', 'INTEGER', 'REAL', 'OCTET STRING']:
                    # make sure we have mapping instructions for BASE elements
                    if 'OnBasic' not in dir(backend):
                        panic("ASN.1 grammar contains literal(%s) but no BASE section found in the mapping grammar (%s)" % (nodeTypename, sys.argv[2]))  # pragma: no cover
                    backend.OnBasic(nodeTypename, node, leafTypeDict)
                # if it is a complex type
                elif leafType in ['SEQUENCE', 'SET', 'CHOICE', 'SEQUENCEOF', 'SETOF', 'ENUMERATED']:
                    # make sure we have mapping instructions for the element
                    mappedName = {
                        'SEQUENCE': 'OnSequence',
                        'SET': 'OnSet',
                        'CHOICE': 'OnChoice',
                        'SEQUENCEOF': 'OnSequenceOf',
                        'SETOF': 'OnSetOf',
                        'ENUMERATED': 'OnEnumerated'
                    }
                    if mappedName[leafType] not in dir(backend):
                        panic("ASN.1 grammar contains %s but no %s section found in the mapping grammar (%s)" % (nodeTypename, mappedName[leafType], backendFilename))  # pragma: no cover
                    processor = backend.__dict__[mappedName[leafType]]
                    processor(nodeTypename, node, leafTypeDict)
                # what type is it?
                else:  # pragma: no cover
                    panic("Unexpected type of element: %s" % leafTypeDict[nodeTypename])  # pragma: no cover

            if 'OnShutdown' in dir(backend):
                backend.OnShutdown(badTypes)

if __name__ == "__main__":
    if "-pdb" in sys.argv:
        sys.argv.remove("-pdb")  # pragma: no cover
        import pdb  # pragma: no cover pylint: disable=wrong-import-position,wrong-import-order
        pdb.run('main()')  # pragma: no cover
    else:
        main()
