class Register:
    def __init__(self, operation, operand):
        self.value: int = 0
        self.expression: list[list[str, str]] = [[operation, operand]]
        self.is_evaluated = False

    def reset_register(self):
        self.value = 0
        self.is_evaluated = False


class Calculator:
    def __init__(self):
        self.registers: dict[str, Register] = {}

    def add(self, register, operand):
        if register in self.registers:
            self.registers[register].expression.append(["add", operand])
            self.registers[register].reset_register()
        else:
            self.registers[register] = Register("add", operand)

    def subtract(self, register: str, operand):
        if register in self.registers:
            self.registers[register].expression.append(["subtract", operand])
            self.registers[register].reset_register()
        else:
            self.registers[register] = Register("subtract", operand)

    def multiply(self, register: str, operand):
        if register in self.registers:
            self.registers[register].expression.append(["multiply", operand])
            self.registers[register].reset_register()
        else:
            self.registers[register] = Register("multiply", operand)

    # TODO: Argumetn should be string
    def evaluate_register(self, register: Register):
        if register.is_evaluated:
            return register.value

        for operation, operand in register.expression:
            if operation == "add":
                if operand.isnumeric():
                    register.value += int(operand)

                else:
                    register.value += self.evaluate_register(
                        self.registers[operand])

            elif operation == "subtract":
                if operand.isnumeric():
                    register.value -= int(operand)

                else:
                    register.value -= self.evaluate_register(
                        self.registers[operand])

            elif operation == "multiply":
                if operand.isnumeric():
                    register.value *= int(operand)

                else:
                    register.value *= self.evaluate_register(
                        self.registers[operand])

        register.is_evaluated = True
        return register.value


class CalculatorInterface:
    VALID_OPERATIONS = ["add", "subtract", "multiply"]

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
                    self.calculator.registers[register].reset_register()
                    print(self.calculator.evaluate_register(
                        self.calculator.registers[register]))

            case[register, operation, value]:
                if not self.is_valid_register(register) or not self.is_valid_value(value):
                    return

                if operation not in self.VALID_OPERATIONS:
                    print("Invalid operation")
                    return

                elif operation == "add":
                    self.calculator.add(register, value)

                elif operation == "subtract":
                    self.calculator.subtract(register, value)

                elif operation == "multiply":
                    self.calculator.multiply(register, value)

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
