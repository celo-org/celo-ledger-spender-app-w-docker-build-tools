#!/usr/bin/env python
"""
*******************************************************************************
*   Ledger Ethereum App
*   (c) 2016-2019 Ledger
*
*  Licensed under the Apache License, Version 2.0 (the "License");
*  you may not use this file except in compliance with the License.
*  You may obtain a copy of the License at
*
*      http://www.apache.org/licenses/LICENSE-2.0
*
*  Unless required by applicable law or agreed to in writing, software
*  distributed under the License is distributed on an "AS IS" BASIS,
*  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
*  See the License for the specific language governing permissions and
*  limitations under the License.
********************************************************************************
"""
from __future__ import print_function

from ledgerblue.comm import getDongle
from ledgerblue.commException import CommException
from decimal import Decimal
import argparse
import struct
import binascii
from ethBase import Transaction, UnsignedTransaction, unsigned_tx_from_tx
from rlp import encode

# Define here Chain_ID for EIP-155
CHAIN_ID = 0

try:
    from rlp.utils import decode_hex, encode_hex, str_to_bytes
except:
    #Python3 hack import for pyethereum
    from ethereum.utils import decode_hex, encode_hex, str_to_bytes

def parse_bip32_path(path):
    if len(path) == 0:
        return b""
    result = b""
    elements = path.split('/')
    for pathElement in elements:
        element = pathElement.split('\'')
        if len(element) == 1:
            result = result + struct.pack(">I", int(element[0]))
        else:
            result = result + struct.pack(">I", 0x80000000 | int(element[0]))
    return result


parser = argparse.ArgumentParser()
parser.add_argument('--nonce', help="Nonce associated to the account", type=int, required=True)
parser.add_argument('--gasprice', help="Network gas price", type=int, required=True)
parser.add_argument('--startgas', help="startgas", default='21000', type=int)
parser.add_argument('--amount', help="Amount to send in ether", required=True)
parser.add_argument('--to', help="Destination address", type=str, required=True)
parser.add_argument('--path', help="BIP 32 path to sign with")
parser.add_argument('--data', help="Data to add, hex encoded")
args = parser.parse_args()

if args.path == None:
    args.path = "44'/60'/0'/0/0"

if args.data == None:
    args.data = b""
else:
    args.data = decode_hex(args.data[2:])

amount = Decimal(args.amount) * 10**18

tx = Transaction(
    nonce=int(args.nonce),
    gasprice=int(args.gasprice),
    startgas=int(args.startgas),
    to=decode_hex(args.to[2:]),
    value=int(amount),
    data=args.data,
    v=CHAIN_ID,
    r=0,
    s=0
)

encodedTx = encode(tx, Transaction)

donglePath = parse_bip32_path(args.path)
apdu = bytearray.fromhex("e0040000")
apdu.append(len(donglePath) + 1 + len(encodedTx))
apdu.append(len(donglePath) // 4)
apdu += donglePath + encodedTx

dongle = getDongle(True)
result = dongle.exchange(bytes(apdu))

# Needs to recover (main.c:1121)
if (CHAIN_ID*2 + 35) + 1 > 255:
	ecc_parity = result[0] - ((CHAIN_ID*2 + 35) % 256)
	v = (CHAIN_ID*2 + 35) + ecc_parity
else:
	v = result[0]

r = int(binascii.hexlify(result[1:1 + 32]), 16)
s = int(binascii.hexlify(result[1 + 32: 1 + 32 + 32]), 16)

tx = Transaction(tx.nonce, tx.gasprice, tx.startgas,
                 tx.to, tx.value, tx.data, v, r, s)

print("Signed transaction", encode_hex(encode(tx)))
