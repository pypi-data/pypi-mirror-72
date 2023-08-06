from unittest import TestCase

from hypothesis import given, note, seed, example
from hypothesis.strategies import integers, lists, text, dictionaries

from bare import BarePrimitive, TypeKind, OptionalType, _pack_type, _unpack_type, ArrayType, MapType


class Test(TestCase):

    @given(integers(min_value=0, max_value=255))
    @example(None)
    def test_optional(self, number):
        ast = OptionalType(BarePrimitive(TypeKind.U8))
        packed = _pack_type(ast, number, None)
        note(repr(packed))
        result = _unpack_type(ast, None, None, packed, 0)[0]
        note("result: {}".format(repr(result)))
        assert result == number

    @given(lists(integers(min_value=0, max_value=255)))
    def test_array_fixedsubtype(self, numbers):
        ast = ArrayType(BarePrimitive(TypeKind.U8))
        packed = _pack_type(ast, numbers, None)
        note(repr(packed))
        result = _unpack_type(ast, None, None, packed, 0)[0]
        note("result: {}".format(repr(result)))
        assert result == numbers

    @given(lists(text()))
    def test_array_nonfixedsubtype(self, texts):
        ast = ArrayType(BarePrimitive(TypeKind.String))
        packed = _pack_type(ast, texts, None)
        note(repr(packed))
        result = _unpack_type(ast, None, None, packed, 0)[0]
        note("result: {}".format(repr(result)))
        assert result == texts

    @given(lists(integers(min_value=0, max_value=255), min_size=64, max_size=64))
    def test_fixedarray_fixedsubtype(self, numbers):
        ast = ArrayType(BarePrimitive(TypeKind.U8), length=64)
        packed = _pack_type(ast, numbers, None)
        note(repr(packed))
        result = _unpack_type(ast, None, None, packed, 0)[0]
        note("result: {}".format(repr(result)))
        assert result == numbers

    @given(lists(text(), min_size=32, max_size=32))
    def test_fixedarray_nonfixedsubtype(self, texts):
        ast = ArrayType(BarePrimitive(TypeKind.String), length=32)
        packed = _pack_type(ast, texts, None)
        note(repr(packed))
        result = _unpack_type(ast, None, None, packed, 0)[0]
        note("result: {}".format(repr(result)))
        assert result == texts

    @given(dictionaries(integers(min_value=0, max_value=255), text()))
    def test_map_int_string(self, map):
        ast = MapType(BarePrimitive(TypeKind.U8), BarePrimitive(TypeKind.String))
        packed = _pack_type(ast, map, None)
        note(repr(packed))
        result = _unpack_type(ast, None, None, packed, 0)[0]
        note("result: {}".format(repr(result)))
        assert result == map

    @given(dictionaries(text(), text()))
    def test_map_string_string(self, map):
        ast = MapType(BarePrimitive(TypeKind.String), BarePrimitive(TypeKind.String))
        packed = _pack_type(ast, map, None)
        note(repr(packed))
        result = _unpack_type(ast, None, None, packed, 0)[0]
        note("result: {}".format(repr(result)))
        assert result == map
