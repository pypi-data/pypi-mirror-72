from math import isnan
from unittest import TestCase

from hypothesis import given, note, seed
from hypothesis.strategies import integers, floats, booleans, binary, tuples, text

from bare import _pack_primitive, _unpack_primitive, BarePrimitive, TypeKind


class Test(TestCase):
    @given(integers(min_value=0, max_value=255))
    def test_u8(self, number):
        ast = BarePrimitive(TypeKind.U8)
        packed = _pack_primitive(ast, number)
        note(packed)
        result = _unpack_primitive(ast, packed, 0)[0]
        assert result == number

    @given(integers(min_value=0, max_value=65535))
    def test_u16(self, number):
        ast = BarePrimitive(TypeKind.U16)
        packed = _pack_primitive(ast, number)
        note(packed)
        result = _unpack_primitive(ast, packed, 0)[0]
        assert result == number

    @given(integers(min_value=0, max_value=4294967296))
    def test_u32(self, number):
        ast = BarePrimitive(TypeKind.U32)
        packed = _pack_primitive(ast, number)
        note(packed)
        result = _unpack_primitive(ast, packed, 0)[0]
        assert result == number

    @given(integers(min_value=0, max_value=18446744073709551615))
    def test_u64(self, number):
        ast = BarePrimitive(TypeKind.U64)
        packed = _pack_primitive(ast, number)
        note(packed)
        result = _unpack_primitive(ast, packed, 0)[0]
        assert result == number

    @given(integers(min_value=0))
    def test_uint(self, number):
        ast = BarePrimitive(TypeKind.UINT)
        packed = _pack_primitive(ast, number)
        note(packed)
        result = _unpack_primitive(ast, packed, 0)[0]
        assert result == number

    @given(integers(min_value=-128, max_value=127))
    def test_i8(self, number):
        ast = BarePrimitive(TypeKind.I8)
        packed = _pack_primitive(ast, number)
        note(packed)
        result = _unpack_primitive(ast, packed, 0)[0]
        assert result == number

    @given(integers(min_value=-32768, max_value=32767))
    def test_i16(self, number):
        ast = BarePrimitive(TypeKind.I16)
        packed = _pack_primitive(ast, number)
        note(packed)
        result = _unpack_primitive(ast, packed, 0)[0]
        assert result == number

    @given(integers(min_value=-2147483648, max_value=2147483647))
    def test_i32(self, number):
        ast = BarePrimitive(TypeKind.I32)
        packed = _pack_primitive(ast, number)
        note(packed)
        result = _unpack_primitive(ast, packed, 0)[0]
        assert result == number

    @given(integers(min_value=-9223372036854775808, max_value=9223372036854775807))
    def test_i64(self, number):
        ast = BarePrimitive(TypeKind.I64)
        packed = _pack_primitive(ast, number)
        note(packed)
        result = _unpack_primitive(ast, packed, 0)[0]
        assert result == number

    @given(integers())
    def test_i64(self, number):
        ast = BarePrimitive(TypeKind.INT)
        packed = _pack_primitive(ast, number)
        note(packed)
        result = _unpack_primitive(ast, packed, 0)[0]
        assert result == number

    @given(floats(width=32))
    def test_f32(self, number):
        ast = BarePrimitive(TypeKind.F32)
        packed = _pack_primitive(ast, number)
        note(repr(packed))
        result = _unpack_primitive(ast, packed, 0)[0]
        note(result)
        if isnan(number):
            assert isnan(result)
        else:
            assert result == number

    @given(floats(width=64))
    def test_f64(self, number):
        ast = BarePrimitive(TypeKind.F64)
        packed = _pack_primitive(ast, number)
        note(repr(packed))
        result = _unpack_primitive(ast, packed, 0)[0]
        note(result)
        if isnan(number):
            assert isnan(result)
        else:
            assert result == number

    @given(booleans())
    def test_bool(self, bool):
        ast = BarePrimitive(TypeKind.Bool)
        packed = _pack_primitive(ast, bool)
        note(repr(packed))
        result = _unpack_primitive(ast, packed, 0)[0]
        note(result)
        assert result == bool

    @given(binary())
    def test_data(self, data):
        ast = BarePrimitive(TypeKind.Data)
        packed = _pack_primitive(ast, data)
        note(repr(packed))
        result = _unpack_primitive(ast, packed, 0)[0]
        note(result)
        assert result == data

    @given(tuples(binary(max_size=128), integers(min_value=1, max_value=128)).filter(
        lambda x: len(x[0]) <= x[1]))
    def test_datafixed(self, testdata):
        data, length = testdata
        ast = BarePrimitive(TypeKind.DataFixed, length=length)
        packed = _pack_primitive(ast, data)
        note('packed: {}'.format(repr(packed)))
        result = _unpack_primitive(ast, packed, 0)[0]
        note('unpacked: {}'.format(repr(result)))
        note('input pa: {}'.format(repr(data.ljust(length, b'\0'))))
        assert result == data.ljust(length, b'\0')

    @given(text())
    def test_string(self, data):
        ast = BarePrimitive(TypeKind.String)
        packed = _pack_primitive(ast, data)
        note(repr(packed))
        result = _unpack_primitive(ast, packed, 0)[0]
        note(result)
        assert result == data

    def test_void(self):
        ast = BarePrimitive(TypeKind.Void)
        packed = _pack_primitive(ast, None)
        result = _unpack_primitive(ast, packed, 0)[0]
        assert result == None
