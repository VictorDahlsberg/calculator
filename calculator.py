import sys
import io


def is_float(value: any) -> bool:
    """Checks if value is float"""
    try:
        float(value)
        return True

    except ValueError:
        return False


class Register:
    """
    A register which has a value and list of operations
    which are to be executed on the register
    """

    def __init__(self, operation: str, operand: str) -> None:
        """Inits Register with value 0 and adds
        operation and operand to expression list"""
        self.value: int = 0
        self.expression: list[list[str, str]] = [[operation, operand]]
        self.is_evaluated: bool = False

    def reset_register(self) -> None:
        """Resets register value and marks it as not evaluated"""
        self.value: float = 0
        self.is_evaluated: bool = False

    def add_operation(self, operation: str, operand: str):
        """Adds a new operation to the register"""
        self.expression.append([operation, operand])


class Calculator:
    """
    A lazily evaluated calculator that can add, subract and multiply
    values in a set of registers. Registers that don't explicitly get
    assigned a value will be assumed to have the value 0.
    """

    VALID_OPERATIONS = ["add", "subtract", "multiply"]

    def __init__(self) -> None:
        """Inits Calculator with no registers"""
        self.registers: dict[str, Register] = {}
        self.register_visitation_map: dict[str, list[str]] = {}

    def new_operation(
            self, register: str, operation: str, operand: str) -> None:
        """Adds new operation to be evaluated to register"""
        if register in self.registers:
            self.registers[register].add_operation(operation, operand)
            self.registers[register].reset_register()
        else:
            self.registers[register] = Register(operation, operand)
            self.register_visitation_map[register] = []

    def evaluate_register(
            self, register: str, visited_registers: list[str] = []) -> float:
        """Returns the value of the register if possible"""

        # Avoids RecursionError by checking for loops in visited_registers
        if register in visited_registers[0:-1]:
            print("Cirlcular logic detected, aborting...")
            quit()

        # Register value is assumed to be 0 if not given a value
        if register not in self.registers:
            return 0

        reg: Register = self.registers[register]

        if reg.is_evaluated:
            return reg.value

        for operation, operand in reg.expression:
            if operation == "add":
                if is_float(operand):
                    reg.value += float(operand)

                else:
                    reg.value += self.evaluate_register(
                        operand, visited_registers + [operand])

            elif operation == "subtract":
                if is_float(operand):
                    reg.value -= float(operand)

                else:
                    reg.value -= self.evaluate_register(
                        operand, visited_registers + [operand])

            elif operation == "multiply":
                if is_float(operand):
                    reg.value *= float(operand)

                else:
                    reg.value *= self.evaluate_register(
                        operand, visited_registers + [operand])

        reg.is_evaluated = True
        return reg.value


class CalculatorInterface:
    """
    A termminal user interface for Calculator used for reading commands from
    standard input or from file. Also notifies user of potential invalid inputs
    """

    def __init__(self) -> None:
        """Inits CalculatorInterface and creates new Calculator"""
        self.calculator: Calculator = Calculator()
        self.file_line_number: int = None

    def parse_input(self, command: str, line_number: int = None) -> None:
        """Interprets command and notifies user of potential invalid input"""
        words: list[str] = command.lower().split()
        match words:
            case["quit"]:
                quit()

            case["print", register]:
                self.print_register(register)

            case[register, operation, operand]:
                if (not self.is_valid_register(register, line_number) or
                        not self.is_valid_operand(operand, line_number)):
                    return

                if operation not in self.calculator.VALID_OPERATIONS:
                    self.notify_input_error("Invalid operation")
                    return

                else:
                    self.calculator.new_operation(register, operation, operand)

            case _:
                self.notify_input_error("Invalid command structure")

    def parse_file(self, file_path: str) -> None:
        """Reads lines from file and interprets each line as a command"""
        try:
            file_object: io.TextIOWrapper = open(file_path, "r")

        except FileNotFoundError:
            print("File \"{}\" could not found".format(file_path))
            return

        self.is_file_mode = True
        lines: list[str] = file_object.readlines()
        for line_number, line in enumerate(lines):
            self.file_line_number = line_number
            self.parse_input(line)
        quit()

    def print_register(self, register: str) -> None:
        """Prints register value to standard output with 1 decimal place"""

        if not self.is_valid_register(register):
            return

        print(round(self.calculator.evaluate_register(register), 1))

    def is_valid_register(
            self, register: str, line_number: int = None) -> bool:
        """Checks if the specified register has a valid name"""

        if not register:
            self.notify_input_error("Register name cannot be empty")
            return False

        elif register.isnumeric():
            self.notify_input_error(
                "Register name must contain atleast one letter")
            return False

        elif not register.isalnum():
            self.notify_input_error(
                "Register name can only contain alphanumerical characters")
            return False

        return True

    def is_valid_operand(self, operand: str, line_number: int = None) -> bool:
        """Checks if the specified operand is valid"""

        if not operand:
            self.notify_input_error("Value can't be empty")
            return False

        elif not is_float(operand):
            return self.is_valid_register(operand, line_number)

        return True

    def notify_input_error(self, error_message: str) -> None:
        """
        Notifies user of potential invalid inputs by
        printing error_message to standard output
        """
        message: str = ""
        if self.file_line_number is not None:
            message += "Error in line {}, ".format(self.file_line_number)

        message += error_message
        print(message)


if __name__ == "__main__":
    calc_interface: CalculatorInterface = CalculatorInterface()
    num_args: int = len(sys.argv)

    if num_args > 2:
        print("Expected 0 or 1 argument, but {} were given"
              .format(num_args - 1))

    elif num_args == 2:
        calc_interface.parse_file(sys.argv[1])

    else:
        print("Enter commands on the form <register> <operation> <value>")
        while True:
            command: str = input("Please enter command:\n")
            calc_interface.parse_input(command)
