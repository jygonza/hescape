def input_validation(some_input, valid_selections):
    some_input = some_input.lower() 
    while some_input not in valid_selections:
        print("Invalid selection. Please try again.")
        some_input = input("Enter your selection: ")