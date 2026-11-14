
from vm import TextOSVM

with open(input("Binary file: "), "r") as file:
    binary = file.read()

vm = TextOSVM()
vm.load(binary)
vm.run()
