import os

from vm import TextOSVM


def run_binary(path, output_callback=print):
    vm = TextOSVM()

    # Redirect VM output to TextOS
    vm.output = output_callback

    with open(path, "r") as file:
        binary = file.read()

    vm.load(binary)
    vm.run()
