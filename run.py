
import sys
import os

from vm import TextOSVM
from loader import load_tbc
from compile import compile_tlib

if len(sys.argv) < 2:
    print("Usage:")
    print("  runb <file.tbin or file.tbinc>")
    print("  runb compile <file.tbin>")
    sys.exit(1)

command = sys.argv[1]

if command == "compile":
    if len(sys.argv) != 3:
        print("Usage: runb compile <path to .tbin>")
        sys.exit(1)

    source = sys.argv[2]

    if not source.endswith(".tbin"):
        print("Error: Source file must be .tbin")
        sys.exit(1)

    output = os.path.splitext(source)[0] + ".tbinc"

    compile_tlib(source, output)

elif command == "run":
    if len(sys.argv) != 3:
        print("Usage: runb run <file.tbin or file.tbinc>")
        sys.exit(1)

    filename = sys.argv[2]
    extension = os.path.splitext(filename)[1]

    vm = TextOSVM()

    if extension == ".tbin":
        with open(filename) as f:
            binary = f.read()

        vm.load(binary)

    elif extension == ".tbinc":
        load_tbc(vm, filename)

    else:
        print("Unsupported file extension:", extension)
        sys.exit(1)

    vm.run()

else:
    print("Unknown command:", command)
