"""
String.ExtractNumbers
---------------------
Extracts all the numbers from the given string. 
This is useful when you have a string with numbers and you want to extract them as a list of numbers.
"""

import re


def get_numbers(str): 
    array = re.findall(r'[-+]\d*\.\d+|\d+', str)
    double = [float(x) for x in array]
    return double


strings = IN[0] if isinstance(IN[0],list) else [IN[0]]
array = [get_numbers(x) for x in strings]

OUT = array if isinstance(IN[0], list) else array[0]