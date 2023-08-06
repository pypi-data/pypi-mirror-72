from unittest import TestCase

from bare.lex import lex_schema, LexedToken, Token


class Test(TestCase):
    def test_basic_lexing(self):
        schema = """
        type PublicRSAKey data<128>
        type PublicED25519Key data<32>
        type Time string # ISO 8601
        type Unemployed void
        
        enum Department {
            ACCOUNTING
            ADMINISTRATION
            CUSTOMER_SERVICE
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

        tokens = list(lex_schema(schema))
        expected = [
            (Token.TTYPE, ""),
            (Token.TNAME, "PublicRSAKey"),
            (Token.TDATA, ""),
            (Token.TLANGLE, ""),
            (Token.TINTEGER, "128"),
            (Token.TRANGLE, ""),
            (Token.TTYPE, ""),
            (Token.TNAME, "PublicED25519Key"),
            (Token.TDATA, ""),
            (Token.TLANGLE, ""),
            (Token.TINTEGER, "32"),
            (Token.TRANGLE, ""),
            (Token.TTYPE, ""),
            (Token.TNAME, "Time"),
            (Token.TSTRING, ""),
            (Token.TTYPE, ""),
            (Token.TNAME, "Unemployed"),
            (Token.TVOID, ""),

            (Token.TENUM, ""),
            (Token.TNAME, "Department"),
            (Token.TLBRACE, ""),
            (Token.TNAME, "ACCOUNTING"),
            (Token.TNAME, "ADMINISTRATION"),
            (Token.TNAME, "CUSTOMER_SERVICE"),
            (Token.TNAME, "DEVELOPMENT"),
            (Token.TNAME, "JSMITH"),
            (Token.TEQUAL, ""),
            (Token.TINTEGER, "99"),
            (Token.TRBRACE, ""),

            (Token.TTYPE, ""),
            (Token.TNAME, "Customer"),
            (Token.TLBRACE, ""),
            (Token.TNAME, "name"),
            (Token.TCOLON, ""),
            (Token.TSTRING, ""),
            (Token.TNAME, "address"),
            (Token.TCOLON, ""),
            (Token.TNAME, "Address"),
            (Token.TNAME, "orders"),
            (Token.TCOLON, ""),
            (Token.TLBRACKET, ""),
            (Token.TRBRACKET, ""),
            (Token.TLBRACE, ""),
            (Token.TNAME, "orderId"),
            (Token.TCOLON, ""),
            (Token.TI64, ""),
            (Token.TNAME, "quantity"),
            (Token.TCOLON, ""),
            (Token.TI32, ""),
            (Token.TRBRACE, ""),
            (Token.TNAME, "metadata"),
            (Token.TCOLON, ""),
            (Token.TMAP, ""),
            (Token.TLBRACKET, ""),
            (Token.TSTRING, ""),
            (Token.TRBRACKET, ""),
            (Token.TDATA, ""),
            (Token.TRBRACE, ""),

            (Token.TTYPE, ""),
            (Token.TNAME, "Employee"),
            (Token.TLBRACE, ""),
            (Token.TNAME, "name"),
            (Token.TCOLON, ""),
            (Token.TSTRING, ""),
            (Token.TNAME, "address"),
            (Token.TCOLON, ""),
            (Token.TNAME, "Address"),
            (Token.TNAME, "department"),
            (Token.TCOLON, ""),
            (Token.TNAME, "Department"),
            (Token.TNAME, "hireDate"),
            (Token.TCOLON, ""),
            (Token.TNAME, "Time"),
            (Token.TNAME, "publicKey"),
            (Token.TCOLON, ""),
            (Token.TOPTIONAL, ""),
            (Token.TLANGLE, ""),
            (Token.TLPAREN, ""),
            (Token.TNAME, "PublicRSAKey"),
            (Token.TPIPE, ""),
            (Token.TNAME, "PublicED25519Key"),
            (Token.TRPAREN, ""),
            (Token.TRANGLE, ""),
            (Token.TNAME, "metadata"),
            (Token.TCOLON, ""),
            (Token.TMAP, ""),
            (Token.TLBRACKET, ""),
            (Token.TSTRING, ""),
            (Token.TRBRACKET, ""),
            (Token.TDATA, ""),
            (Token.TRBRACE, ""),

            (Token.TTYPE, ""),
            (Token.TNAME, "Person"),
            (Token.TLPAREN, ""),
            (Token.TNAME, "Customer"),
            (Token.TPIPE, ""),
            (Token.TNAME, "Employee"),
            (Token.TPIPE, ""),
            (Token.TNAME, "Unemployed"),
            (Token.TRPAREN, ""),

            (Token.TTYPE, ""),
            (Token.TNAME, "Address"),
            (Token.TLBRACE, ""),
            (Token.TNAME, "address"),
            (Token.TCOLON, ""),
            (Token.TLBRACKET, ""),
            (Token.TINTEGER, "4"),
            (Token.TRBRACKET, ""),
            (Token.TSTRING, ""),
            (Token.TNAME, "city"),
            (Token.TCOLON, ""),
            (Token.TSTRING, ""),
            (Token.TRBRACE, ""),
        ]

        self.assertEqual(len(expected), len(tokens), "number of tokens")
        for token, exp in zip(tokens, expected):
            self.assertEqual(token.token, exp[0])
            self.assertEqual(token.value, exp[1])
