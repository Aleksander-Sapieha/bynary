
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
        self.globals = {}
        self.memory = [{}]
        self.call_stack = []
        self.max_call_depth = 1000



    def load(self, binary):
        # print("RAW INPUT:")
        # print(repr(binary))

        binary = "".join(binary.split())

        # print("CLEAN INPUT:")
        # print(binary)
        # print("TOTAL BITS:", len(binary))
        # print("REMAINDER:", len(binary) % 32)

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

            elif opcode == "POP":
                self.stack.pop()

            elif opcode == "ADD":
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a + b)

            elif opcode == "SUB":
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a - b)

            elif opcode == "MUL":
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a * b)

            elif opcode == "DIV":
                b = self.stack.pop()
                a = self.stack.pop()

                if b == 0:
                    raise ZeroDivisionError("Division by zero")

                self.stack.append(a // b)

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





