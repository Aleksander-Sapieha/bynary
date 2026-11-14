import sys
from vm import TextOSVM

if len(sys.argv) != 1:
    print("Usage: runb <path to .tbin file>")
else:
    binary = sys.argv[1]

vm = TextOSVM()
vm.load(binary)
vm.run()
