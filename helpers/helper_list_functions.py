"""
Helper List functions
------------------------
This module contains helper functions for list manipulation, 
including converting objects to lists, equalizing list lengths, checking if all arguments are None, and checking if a list is nested.
It also includes a function to check if a list is a nested list of lists.
"""

def tolist(obj) -> list:
	"""Converts the input into a list if it is not already a list."""
	return obj if isinstance(obj, list) else [obj]


def equalize_list_lengths(*lists):
	"""
	Determines the maximum length of the input lists. Then, iterates through each list and appends the last item of the list until its length matches the maximum length.
	"""
	# Find the maximum length among the lists
	max_length = max(len(lst) for lst in lists)
	
	# Duplicate the last item in each list to match the maximum length
	for lst in lists:
		while len(lst) < max_length:
			if lst:
				lst.append(lst[-1])
			else:
				lst.append(None)
	return lists


def all_none(*args) -> bool:
	"""Returns True if all the input arguments are None."""
	return all(arg is None for arg in args)


def is_nested_list(lst) -> bool:
    """
    Check if the given list is a nested list of lists.

    Parameters:
    lst (list): The list to check.

    Returns:
    bool: True if the list is a nested list of lists, False otherwise.
    """
    if not isinstance(lst, list):
        return False
    return all(isinstance(i, list) for i in lst)

