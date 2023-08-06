from unittest import TestCase

from bare.bare_ast import BareType, TypeKind, BarePrimitive, BareEnum, StructType, NamedType
from bare.lex import lex_schema, LexedToken, Token
from bare.parser import parse


class Test(TestCase):
    def test_basic_parsing(self):
        schema = """
        type PublicRSAKey data<128>
        type PublicED25519Key data<32>
        type Time string # ISO 8601
        type Unemployed void
        
        enum Department {
            ACCOUNTING
            ADMINISTRATION
            CUSTOMER_SERVICE = 10
            DEVELOPMENT
        
            # Reserved for the CEO
            JSMITH = 99
        }
        
        type Customer {
            name: string
            address: Address
            orders: []{
                orderId: i64
                quantity: i32
            }
            metadata: map[string]data
        }
        
        type Employee {
            name: string
            address: Address
            department: Department
            hireDate: Time
            publicKey: optional<(PublicRSAKey|PublicED25519Key)>
            metadata: map[string]data
        }
        
        type Person (Customer | Employee | Unemployed)
        
        type Address {
            address: [4]string
            city: string
        }
        """

        types = parse(schema)

        # type PublicRSAKey data<128>
        type = types[0]
        types = types[1:]
        self.assertIsInstance(type, BareType)
        self.assertEqual("PublicRSAKey", type.name)
        self.assertIsInstance(type.type, BarePrimitive)
        self.assertEqual(TypeKind.DataFixed, type.type.type)
        self.assertEqual(128, type.type.length)

        # type PublicED25519Key data<32>
        type = types[0]
        types = types[1:]
        self.assertIsInstance(type, BareType)
        self.assertEqual("PublicED25519Key", type.name)
        self.assertIsInstance(type.type, BarePrimitive)
        self.assertEqual(TypeKind.DataFixed, type.type.type)
        self.assertEqual(32, type.type.length)

        # type Time string # ISO 8601
        type = types[0]
        types = types[1:]
        self.assertIsInstance(type, BareType)
        self.assertEqual("Time", type.name)
        self.assertIsInstance(type.type, BarePrimitive)
        self.assertEqual(TypeKind.String, type.type.type)
        self.assertEqual(None, type.type.length)

        # type Unemployed void
        type = types[0]
        types = types[1:]
        self.assertIsInstance(type, BareType)
        self.assertEqual("Unemployed", type.name)
        self.assertIsInstance(type.type, BarePrimitive)
        self.assertEqual(TypeKind.Void, type.type.type)
        self.assertEqual(None, type.type.length)

        # enum Department
        type = types[0]
        types = types[1:]
        self.assertIsInstance(type, BareEnum)
        self.assertEqual("Department", type.name)
        self.assertEqual("ACCOUNTING", type.values[0].name)
        self.assertEqual("ADMINISTRATION", type.values[1].name)
        self.assertEqual("CUSTOMER_SERVICE", type.values[2].name)
        self.assertEqual("DEVELOPMENT", type.values[3].name)
        self.assertEqual("JSMITH", type.values[4].name)
        self.assertEqual(0, type.values[0].value)
        self.assertEqual(1, type.values[1].value)
        self.assertEqual(10, type.values[2].value)
        self.assertEqual(11, type.values[3].value)
        self.assertEqual(99, type.values[4].value)

        # type Customer
        type = types[0]
        types = types[1:]
        self.assertIsInstance(type, BareType)
        self.assertEqual("Customer", type.name)
        self.assertIsInstance(type.type, StructType)
        self.assertIn('name', type.type.fields)
        self.assertIn('address', type.type.fields)
        self.assertIn('orders', type.type.fields)
        self.assertIn('metadata', type.type.fields)
        self.assertIsInstance(type.type.fields['name'], BarePrimitive)
        self.assertEqual(TypeKind.String, type.type.fields['name'].type)
        self.assertEqual(None, type.type.fields['name'].length)
        self.assertIsInstance(type.type.fields['address'], NamedType)
        self.assertEqual("Address", type.type.fields['address'].name)

        pass
