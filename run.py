import sys
from vm import TextOSVM

if len(sys.argv) != 2:
    print("Usage: runb <path to .tbin file>")
else:
    with open(sys.argv[1]) as f:
        binary = f.read()

vm = TextOSVM()
vm.load(binary)
vm.run()
