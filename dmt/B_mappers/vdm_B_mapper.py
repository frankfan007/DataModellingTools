#
# (C) Semantix Information Technologies.
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
This is the code generator for the Overture VDM code mappers.
This backend is called by aadl2glueC, when a VDM subprogram is identified in the input concurrency view.
'''

# from ..commonPy.utility import panic

from typing import List

from ..commonPy.asnAST import (
    sourceSequenceLimit, isSequenceVariable, AsnInt, AsnReal, AsnEnumerated,
    AsnBool, AsnSequenceOrSet, AsnSequenceOrSetOf, AsnChoice, AsnOctetString,
    AsnBasicNode, AsnNode, AsnSequence, AsnSet, AsnSetOf, AsnSequenceOf)
from ..commonPy.asnParser import AST_Lookup, AST_Leaftypes
from ..commonPy.recursiveMapper import RecursiveMapper
from ..commonPy.asnParser import g_modules, g_names

from .asynchronousTool import ASynchronousToolGlueGenerator

isAsynchronous = True
vdmBackend = None


def Version() -> None:
    print("Code generator: " + "$Id: vdm_B_mapper.py 2390 2015-07-04 12:39:17Z tfabbri $")


# noinspection PyListCreation
# pylint: disable=no-self-use
class FromVDMToASN1SCC(RecursiveMapper):
    def __init__(self) -> None:
        self.uniqueID = 0

    def UniqueID(self) -> int:
        self.uniqueID += 1
        return self.uniqueID

    def DecreaseUniqueID(self) -> None:
        self.uniqueID -= 1

    def MapInteger(self, srcVDMVariable: str, destVar: str, _: AsnInt, __: AST_Leaftypes, ___: AST_Lookup) -> List[str]:  # pylint: disable=invalid-sequence-index
        return ["%s = (asn1SccSint)(%s)->value.intVal;\n" % (destVar, srcVDMVariable)]

    def MapBoolean(self, srcVDMVariable: str, destVar: str, _: AsnBool, __: AST_Leaftypes, ___: AST_Lookup)-> List[str]:  # pylint: disable=invalid-sequence-index
        return ["%s = (%s->value.boolVal==true)?0xff:0;\n" % (destVar, srcVDMVariable)]

    def MapReal(self, srcVDMVariable: str, destVar: str, _: AsnReal, __: AST_Leaftypes, ___: AST_Lookup) -> List[str]:  # pylint: disable=invalid-sequence-index
        return ["%s = ((TVP) %s)->value.doubleVal;\n" % (destVar, srcVDMVariable)]

    def MapSequenceOf(self, srcVDMVariable: str, destVar: str, node: AsnSequenceOrSetOf, leafTypeDict: AST_Leaftypes, names: AST_Lookup) -> List[str]:  # pylint: disable=invalid-sequence-index
        lines = []  # type: List[str]
        lines.append("{\n")
        uniqueId = self.UniqueID()
        lines.append("    int i%s;\n" % uniqueId)
        lines.append("    UNWRAP_COLLECTION(col, %s);" % srcVDMVariable)
        lines.append("    int size%s = col->size;" % uniqueId)
        lines.append("    int count%s = 0;" % uniqueId)
        lines.append("    for(i%s=0; i%s<size%s; i%s++) {\n" % (uniqueId, uniqueId, uniqueId, uniqueId))
        lines.append("        if(col->value[i%s] != NULL){\n" % uniqueId)
        lines.extend(
            ["            " + x
             for x in self.Map(
                 "col->value[i%s]" % uniqueId,
                 "%s.arr[i%s]" % (destVar, uniqueId),
                 node._containedType,
                 leafTypeDict,
                 names)])
        lines.append("            count%s++;\n" %uniqueId)
        lines.append("        }\n")
        lines.append("    }\n")
        if isSequenceVariable(node):
            lines.append("    %s.nCount = count%s;\n" % (destVar, uniqueId))
        lines.append("}\n")
        self.DecreaseUniqueID()
        return lines

    def MapOctetString(self, srcVDMVariable: str, destVar: str, node: AsnOctetString, __: AST_Leaftypes, ___: AST_Lookup) -> List[str]:  # pylint: disable=invalid-sequence-index
        lines = []  # type: List[str]
        uniqueId = self.UniqueID()
        lines.append("{\n")
        lines.append("    int i%s;\n" % uniqueId)
        lines.append("    UNWRAP_COLLECTION(col, %s);" % srcVDMVariable)
        lines.append("    int size = col->size;")
        lines.append("    int count%s = 0;" % uniqueId)
        lines.append("    for(i%s=0; i%s<size; i%s++) {\n" % (uniqueId, uniqueId, uniqueId))
        lines.append("        if(col->value[i%s] != NULL){\n" % uniqueId)
        lines.append("            %s.arr[i%s] = (unsigned char) (col->value[i%s]->value.charVal);\n" % (destVar, uniqueId, uniqueId))
        lines.append("            count%s++;\n" %uniqueId)
        lines.append("        }\n")
        lines.append("    }\n")
        if isSequenceVariable(node):
            lines.append("    %s.nCount = count%s;\n" % (destVar, uniqueId))
        lines.append("}\n")
        self.DecreaseUniqueID()
        return lines

    def MapEnumerated(self, srcVDMVariable: str, destVar: str, node: AsnEnumerated, __: AST_Leaftypes, ___: AST_Lookup) -> List[str]:  # pylint: disable=invalid-sequence-index
        lines = []  # type: List[str]
        lines.append("switch(%s->value.intVal) {\n" %srcVDMVariable)
        for m in node._members:
            lines.append("    case QUOTE_%s:\n" % m[0].upper())
            lines.append("        (%s) = %s;\n" % (destVar, m[1]))
            lines.append("        break;\n")
        lines.append("}\n")
        return lines

    def MapSequence(self, srcVDMVariable: str, destVar: str, node: AsnSequenceOrSet, leafTypeDict: AST_Leaftypes, names: AST_Lookup) -> List[str]:  # pylint: disable=invalid-sequence-index
        lines = []  # type: List[str]
        for key in names:
            if names[key] == node:
                type_str = key  # type: str

        for child in node._members:
            lines.extend(
                self.Map(
                    # "((struct * %s) (%s->value.ptr))->%s" % (type_str, srcVDMVariable, self.CleanName(child[0])),
                    "TO_CLASS_PTR(%s, %s)->m_%s_%s" % (srcVDMVariable, type_str, type_str, self.CleanName(child[0])),
                    destVar + "." + self.CleanName(child[0]),
                    child[1],
                    leafTypeDict,
                    names))
        return lines

    def MapSet(self, srcVDMVariable: str, destVar: str, node: AsnSequenceOrSet, leafTypeDict: AST_Leaftypes, names: AST_Lookup) -> List[str]:  # pylint: disable=invalid-sequence-index
        return self.MapSequence(srcVDMVariable, destVar, node, leafTypeDict, names)  # pragma: nocover
'''
    def MapChoice(self, srcVDMVariable, destVar, node, leafTypeDict, names):
        lines = []  # type: List[str]
        childNo = 0
        for child in node._members:
            childNo += 1
            lines.append("%sif (%s.present == %d) {\n" % (self.maybeElse(childNo), srcSDLVariable, childNo))
            lines.extend(
                ["    " + x
                 for x in self.Map(
                     "%s.__value.%s" % (srcSDLVariable, self.CleanName(child[0])),
                     destVar + (".u.%s" % self.CleanName(child[0])),
                     child[1],
                     leafTypeDict,
                     names)])
            lines.append("    %s.kind = %s;\n" % (destVar, self.CleanName(child[2])))
            lines.append("}\n")
        return lines

    def MapSetOf(self, unused_srcSDLVariable, unused_destVar, node, unused_leafTypeDict, unused_names):
        panic("The PragmaDev mapper does not support SETOF. Please use SEQUENCEOF instead (%s)" % node.Location())  # pragma: nocover
