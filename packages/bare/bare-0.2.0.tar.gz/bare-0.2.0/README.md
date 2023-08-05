# bare-py

Python implementation of [BARE](https://baremessages.org/). Work in progress.

## Example

The schema:

```bare
type PublicKey data<128>
type Time string # ISO 8601

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
	email: string
	address: Address
	orders: []{
		orderId: i64
		quantity: i32
	}
	metadata: map[string]data
}

type Employee {
	name: string
	email: string
	address: Address
	department: Department
	hireDate: Time
	publicKey: optional<PublicKey>
	metadata: map[string]data
}

type Person (Customer | Employee)

type Address {
	address: [4]string
	city: string
	state: string
	country: string
}
```

Generate `schema.py` with the `bare` command

```shell-session
$ bare schema.bare schema.py
```

### Packing data

```python
from schema import Customer, Address, Person

address = Address()
address.address = ["Address line 1", "", "", ""]
address.city = "The big city"
address.state = "Drenthe"
address.country = "The Netherlands"

customer = Customer()
customer.name = "Martijn Braam"
customer.email = "spam@example.org"
customer.address = address
customer.orders = [
    {'orderId': 5, 'quantity': 1},
    {'orderId': 6, 'quantity': 2}
]
customer.metadata = {
    'ssh': b'jafsl8dfaf2',
    'gpg': b'jofa8f2jdlasfj8'
}

# Write a Customer as a BARE encoded file
with open('example.bin', 'wb') as handle:
    handle.write(customer.pack())

# Write it as a Person instead, only works with tagged unions
with open('person.bin', 'wb') as handle:
    handle.write(Person.pack(customer))
```

```shell-session
$ xxd example.bin
00000000: 0d00 0000 4d61 7274 696a 6e20 4272 6161  ....Martijn Braa
00000010: 6d10 0000 0073 7061 6d40 6578 616d 706c  m....spam@exampl
00000020: 652e 6f72 670e 0000 0041 6464 7265 7373  e.org....Address
00000030: 206c 696e 6520 3100 0000 0000 0000 0000   line 1.........
00000040: 0000 000c 0000 0054 6865 2062 6967 2063  .......The big c
00000050: 6974 7907 0000 0044 7265 6e74 6865 0f00  ity....Drenthe..
00000060: 0000 5468 6520 4e65 7468 6572 6c61 6e64  ..The Netherland
00000070: 7302 0000 0005 0000 0000 0000 0001 0000  s...............
00000080: 0006 0000 0000 0000 0002 0000 0002 0000  ................
00000090: 0003 0000 0073 7368 0b00 0000 6a61 6673  .....ssh....jafs
000000a0: 6c38 6466 6166 3203 0000 0067 7067 0f00  l8dfaf2....gpg..
000000b0: 0000 6a6f 6661 3866 326a 646c 6173 666a  ..jofa8f2jdlasfj
000000c0: 38                                       8

```