class Register:
    def __init__(self, operation, value):
        self.value = 0
        self.expression = []


class Calculator:
    def __init__(self):
        self.registers: dict[Register] = {}

    def add(self, register, value):
        if not self.registers[register]:
            self.registers[register] = Register("add", value)
        else:
            self.registers[register].expression.append("add", value)

    def subtract(self, register: str, value):
        pass

    def multiply(self, register: str, value):
        pass

    def evaluate_register(self, register):
        pass


class CalculatorInterface:
    VALID_OPERATIONS = ["add", "subtract", "multiply"]
    self.registers: dict[binaryOperation]

    def __init__(self) -> None:
        self.calculator: Calculator = Calculator()

    def parse_input(self) -> None:
        command: str = input("Please enter command:\n")
        words: list[str] = command.lower().split()

        match words:
            case["quit"]:
                quit()

            case["print", register]:
                # TODO: check if register exists
                if self.is_valid_register(register):
                    print(self.calculator.evaluate_register(register))

            case[register, operation, value]:
                if not self.is_valid_register(register) or not self.is_valid_value(value):
                    return

                if operation not in self.VALID_OPERATIONS:
                    print("Invalid operation")
                    return

                elif operation == "add":
                    self.calculator.add(register, value)

                elif operation == "subtract":
                    self.calculator.add(register, value)

                elif operation == "multiply":
                    self.calculator.add(register, value)

            case _:
                print("Invalid command")

    def is_valid_register(self, register: str) -> bool:
        if not register:
            print("Register can't be empty")
            return False

        elif register.isnumeric():
            print("Registers must contain atleast one letter")
            return False

        elif not register.isalnum():
            print("Registers can only contaion alphanumerical characters")
            return False
        return True

    def is_valid_value(self, value: str) -> bool:
        if not value:
            print("Value can't be empty")
            return False

        elif not value.isnumeric():
            return self.is_valid_register(value)
        return True


if __name__ == "__main__":
    calc_interface = CalculatorInterface()
    while True:
        calc_interface.parse_input()
