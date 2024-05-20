def input_validation(some_input, valid_selections):
    valid_selections_set = set(valid_selections)
    some_input = some_input.lower() 
    while some_input not in valid_selections_set:
        some_input = input("Invalid selection. Please try again:").lower()
    return some_input