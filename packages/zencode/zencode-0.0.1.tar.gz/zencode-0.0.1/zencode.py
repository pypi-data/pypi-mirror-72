#!/usr/bin/env python3
#
# Naive implementation of an encoder for restricted character sets.
# Currently encodes the input into valid ASCII (0x00 - 0x7f); it doesn't
# do full alphanumeric encoding (yet).

import argparse
import os
import struct
import sys

from binascii import hexlify, unhexlify
from math import remainder
from z3 import *

__version__ = '0.0.1'
__author__ = 'Jasper Lievisse Adriaanse <r+pypi@jasper.la>'
__license__ = 'ISC'
__url__ = 'https://github.com/jasperla/zencode'

class Encoder():
    def __init__(self, badbytes, shellcode, register):
        self.badbytes = badbytes
        self.shellcode = shellcode
        self.register = register
        self.prologue = (
            f'and {self.register}, 0x42424242\n'
            f'and {self.register}, 0x3d3d3d3d'
        )
        self.epilogue = f'push {self.register}'

    def split_block(self, block):
        """
        Split a block into individual bytes.
        """
        # Get the individual blocks. The input is a decimal number.
        # So we convert it to a hex string, take the individual nibbles,
        # convert those back into decimal.
        block_1 = int(hex(block)[2:4], 16)
        block_2 = int(hex(block)[4:6], 16)
        block_3 = int(hex(block)[6:8], 16)
        block_4 = int(hex(block)[8:10], 16)
        return [block_1, block_2, block_3, block_4]

    def push_block(self, block):
        """
        If the block contains not bad bytes we can simply push it in one go.
        """
        for b in self.split_block(block):
            if b in self.badbytes:
                return None

        print(self.prologue)
        print(f'add {self.register}, {block:#010x}')
        print(self.epilogue)
        return True

    def divide(self, block, n_parts = 2):
        """
        Attempt to divide the given block in N equal parts.
        """

        if remainder(block, n_parts):
            return None
        else:
            parts = int(block / n_parts)

            # Validate the parts to check for any badbytes.
            for b in unhexlify(hex(parts)[2:]):
                if b in self.badbytes:
                    #print(f'[-] Bad byte {b:#02x} found in {parts:#02x}')
                    return None

            print(self.prologue)
            for i in range(0, n_parts):
                print(f'add {self.register}, {parts:#010x}')
            print(self.epilogue)
            return True

    def call_model(self, byte, nparts = None):
        """
        Returned values:
        [nparts, *parts]
        """
        try:
            if nparts == 2:
                [*vars] = self.z3_model_2(byte)
            elif nparts == 3:
                [*vars] = self.z3_model_3(byte)
            else:
                [*vars] = self.z3_model_2(byte) or self.z3_model_3(byte)

            return len(vars), vars
        except Exception:
            return None, []

    def divide_bytes(self, block):
        """
        Divide the indiviual bytes of this block.
        """
        block_1, block_2, block_3, block_4 = self.split_block(block)

        results = [[], []]

        max_nparts = 2
        force_three_parts = False
        for byte in [block_1, block_2, block_3, block_4]:
            # Start by attempting to split the bytes into two parts, however if one requires
            # three parts we must start over and force using three parts on all of them.
            nparts, *vars = self.call_model(byte)
            if nparts:
                if nparts == 3:
                    # Found a solution with 3 parts. Start over and force the 3 parameter
                    # model this time.
                    force_three_parts = True
                    break
                else:
                    results[0].append(vars[0][0])
                    results[1].append(vars[0][1])
            else:
                print('Not solved in two or three parts?')
                sys.exit(1)

        # If the model was not solved it either meant we need to use three parts or there really
        # is no solution. Either way, try harder.
        if force_three_parts:
            results = [[], [], []]
            for byte in [block_1, block_2, block_3, block_4]:
                nparts, *vars = self.call_model(byte, 3)
                if nparts:
                    results[0].append(vars[0][0])
                    results[1].append(vars[0][1])
                    results[2].append(vars[0][2])

            # Go through the resulting integers from each list, convert them to hex
            # and take care to add a leading zero if needed.
            first, second, third = '0x', '0x', '0x'
            for i in range(0, 4):
                first += hex(results[0][i])[2:].zfill(2)
                second += hex(results[1][i])[2:].zfill(2)
                third += hex(results[2][i])[2:].zfill(2)
        else:
            first, second, third = '0x', '0x', None
            for i in range(0, 4):
                first += hex(results[0][i])[2:].zfill(2)
                second += hex(results[1][i])[2:].zfill(2)


        print('; (z3 solved)')
        print(self.prologue)
        print(f'add {self.register}, {first}')
        print(f'add {self.register}, {second}')
        if third:
            print(f'add {self.register}, {third}')
        print(self.epilogue)

        return True

    def z3_add_constraints(self, solver, *vars):
        for v in vars:
            # Ensure the parameters are within ASCII range
            solver.add(v > 0)
            solver.add(v < 0x80)

            # Also weed out any badbytes
            [solver.add(v != b) for b in self.badbytes]

    def z3_model_2(self, byte):
        x, y = Ints('x y')
        s = Solver()
        s.add(x + y == byte)

        m = self.z3_model_solve(s, x, y)
        if m:
            #print(f'{hex(byte)} solved: ', end='')
            return [m[x], m[y]]
        else:
            return None

    def z3_model_3(self, byte):
        x, y, z = Ints('x y z')
        s = Solver()
        s.add(x + y + z == byte)

        m = self.z3_model_solve(s, x, y, z)
        if m:
            #print(f'{hex(byte)} solved: ', end='')
            return [m[x], m[y], m[z]]
        else:
            return None

    def z3_model_solve(self, solver, *vars):
        self.z3_add_constraints(solver, *vars)
        solver.check()

        try:
            model = solver.model()
            results = {}
            for v in vars:
                results[v] = model[v].as_long()
            return results
        except Z3Exception:
            return None


    def encode(self):
        # Now go through the shellcode in blocks of 4 bytes
        for i in range(0, len(self.shellcode), 4):
            # convert the block from bytes into a number we can divide by
            block = int(hexlify(self.shellcode[i:i + 4]), 16)
            block_hex = hex(block)[2:]

            print(f'\n; 0x{block_hex}')
            if not self.push_block(block):
                if not self.divide(block, 2):
                    if not self.divide(block, 3):
                        if not self.divide_bytes(block):
                            print('sorry, you have to encode this block manually')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--badbytes', '-b', type=os.fsencode, default=b'',
                        help='Badbytes to take into account; in \'\\x00\' format.')
    parser.add_argument('--shellcode', '-s', type=os.fsencode, required=True,
                        help='Shellcode to encode; in \'\\xca\\xfe\' format.')
    parser.add_argument('--register', '-r', default='eax',
                        help='Target register; defaults to "eax".')
    args = parser.parse_args()

    # Remove the '\x' that snuck in as part of the raw input,
    # then convert it into a string a re-introduce the '\x' but this
    # time as actual escapes as oposed to merely filler charactesr.
    badbytes = args.badbytes.replace(b'\\x', b'').decode()
    #print(f'badbytes: {badbytes}')
    badbytes = unhexlify(badbytes)
    #print(f'badbytes: {badbytes}')

    # Add all non-ascii characters to the badbytes list
    for x in range(0x80, 0xff + 1):
        badbytes += struct.pack('<B', x)

    # Do the same for the actual payload bytes
    shellcode = unhexlify(args.shellcode.replace(b'\\x', b'').decode())

    # Pad the shellcode to a length which is a multiple of 4.
    if len(shellcode) % 4:
        print(f'[*] Shellcode is {len(shellcode)} long; padding it with ', end='')
        numpad = 4 - (len(shellcode) % 4)
        print(f'{numpad} bytes of 0x90')
        padding = b'\x90' * numpad
        shellcode += padding

    #print('individual bad bytes as hex = ', end='')
    #[print(hex(x), end=' ') for x in badbytes]
    #print()

    print(f'[*] bad bytes: {badbytes}')
    print(f'[*] shellcode: {shellcode}')

    enc = Encoder(badbytes, shellcode, args.register)
    enc.encode()



if __name__ == '__main__':
    main()
