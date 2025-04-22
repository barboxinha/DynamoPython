"""
Helper Lambda Functions
"""

# Helper function in order to map a function to each item in a list
def process_list(_func, _list):
    """
    Applies a function to each item in a list, recursively handling nested lists.
    If the item is a list, it applies the function to each element in that list.
    """
    # Check if the input is a list, if not, apply the function directly
    return map(lambda x: process_list(_func, x) if type(x)==list else _func(x), _list)


# Helper function in order to map a function to each item in a list 
# with the option to pass another argument to the function
def process_list_arg(_func, _list, _arg):
    """
    Applies a function to each item in a list, recursively handling nested lists.
    If the item is a list, it applies the function to each element in that list.
    The function can also take an additional argument.
    """
    # Check if the input is a list, if not, apply the function directly
    return map(lambda x: process_list_arg(_func, x, _arg) if type(x)==list else _func(x, _arg), _list)