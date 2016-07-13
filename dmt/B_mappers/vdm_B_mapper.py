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
This is the code generator for the PragmaDev RTDS code mappers.
This backend is called by aadl2glueC, when an RTDS subprogram
is identified in the input concurrency view.

Implementation notes: Like OG, RTDS is a complex case;
It is used to model asynchronous processes (SDL)...

'''

# from ..commonPy.utility import panic
from ..commonPy.asnAST import isSequenceVariable, sourceSequenceLimit, AsnBasicNode, AsnEnumerated

from ..commonPy.recursiveMapper import RecursiveMapper
from .asynchronousTool import ASynchronousToolGlueGenerator

from . import c_B_mapper

isAsynchronous = True
rtdsBackend = None
cBackend = None
vdmBackend = None


def Version():
    print("Code generator: " + "$Id: vdm_B_mapper.py 2390 2015-07-04 12:39:17Z tfabbri $")


# noinspection PyListCreation
# pylint: disable=no-self-use
class FromVDMToASN1SCC(RecursiveMapper):
    def __init__(self):
        self.uniqueID = 0

    def UniqueID(self):
        self.uniqueID += 1
        return self.uniqueID

    def DecreaseUniqueID(self):
        self.uniqueID -= 1

    def MapInteger(self, srcVDMVariable, destVar, _, __, ___):
        return ["%s = (asn1SccSint)((TVP) %s)->value.intVal;\n" % (destVar, srcVDMVariable)]

    def MapBoolean(self, srcVDMVariable, destVar, _, __, ___):
        return ["%s = (%s->value.boolVal==true)?0xff:0;\n" % (destVar, srcVDMVariable)]

    def MapReal(self, srcVDMVariable, destVar, _, __, ___):
        return ["%s = ((TVP) %s)->value.doubleVal;\n" % (destVar, srcVDMVariable)]

    def MapSequenceOf(self, srcVDMVariable, destVar, node, leafTypeDict, names):
        lines = []  # type: List[str]
        lines.append("{\n")
        uniqueId = self.UniqueID()
        lines.append("    int i%s;\n" % uniqueId)
        lines.append("    UNWRAP_COLLECTION(col, %s);" % srcVDMVariable)
        lines.append("    int size%s = col->size;" % uniqueId)
        lines.append("    for(i%s=0; i%s<size%s; i%s++) {\n" % (uniqueId, uniqueId, uniqueId, uniqueId))
        lines.extend(
            ["        " + x
             for x in self.Map(
                 "col->value[i%s]" % uniqueId,
                 "%s.arr[i%s]" % (destVar, uniqueId),
                 node._containedType,
                 leafTypeDict,
                 names)])
        lines.append("    }\n")
        if isSequenceVariable(node):
            lines.append("    %s.nCount = size%s;\n" % (destVar, uniqueId))
        lines.append("}\n")
        self.DecreaseUniqueID()
        return lines

    def MapOctetString(self, srcVDMVariable, destVar, node, __, ___):
        lines = []  # type: List[str]
        lines.append("{\n")
        lines.append("    int i;\n")
        lines.append("    UNWRAP_COLLECTION(col, %s);" % srcVDMVariable)
        lines.append("    int size = col->size;")
        lines.append("    for(i=0; i<size; i++) {\n")
        lines.append("        %s.arr[i] = col->value[i]->value.charVal;\n" % destVar)
        lines.append("    }\n")
        # for i in xrange(0, node._range[-1]):
        #     lines.append("    placeHolder[%d] = %s[%d];\n" % (i, srcSDLVariable, i))
        if isSequenceVariable(node):
            lines.append("    %s.nCount = size;\n" % destVar)
        lines.append("}\n")
        return lines

    def MapEnumerated(self, srcVDMVariable, destVar, node, _, __):
        lines = []
        lines.append("switch(%s) {\n" %srcVDMVariable)
        for m in node._members:
            lines.append("    case QUOTE_%s:\n" % m[0].upper())
            lines.append("        (%s) = %s;\n" % (destVar, m[1]))
            lines.append("        break;\n")
        lines.append("}\n")
        return lines

    def MapSequence(self, srcVDMVariable, destVar, node, leafTypeDict, names):
        lines = []  # type: List[str]
        for child in node._members:
            lines.extend(
                self.Map(
                    "%s.%s" % (srcVDMVariable, self.CleanName(child[0])),
                    destVar + "." + self.CleanName(child[0]),
                    child[1],
                    leafTypeDict,
                    names))
        return lines

    def MapSet(self, srcVDMVariable, destVar, node, leafTypeDict, names):
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
    def __init__(self):
        self.uniqueID = 0

    def UniqueID(self):
        self.uniqueID += 1
        return self.uniqueID

    def DecreaseUniqueID(self):
        self.uniqueID -= 1

    def MapInteger(self, srcVar, dstVDMVariable, _, __, ___):
        return ["%s = newInt(%s);\n" % (dstVDMVariable, srcVar)]

    def MapBoolean(self, srcVar, dstVDMVariable, _, __, ___):
        return ["%s = (%s)?newBool(true):newBool(false);\n" % (dstVDMVariable, srcVar)]

    def MapReal(self, srcVar, dstSDLVariable, _, __, ___):
        return ["%s = newReal(%s);\n" % (dstSDLVariable, srcVar)]

    def MapSequenceOf(self, srcVar, dstVDMVariable, node, leafTypeDict, names):
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

    def MapOctetString(self, srcVar, dstVDMVariable, node, _, __):
        # for i in xrange(0, node._range[-1]):
        #     lines.append("%s[%d] = %s->buf[%d];\n" % (dstSDLVariable, i, srcVar, i))
        lines = []  # type: List[str]
        limit = sourceSequenceLimit(node, srcVar)
        lines.append("{\n")
        lines.append("    int i;\n")
        lines.append("    UNWRAP_COLLECTION(col, %s);" % dstVDMVariable)
        lines.append("    for(i=0; i<%s; i++) {\n" % limit)
        lines.append("        col->value[i] = newChar(%s.arr[i]);\n" % (srcVar))
        lines.append("    }\n")
        lines.append("}\n")
        return lines

    def MapEnumerated(self, srcVar, dstVDMVariable, node, _, __):
        lines = []
        lines.append("switch(%s) {\n" %srcVar)
        for m in node._members:
            lines.append("    case %s:\n" % m[1])
            lines.append("        (%s) = newQuote(QUOTE_%s);\n" % (dstVDMVariable, m[0].upper()))
            lines.append("        break;\n")
        lines.append("}\n")
        return lines

    def MapSequence(self, srcVar, dstVDMVariable, node, leafTypeDict, names):
        lines = []  # type: List[str]
        for child in node._members:
            lines.extend(
                self.Map(
                    srcVar + "." + self.CleanName(child[0]),
                    "%s.%s" % (dstVDMVariable, self.CleanName(child[0])),
                    child[1],
                    leafTypeDict,
                    names))
        return lines

    def MapSet(self, srcVar, dstSDLVariable, node, leafTypeDict, names):
        return self.MapSequence(srcVar, dstSDLVariable, node, leafTypeDict, names)  # pragma: nocover
'''
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

    def MapSetOf(self, unused_srcVar, unused_dstSDLVariable, node, unused_leafTypeDict, unused_names):
        panic("The PragmaDev mapper does not support SETOF. Please use SEQUENCEOF instead (%s)" % node.Location())  # pragma: nocover