'''


# noinspection PyListCreation
# pylint: disable=no-self-use
class FromASN1SCCtoVDM(RecursiveMapper):
    def __init__(self) -> None:
        self.uniqueID = 0

    def UniqueID(self) -> int:
        self.uniqueID += 1
        return self.uniqueID

    def DecreaseUniqueID(self) -> None:
        self.uniqueID -= 1

    def MapInteger(self, srcVar: str, dstVDMVariable: str, _: AsnInt, __: AST_Leaftypes, ___: AST_Lookup) -> List[str]:  # pylint: disable=invalid-sequence-index
        return ["%s = newInt(%s);\n" % (dstVDMVariable, srcVar)]

    def MapBoolean(self, srcVar: str, dstVDMVariable: str, _: AsnBool, __: AST_Leaftypes, ___: AST_Lookup) -> List[str]:  # pylint: disable=invalid-sequence-index
        return ["%s = (%s)?newBool(true):newBool(false);\n" % (dstVDMVariable, srcVar)]

    def MapReal(self, srcVar: str, dstVDMVariable: str, _: AsnReal, __: AST_Leaftypes, ___: AST_Lookup) -> List[str]:  # pylint: disable=invalid-sequence-index
        return ["%s = newReal(%s);\n" % (dstVDMVariable, srcVar)]

    def MapSequenceOf(self, srcVar: str, dstVDMVariable: str, node: AsnSequenceOrSetOf, leafTypeDict: AST_Leaftypes, names: AST_Lookup) -> List[str]:  # pylint: disable=invalid-sequence-index
        lines = []  # type: List[str]
        lines.append("{\n")
        uniqueId = self.UniqueID()
        limit = sourceSequenceLimit(node, srcVar)
        lines.append("    int i%s;\n" % uniqueId)
        lines.append("    UNWRAP_COLLECTION(col, %s);" % dstVDMVariable)
        lines.append("    for(i%s=0; i%s<%s; i%s++) {\n" % (uniqueId, uniqueId, limit, uniqueId))
        lines.extend(
            ["        " + x
             for x in self.Map(
                 srcVar + ".arr[i%s]" % uniqueId,
                 "col->value[i%s]" % (uniqueId),
                 node._containedType,
                 leafTypeDict,
                 names)])
        lines.append("    }\n")
        lines.append("}\n")
        self.DecreaseUniqueID()
        return lines

    def MapOctetString(self, srcVar: str, dstVDMVariable: str, node: AsnOctetString, __: AST_Leaftypes, ___: AST_Lookup) -> List[str]:  # pylint: disable=invalid-sequence-index
        lines = []  # type: List[str]
        limit = sourceSequenceLimit(node, srcVar)
        lines.append("{\n")
        lines.append("    int i;\n")
        lines.append("    UNWRAP_COLLECTION(col, %s);" % dstVDMVariable)
        lines.append("    for(i=0; i<%s; i++) {\n" % limit)
        lines.append("        col->value[i] = newChar((char) (%s.arr[i]));\n" % (srcVar))
        lines.append("    }\n")
        lines.append("}\n")
        return lines

    def MapEnumerated(self, srcVar: str, dstVDMVariable: str, node: AsnEnumerated, __: AST_Leaftypes, ___: AST_Lookup) -> List[str]:  # pylint: disable=invalid-sequence-index
        lines = []  # type: List[str]
        lines.append("switch(%s) {\n" %srcVar)
        for m in node._members:
            lines.append("    case %s:\n" % m[1])
            lines.append("        (%s) = newQuote(QUOTE_%s);\n" % (dstVDMVariable, m[0].upper()))
            lines.append("        break;\n")
        lines.append("}\n")
        return lines

    def MapSequence(self, srcVar: str, dstVDMVariable: str, node: AsnSequenceOrSet, leafTypeDict: AST_Leaftypes, names: AST_Lookup) -> List[str]:  # pylint: disable=invalid-sequence-index
        lines = []  # type: List[str]
        for key in names:
            if names[key] == node:
                type_str = key  # type: str
        for child in node._members:
            lines.extend(
                self.Map(
                    srcVar + "." + self.CleanName(child[0]),
                    "TO_CLASS_PTR(%s, %s)->m_%s_%s" % (dstVDMVariable, type_str, type_str, self.CleanName(child[0])),
                    child[1],
                    leafTypeDict,
                    names))
        return lines

    def MapSet(self, srcVar: str, dstSDLVariable: str, node: AsnSequenceOrSet, leafTypeDict: AST_Leaftypes, names: AST_Lookup) -> List[str]:  # pylint: disable=invalid-sequence-index
        return self.MapSequence(srcVar, dstSDLVariable, node, leafTypeDict, names)  # pragma: nocover

    def MapChoice(self, srcVar, dstSDLVariable, node, leafTypeDict, names):
        lines = []  # type: List[str]
        childNo = 0
        for child in node._members:
            childNo += 1
            lines.append("%sif (%s.kind == %s) {\n" %
                         (self.maybeElse(childNo), srcVar, self.CleanName(child[2])))
            lines.extend(
                ['    ' + x
                 for x in self.Map(
                     srcVar + ".u." + self.CleanName(child[0]),
                     "%s.__value.%s" % (dstSDLVariable, self.CleanName(child[0])),
                     child[1],
                     leafTypeDict,
                     names)])
            lines.append("    %s.present = %d;\n" % (dstSDLVariable, childNo))
            lines.append("}\n")
        return lines
'''
    def MapSetOf(self, unused_srcVar, unused_dstSDLVariable, node, unused_leafTypeDict, unused_names):
        panic("The PragmaDev mapper does not support SETOF. Please use SEQUENCEOF instead (%s)" % node.Location())  # pragma: nocover
