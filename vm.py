
# vm.py

from instructions import decode


class TextOSVM:
    def __init__(self):
        self.stack = []
        self.program = []
        self.ip = 0
        self.running = False
        self.memory = [{}]
        self.call_stack = []
        self.max_call_depth = 1000



    def load(self, binary):
        binary = "".join(binary.split())

        if len(binary) % 32 != 0:
            raise ValueError(f"Invalid: {len(binary)} Bits")

        if any(c not in "01" for c in binary):
            raise ValueError("Program must contain only 0s and 1s")

        self.program = [
            binary[i:i+32]
            for i in range(0, len(binary), 32)
        ]

        self.ip = 0
        self.stack = []
        self.globals = {}
        self.memory = [{}]
        self.call_stack = []


    def run(self):
        self.running = True
        self.output = print
        while self.running:
            if self.ip >= len(self.program):
                break

            opcode, operand = decode(self.program[self.ip])
            self.ip += 1

            if opcode == "PUSH":
                self.stack.append(operand)

            elif opcode == "ADD":
                try:
                    b = self.stack.pop()
                    a = self.stack.pop()
                    self.stack.append(a + b)
                except TypeError:
                    self.output("Error: Incompatible types! You can't add a string and an int!")

            elif opcode == "SUB":
                try:
                    b = self.stack.pop()
                    a = self.stack.pop()
                    self.stack.append(a - b)
                except TypeError:
                    self.output("Error: Incompatible types! You can't subtract a string from an int!")

            elif opcode == "MUL":
                try:
                    b = self.stack.pop()
                    a = self.stack.pop()
                    self.stack.append(a * b)
                except TypeError:
                    self.output("Error: Incompatible types! You can't multiply a string and an int!")

            elif opcode == "DIV":
                try:
                    b = self.stack.pop()
                    a = self.stack.pop()

                    if b == 0:
                        raise ZeroDivisionError("Division by zero isn't allowed!")

                    self.stack.append(a // b)
                except TypeError:
                    self.output("Error: Incompatible types! You can't divide a string and an int!")


            elif opcode == "PRINT":
                self.output(str(self.stack.pop()))

            elif opcode == "HALT":
                self.running = False
            

            elif opcode == "LOAD":
                if operand not in self.memory[-1]:
                    raise RuntimeError(
                        f"Undefined variable: {operand}"
                    )

                self.stack.append(self.memory[-1][operand])

            elif opcode == "STORE":
                if not self.stack:
                    raise RuntimeError("Stack is empty")

                self.memory[-1][operand] = self.stack.pop()


            
            elif opcode == "JUMP":
                if operand > len(self.program):
                    raise RuntimeError("Invalid jump address")

                self.ip = operand

            elif opcode == "JUMP_IF":
                condition = self.stack.pop()

                if condition != 0:
                    if operand > len(self.program):
                        raise RuntimeError("Invalid jump address")

                    self.ip = operand

            elif opcode.startswith("CMP_"):
                b = self.stack.pop()
                a = self.stack.pop()

                if opcode == "CMP_EQ":
                    result = a == b
                elif opcode == "CMP_NE":
                    result = a != b
                elif opcode == "CMP_GT":
                    result = a > b
                elif opcode == "CMP_LT":
                    result = a < b
                elif opcode == "CMP_GE":
                    result = a >= b
                elif opcode == "CMP_LE":
                    result = a <= b

                self.stack.append(int(result))



            elif opcode == "CALL":
                if operand >= len(self.program):
                    raise RuntimeError("Invalid function address")

                if len(self.call_stack) >= self.max_call_depth:
                    raise RuntimeError("Maximum recursion depth exceeded")

                self.call_stack.append(self.ip)
                self.memory.append({})
                self.ip = operand


            elif opcode == "RETURN":
                if not self.call_stack:
                    raise RuntimeError("RETURN without CALL")

                # Remove current function scope
                self.memory.pop()

                # Restore execution position
                self.ip = self.call_stack.pop()


            
            elif opcode == "LOAD_GLOBAL":
                if operand not in self.globals:
                    raise RuntimeError(
                        f"Undefined global variable: {operand}"
                    )

                self.stack.append(self.globals[operand])

            elif opcode == "STORE_GLOBAL":
                if not self.stack:
                    raise RuntimeError("Stack is empty")

                self.globals[operand] = self.stack.pop()

            elif opcode == "INPUT":
                inp = input()
                self.stack.append(inp)

            elif opcode == "F_WRITE":
                if len(self.stack) < 2:
                    raise RuntimeError("Not enough stack values")

                path = self.stack.pop()
                contents = self.stack.pop()

                with open(path, "w", encoding="utf-8") as f:
                    f.write(str(contents))


            elif opcode == "F_READ":
                if not self.stack:
                    raise RuntimeError("Stack is empty")

                path = self.stack.pop()

                with open(path, "r", encoding="utf-8") as f:
                    self.stack.append(f.read())

            elif opcode == "F_EXISTS":
                import os

                if not self.stack:
                    raise RuntimeError("Stack is empty")

                path = self.stack.pop()
                self.stack.append(int(os.path.exists(path)))

            elif opcode == "STRING":
                length = operand

                chars = []

                for _ in range(length):
                    if self.ip >= len(self.program):
                        raise RuntimeError("Unexpected end of string")

                    value = int(self.program[self.ip], 2)
                    chars.append(chr(value))
                    self.ip += 1

                self.stack.append("".join(chars))

            elif opcode == "F_DEL":
                import os
                if len(self.stack) < 1:
                    raise RuntimeError("Not enough stack values")

                path = self.stack.pop()

                os.remove(path)

            elif opcode == "F_SIZE":
                import os
                if len(self.stack) < 1:
                    raise RuntimeError("Not enough stack values")
                path = self.stack.pop()
                size = os.stat(path).st_size
                self.stack.append(size)



