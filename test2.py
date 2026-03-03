class Calculator:
    """A simple calculator class with basic arithmetic operations."""
    
    def add(self, a, b):
        """Add two numbers."""
        return a + b

    def subtract(self, a, b):
        """Subtract two numbers."""
        return a - b

    def multiply(self, a, b):
        """Multiply two numbers."""
        return a * b

    def divide(self, a, b):
        """Divide two numbers with error handling for zero division."""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    
    def power(self, a, b):
        """Raise a number to a power."""
        return a ** b


def get_user_input():
    """Get operation and numbers from user with error handling."""
    try:
        print("\n=== Simple Calculator ===")
        print("Available operations: +, -, *, /, **")
        
        operation = input("Enter operation (+, -, *, /, **): ").strip()
        
        if operation not in ['+', '-', '*', '/', '**']:
            print("Error: Invalid operation. Please use +, -, *, /, or **")
            return None
        
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        
        return operation, num1, num2
    
    except ValueError as e:
        print(f"Error: Invalid input. Please enter valid numbers. Details: {e}")
        return None
    except KeyboardInterrupt:
        print("\nCalculation cancelled.")
        return None


def perform_calculation(calc, operation, num1, num2):
    """Perform the calculation based on the operation."""
    try:
        if operation == '+':
            result = calc.add(num1, num2)
        elif operation == '-':
            result = calc.subtract(num1, num2)
        elif operation == '*':
            result = calc.multiply(num1, num2)
        elif operation == '/':
            result = calc.divide(num1, num2)
        elif operation == '**':
            result = calc.power(num1, num2)
        
        print(f"\nResult: {num1} {operation} {num2} = {result}")
        return result
    
    except ValueError as e:
        print(f"Error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        return None


if __name__ == "__main__":
    calc = Calculator()
    
    while True:
        user_input = get_user_input()
        
        if user_input is None:
            print("Would you like to try again? (yes/no): ", end="")
            try:
                response = input().strip().lower()
                if response not in ['yes', 'y']:
                    print("Thank you for using the calculator!")
                    break
            except KeyboardInterrupt:
                print("\nThank you for using the calculator!")
                break
        else:
            operation, num1, num2 = user_input
            perform_calculation(calc, operation, num1, num2)
            
            print("Would you like to perform another calculation? (yes/no): ", end="")
            try:
                response = input().strip().lower()
                if response not in ['yes', 'y']:
                    print("Thank you for using the calculator!")
                    break
            except KeyboardInterrupt:
                print("\nThank you for using the calculator!")
                break

