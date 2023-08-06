import argparse
import base64
import sys
import imp
import shutil
import textwrap
from enum import EnumMeta
from itertools import zip_longest as zipl

from bare import _unpack_primitive
from bare.__main__ import codegen
from bare.bare_ast import BareType, UnionType, BarePrimitive, TypeKind, StructType, MapType, NamedType, ArrayType, \
    OptionalType


class Line:
    def __init__(self, data, annotation, decoded, indent):
        self.data = data
        self.annotation = ('|' * indent) + annotation
        self.decoded = decoded
        self.indent = indent
        self.hex = ''
        for i, b in enumerate(data):
            self.hex += '{:02X} '.format(b)
            if i % 8 == 7:
                self.hex += '\n'

    def __str__(self):
        size = shutil.get_terminal_size((120, 20))
        hexwidth = 8 * 3
        annotatewidth = 24
        decodedwidth = size.columns - hexwidth - annotatewidth - 4

        hexlines = self.hex.splitlines()
        annotatelines = [self.annotation]
        decodedlines = textwrap.wrap(self.decoded, decodedwidth)

        maxlines = max(len(hexlines), len(annotatelines), len(decodedlines))
        if len(annotatelines) < maxlines:
            annotatelines += ['|' * self.indent] * (maxlines - len(annotatelines))

        result = ''
        for hex, ann, dec in zipl(hexlines, annotatelines, decodedlines, fillvalue=''):
            result += ann.ljust(annotatewidth) + '  ' + hex.ljust(hexwidth) + '  ' + dec + "\n"
        return result


def import_schema(schema):
    code = codegen(schema, None, '\t')
    schema_module = imp.new_module('schema')
    exec(code, schema_module.__dict__)
    sys.modules['schema'] = schema_module
    return schema_module


def dump(data, type, module, name):
    node = type._ast
    label = name
    offset = 0
    nodelist = []
    indent = 0
    while True:
        if hasattr(node, '_ast') and isinstance(node._ast, StructType):
            yield Line(b'', 'struct {}'.format(label), '', indent)
            end_offset = offset

            newnodes = []
            for fieldname in node._ast.fields:
                newnodes.append((node._ast.fields[fieldname], fieldname))
            nodelist = newnodes + [(None, None)] + nodelist
            indent += 1
        elif isinstance(node, StructType):
            yield Line(b'', 'struct {}'.format(label), '', indent)
            end_offset = offset

            newnodes = []
            for fieldname in node.fields:
                newnodes.append((node.fields[fieldname], fieldname))
            nodelist = newnodes + [(None, None)] + nodelist
            indent += 1
        elif hasattr(node, '_ast') and isinstance(node._ast, BarePrimitive):
            nodelist = [(node._ast, label)] + nodelist
        elif isinstance(node, UnionType):
            tag, end_offset = _unpack_primitive(BarePrimitive(TypeKind.UINT), data, offset)
            for type in node.types:
                if type.value == tag:
                    break
            else:
                raise ValueError("Cannot find type for tag {}".format(tag))
            if isinstance(type.type, BarePrimitive):
                name = type.type.type.name
            else:
                name = type.type.name
            yield Line(data[offset:end_offset], label, 'union, tag = {} ({})'.format(tag, name), indent)
            if isinstance(type.type, BarePrimitive):
                nodelist = [(type.type, name), (None, None)] + nodelist
            else:
                nodelist = [(getattr(module, type.type.name), type.type.name), (None, None)] + nodelist
            indent += 1
        elif isinstance(node, BarePrimitive):
            value, end_offset = _unpack_primitive(node, data, offset)
            if node.length is None:
                dec = '{} = {}'.format(node.type.name, value)
            else:
                dec = '{}<{}> = {}'.format(node.type.name, node.length, value)
            yield Line(data[offset:end_offset], label, dec, indent)
        elif isinstance(node, NamedType):
            referenced = getattr(module, node.name)
            if isinstance(referenced, EnumMeta):
                value, end_offset = _unpack_primitive(BarePrimitive(TypeKind.UINT), data, offset)
                enum = referenced(value)
                yield Line(data[offset:end_offset], label, str(enum), indent)
            else:
                newnode = (referenced, label)
                nodelist = [newnode] + nodelist
                end_offset = offset
        elif isinstance(node, ArrayType):
            if node.length is None:
                length, end_offset = _unpack_primitive(BarePrimitive(TypeKind.UINT), data, offset)
                dec = '[]{}, length = {}'.format(node.subtype.name, length)
            else:
                end_offset = offset
                length = node.length
                dec = '[{}]{}'.format(length, node.subtype.type.name)
            yield Line(data[offset:end_offset], label, dec, indent)
            if length > 0:
                newnodes = []
                for i in range(0, length):
                    newnodes.append((node.subtype, str(i)))
                nodelist = newnodes + [(None, None)] + nodelist
                indent += 1
        elif isinstance(node, OptionalType):
            exists, end_offset = _unpack_primitive(BarePrimitive(TypeKind.UINT), data, offset)
            yield Line(data[offset:end_offset], label, 'optional, value = {}'.format(exists != 0), indent)
            if exists:
                nodelist = [(node.subtype, 'value'), (None, None)] + nodelist
                indent += 1
        elif isinstance(node, MapType):
            length, end_offset = _unpack_primitive(BarePrimitive(TypeKind.UINT), data, offset)
            dec = 'map[{}]{}, length = {}'.format(node.keytype.type.name, node.valuetype.type.name, length)
            yield Line(data[offset:end_offset], label, dec, indent)
            if length > 0:
                newnodes = []
                for i in range(0, length):
                    newnodes.append((node.keytype, 'key {}'.format(i)))
                    newnodes.append((node.valuetype, 'value {}'.format(i)))
                nodelist = newnodes + [(None, None)] + nodelist
                indent += 1

        elif node is None:
            indent -= 1
        else:
            break

        if len(nodelist) == 0:
            return

        offset = end_offset
        node = nodelist[0][0]
        label = nodelist[0][1]
        nodelist = nodelist[1:]


def main():
    parser = argparse.ArgumentParser(description="BARE message debugger")
    parser.add_argument('schema', type=open)
    parser.add_argument('type')
    parser.add_argument('--base64', '-b', action='store_true')
    parser.add_argument('message')
    args = parser.parse_args()

    if args.base64:
        message = base64.b64decode(args.message)
    else:
        if args.message == '-':
            args.message = sys.stdin
        with open(args.message, 'rb') as handle:
            message = handle.read()

    schema = import_schema(args.schema.read())
    type = getattr(schema, args.type)

    for line in dump(message, type, schema, args.type):
        print(line, end='')


if __name__ == '__main__':
    main()
