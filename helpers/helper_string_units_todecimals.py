"""
String.UnitsToDecimals
----------------------
Converts a list of strings with feet and inches to decimal numbers.
"""
__author__ = "Marco Barboza"


def to_list(x):
    if isinstance(x, list): return x
    else: return [x]


def process_list(_func, _list):
    return map(lambda x: process_list(_func, x) if type(x) == list else _func(x), _list)


# String formatting functions
def remove_unit_chars(unit_str):
    """
    Removes unit characters from a string.
    """
    if unit_str.count("\'") > 0 or unit_str.count("\"") > 0:
        new_str = unit_str.replace("\'", "")
        new_str = new_str.replace("\"", "")
        return new_str   
    return unit_str


def convert_to_float(frac_str):
    """
    Converts a string to a float. If the string is a fraction, it converts it to a float.
    """
    try:
        return float(frac_str)
    except ValueError:
        num, denom = frac_str.split("/")
        try:
            leading, num = num.split(" ")
            whole = float(leading)
        except ValueError:
            whole = 0
        frac = float(num) / float(denom)
        return whole - frac if whole < 0 else whole + frac


def convert_feet(lst_vals):
    """
    Converts a list of strings with feet and inches to decimal numbers.
    """
    total = []
    for i in lst_vals:
        if(set("-").intersection(i)):
            first = i.split("-")[0]
            second = i.split("-")[1]
            ft = convert_to_float(first)
            inch = convert_to_float(second.split()[0])
            try:
                fraction = convert_to_float(second.split()[1])
            except IndexError:
                fraction = 0.0
        else:
            term = i.split()
            ft = convert_to_float(term[0])
            inch = convert_to_float(term[1])
            try:
                fraction = convert_to_float(term[2])
            except IndexError:
                fraction = 0.0
        total.append(ft + ((inch +fraction)/12))       
    return total


# Main
error_report = None
unit_strings = to_list(IN[0])

try:
    frac_strings = process_list(remove_unit_chars, unit_strings)
    if isinstance(unit_strings[0], list):
        decimal_numbers = process_list(convert_feet, frac_strings)
    else:
        decimal_numbers = convert_feet(frac_strings)
except:
    import traceback
    error_report = traceback.format_exc()


if error_report == None:
    OUT = decimal_numbers
else:
    OUT = error_report