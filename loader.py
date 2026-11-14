
import struct

MAGIC = b"BYN1"
VERSION = 1

def load_tbc(vm, filename):
    with open(filename, "rb") as f:
        data = f.read()

    if len(data) < 9:
        raise ValueError("Invalid Bynary bytecode")

    if data[:4] != MAGIC:
        raise ValueError("Not a Bynary bytecode file")

    if data[4] != VERSION:
        raise ValueError("Unsupported bytecode version")

    count = struct.unpack(">I", data[5:9])[0]
    payload = data[9:]

    if len(payload) != count * 4:
        raise ValueError("Corrupted bytecode")

    # Convert bytes back into 32-bit instructions
    binary = "".join(f"{b:08b}" for b in payload)

    vm.load(binary)