'''


class VDM_GlueGenerator(ASynchronousToolGlueGenerator):
    def __init__(self) -> None:
        ASynchronousToolGlueGenerator.__init__(self)
        self.FromVDMToASN1SCC = FromVDMToASN1SCC()
        self.FromASN1SCCtoVDM = FromASN1SCCtoVDM()

    def Version(self) -> None:
        print("Code generator: " + "$Id: vdm_B_mapper.py 2390 2015-07-04 12:39:17Z tfabbri $")

    def HeadersOnStartup(self, unused_asnFile: str, unused_outputDir: str, unused_maybeFVname: str) -> None:
        # Constant includes
        self.C_HeaderFile.write("#include <assert.h>\n")
        self.C_HeaderFile.write("#include \"%s.h\"\n" % self.asn_name)
        self.C_HeaderFile.write("#include \"Vdm.h\"\n")
        # Includes depending on the Asn data specification
        for i in g_modules:
            self.C_HeaderFile.write("#include \"%s.h\"\n" % i.replace('-', '_'))
        for i in g_names:
            if g_names[i]._leafType == 'SEQUENCE' or g_names[i]._leafType == 'SET':
                self.C_HeaderFile.write("#include \"%s.h\"\n"% i.replace('-', '_'))
        self.C_HeaderFile.write('\n')

    def Encoder(self, nodeTypename: str, node: AsnNode, leafTypeDict: AST_Leaftypes, names: AST_Lookup, encoding: str) -> None:
        if encoding.lower() in ["uper", "acn"]:
            return
        fileOutHeader = self.C_HeaderFile
        fileOutSource = self.C_SourceFile
        isPointer = True
        if isinstance(node, AsnBasicNode) or isinstance(node, AsnEnumerated):
            isPointer = False
        cleaned = self.CleanNameAsToolWants(nodeTypename)
        fileOutHeader.write(
            "void Convert_%s_from_VDM_to_ASN1SCC(asn1Scc%s *ptrASN1SCC, TVP %sVDM);\n" %
            (cleaned, cleaned, "*" if isPointer else ""))
        fileOutSource.write(
            "void Convert_%s_from_VDM_to_ASN1SCC(asn1Scc%s *ptrASN1SCC, TVP %sVDM)\n{\n" %
            (cleaned, cleaned, "*" if isPointer else ""))

        # Write the mapping code for the message
        if self.useOSS:
            print('useOSS')
            # lines = self.FromRTDSToOSS.Map(
            #    "(%sVDM)" % ("*" if isPointer else ""),
            #    "(*ptrASN1SCC)",
            #    node,
            #    leafTypeDict,
            #    names)
        else:
            lines = self.FromVDMToASN1SCC.Map(
                "(%sVDM)" % ("*" if isPointer else ""),
                "(*ptrASN1SCC)",
                node,
                leafTypeDict,
                names)

        lines = ["    " + x.rstrip() for x in lines]
        fileOutSource.write("\n".join(lines))
        fileOutSource.write("\n}\n\n")

    def Decoder(self, nodeTypename: str, node: AsnNode, leafTypeDict: AST_Leaftypes, names: AST_Lookup, encoding: str) -> None:
        if encoding.lower() in ["uper", "acn"]:
            return
        fileOutHeader = self.C_HeaderFile
        fileOutSource = self.C_SourceFile
        cleaned = self.CleanNameAsToolWants(nodeTypename)
        fileOutHeader.write(
            "void Convert_%s_from_ASN1SCC_to_VDM(TVP *ptrVDM, const asn1Scc%s *ptrASN1SCC);\n" %
            (cleaned, cleaned))

        fileOutSource.write(
            "void Convert_%s_from_ASN1SCC_to_VDM(TVP *ptrVDM, const asn1Scc%s *ptrASN1SCC)\n{\n" %
            (cleaned, cleaned))

        if self.useOSS:
            print('useOSS')
        #    lines = self.FromOSStoRTDS.Map(
        #        "(*ptrASN1SCC)",
        #        "(*ptrVDM)",
        #        node,
        #        leafTypeDict,
        #        names)
        else:
            lines = self.FromASN1SCCtoVDM.Map(
                "(*ptrASN1SCC)",
                "(*ptrVDM)",
                node,
                leafTypeDict,
                names)

        lines = ["    " + x.rstrip() for x in lines]
        fileOutSource.write("\n".join(lines))
        fileOutSource.write("\n}\n\n")


def OnStartup(modelingLanguage: str, asnFile: str, outputDir: str, maybeFVname: str, useOSS: bool) -> None:
    global vdmBackend
    vdmBackend = VDM_GlueGenerator()
    vdmBackend.OnStartup(modelingLanguage, asnFile, outputDir, maybeFVname, useOSS)


def OnBasic(nodeTypename: str, node: AsnBasicNode, leafTypeDict: AST_Leaftypes, names: AST_Lookup) -> None:
    vdmBackend.OnBasic(nodeTypename, node, leafTypeDict, names)


def OnSequence(nodeTypename: str, node: AsnSequence, leafTypeDict: AST_Leaftypes, names: AST_Lookup) -> None:
    vdmBackend.OnSequence(nodeTypename, node, leafTypeDict, names)


def OnSet(nodeTypename: str, node: AsnSet, leafTypeDict: AST_Leaftypes, names: AST_Lookup) -> None:
    vdmBackend.OnSet(nodeTypename, node, leafTypeDict, names)  # pragma: nocover


def OnEnumerated(nodeTypename: str, node: AsnEnumerated, leafTypeDict: AST_Leaftypes, names: AST_Lookup) -> None:
    vdmBackend.OnEnumerated(nodeTypename, node, leafTypeDict, names)


def OnSequenceOf(nodeTypename: str, node: AsnSequenceOf, leafTypeDict: AST_Leaftypes, names: AST_Lookup) -> None:
    vdmBackend.OnSequenceOf(nodeTypename, node, leafTypeDict, names)


def OnSetOf(nodeTypename: str, node: AsnSetOf, leafTypeDict: AST_Leaftypes, names: AST_Lookup) -> None:
    vdmBackend.OnSetOf(nodeTypename, node, leafTypeDict, names)  # pragma: nocover


def OnChoice(nodeTypename: str, node: AsnChoice, leafTypeDict: AST_Leaftypes, names: AST_Lookup) -> None:
    vdmBackend.OnChoice(nodeTypename, node, leafTypeDict, names)


def OnShutdown(modelingLanguage: str, asnFile: str, maybeFVname: str) -> None:
    vdmBackend.OnShutdown(modelingLanguage, asnFile, maybeFVname)
