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
00000000: 0d4d 6172 7469 6a6e 2042 7261 616d 1073  .Martijn Braam.s
00000010: 7061 6d40 6578 616d 706c 652e 6f72 670e  pam@example.org.
00000020: 4164 6472 6573 7320 6c69 6e65 2031 0000  Address line 1..
00000030: 000c 5468 6520 6269 6720 6369 7479 0744  ..The big city.D
00000040: 7265 6e74 6865 0f54 6865 204e 6574 6865  renthe.The Nethe
00000050: 726c 616e 6473 0205 0000 0000 0000 0001  rlands..........
00000060: 0000 0006 0000 0000 0000 0002 0000 0002  ................
00000070: 0373 7368 0b6a 6166 736c 3864 6661 6632  .ssh.jafsl8dfaf2
00000080: 0367 7067 0f6a 6f66 6138 6632 6a64 6c61  .gpg.jofa8f2jdla
00000090: 7366 6a38                                sfj8

```

### Unpacking data

```python
from schema import Address

with open('address.bin', 'rb') as handle:
    raw = handle.read()

address = Address.unpack(raw)
print(address.city)
```