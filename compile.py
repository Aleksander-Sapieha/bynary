import struct

MAGIC = b"BYN1"
VERSION = 1

def compile_tlib(source, output):
    with open(source, "r") as f:
        binary = "".join(f.read().split())

    if any(c not in "01" for c in binary):
        raise ValueError("Invalid Bynary instructions")

    if len(binary) % 32 != 0:
        raise ValueError("Invalid instruction length")

    instruction_count = len(binary) // 32

    # Convert binary text into actual bytes
    payload = bytes(
        int(binary[i:i+8], 2)
        for i in range(0, len(binary), 8)
    )

    # Header + instruction count + payload
    header = MAGIC + bytes([VERSION])
    header += struct.pack(">I", instruction_count)

    with open(output, "wb") as f:
        f.write(header)
        f.write(payload)

    print(f"Compiled {source} -> {output}")
