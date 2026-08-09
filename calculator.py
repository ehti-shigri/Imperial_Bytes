def show_menu():
    print("\n--- DMAS Calculator Menu ---")
    print("1. Division (/)")
    print("2. Multiplication (*)")
    print("3. Addition (+)")
    print("4. Subtraction (-)")
    print("5. Exit")

def dmas_calculator():
    while True:
        show_menu()
        choice = input("Select an operation (1-5): ")

        if choice == '5':
            print("Exiting calculator. Goodbye!")
            break

        if choice in ('1', '2', '3', '4'):
            try:
              
                a = float(input("Enter first number: "))
                b = float(input("Enter second number: "))

                if choice == '1':
                    if b == 0:
                        print("Error: Division by zero is undefined.")
                    else:
                        print(f"Result: {a} / {b} = {a / b}")
                elif choice == '2':
                    print(f"Result: {a} * {b} = {a * b}")
                elif choice == '3':
                    print(f"Result: {a} + {b} = {a + b}")
                elif choice == '4':
                    print(f"Result: {a} - {b} = {a - b}")

            except ValueError:
                print("Invalid input! Please enter valid numeric values.")
        else:
            print("Invalid selection! Please choose a valid option from the menu.")


dmas_calculator();