'''


class VDM_GlueGenerator(ASynchronousToolGlueGenerator):
    def __init__(self):
        ASynchronousToolGlueGenerator.__init__(self)
        self.FromVDMToASN1SCC = FromVDMToASN1SCC()
        self.FromASN1SCCtoVDM = FromASN1SCCtoVDM()

    def Version(self):
        print("Code generator: " + "$Id: vdm_B_mapper.py 2390 2015-07-04 12:39:17Z tfabbri $")

    def HeadersOnStartup(self, unused_asnFile, unused_outputDir, unused_maybeFVname):
        print(unused_asnFile)

        self.C_HeaderFile.write("#include <assert.h>\n\n")
        self.C_HeaderFile.write("#include \"%s.h\"\n" % self.asn_name)
        self.C_HeaderFile.write("#include \"Vdm.h\"\n\n")

    def Encoder(self, nodeTypename, node, leafTypeDict, names, encoding):
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

    def Decoder(self, nodeTypename, node, leafTypeDict, names, encoding):
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


def OnStartup(modelingLanguage, asnFile, outputDir, maybeFVname, useOSS):
    global vdmBackend
    vdmBackend = VDM_GlueGenerator()
    vdmBackend.OnStartup(modelingLanguage, asnFile, outputDir, maybeFVname, useOSS)
    global cBackend
    cBackend = c_B_mapper.C_GlueGenerator()
    cBackend.OnStartup("C", asnFile, outputDir, maybeFVname, useOSS)


def OnBasic(nodeTypename, node, leafTypeDict, names):
    vdmBackend.OnBasic(nodeTypename, node, leafTypeDict, names)
    cBackend.OnBasic(nodeTypename, node, leafTypeDict, names)


def OnSequence(nodeTypename, node, leafTypeDict, names):
    vdmBackend.OnSequence(nodeTypename, node, leafTypeDict, names)
    cBackend.OnSequence(nodeTypename, node, leafTypeDict, names)


def OnSet(nodeTypename, node, leafTypeDict, names):
    vdmBackend.OnSet(nodeTypename, node, leafTypeDict, names)  # pragma: nocover
    cBackend.OnSet(nodeTypename, node, leafTypeDict, names)  # pragma: nocover


def OnEnumerated(nodeTypename, node, leafTypeDict, names):
    vdmBackend.OnEnumerated(nodeTypename, node, leafTypeDict, names)
    cBackend.OnEnumerated(nodeTypename, node, leafTypeDict, names)


def OnSequenceOf(nodeTypename, node, leafTypeDict, names):
    vdmBackend.OnSequenceOf(nodeTypename, node, leafTypeDict, names)
    cBackend.OnSequenceOf(nodeTypename, node, leafTypeDict, names)


def OnSetOf(nodeTypename, node, leafTypeDict, names):
    vdmBackend.OnSetOf(nodeTypename, node, leafTypeDict, names)  # pragma: nocover
    cBackend.OnSetOf(nodeTypename, node, leafTypeDict, names)  # pragma: nocover


def OnChoice(nodeTypename, node, leafTypeDict, names):
    vdmBackend.OnChoice(nodeTypename, node, leafTypeDict, names)
    cBackend.OnChoice(nodeTypename, node, leafTypeDict, names)


def OnShutdown(modelingLanguage, asnFile, maybeFVname):
    vdmBackend.OnShutdown(modelingLanguage, asnFile, maybeFVname)
    cBackend.OnShutdown("C", asnFile, maybeFVname)
