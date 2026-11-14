
INSTRUCTIONS = {
    "PUSH":         0b00000001,
    "POP":          0b00000010,
    "ADD":          0b00000011,
    "SUB":          0b00000100,
    "MUL":          0b00000101,
    "DIV":          0b00000110,
    "PRINT":        0b00000111,
    "HALT":         0b00001000,
    "LOAD":         0b00001001,
    "STORE":        0b00001010,
    "JUMP":         0b00001011,
    "JUMP_IF":      0b00001100,
    "CMP_EQ":       0b00001101,
    "CMP_NE":       0b00001110,
    "CMP_GT":       0b00001111,
    "CMP_LT":       0b00010000,
    "CMP_GE":       0b00010001,
    "CMP_LE":       0b00010010,
    "CALL":         0b00010011,
    "RETURN":       0b00010100,
    "LOAD_GLOBAL":  0b00010101,
    "STORE_GLOBAL": 0b00010110,
    "INPUT":        0b00010111,

    "F_WRITE":      0b00011110,
    "F_DEL":        0b00011111,
    "F_READ":       0b00100000,
    "F_EXISTS":     0b00100001,
    "STRING":       0b00100011,
    "F_SIZE":       0b00100010
}

OPCODES = {
    value: name
    for name, value in INSTRUCTIONS.items()
}


def encode(opcode, operand=0):
    if opcode not in INSTRUCTIONS:
        raise ValueError(f"Unknown instruction: {opcode}")

    if not isinstance(operand, int):
        raise TypeError("Operand must be an integer")

    if not 0 <= operand <= 0xFFFFFF:
        raise ValueError("Operand must fit in 24 bits")

    return f"{INSTRUCTIONS[opcode]:08b}{operand:024b}"


def decode(binary):
    if len(binary) != 32 or any(c not in "01" for c in binary):
        raise ValueError("Invalid instruction")

    opcode = int(binary[:8], 2)
    operand = int(binary[8:], 2)

    if opcode not in OPCODES:
        raise ValueError(f"Unknown opcode: {opcode}")

    return OPCODES[opcode], operand
