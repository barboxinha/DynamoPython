"""
Using Regular Expressions
-------------------------
Go to www.regexr.com to test your reg expressions
"""


import re

# (A\d).* will search for -> Letter\digit.everything
regex_str = IN[0]
sheet_names = IN[1] if isinstance(IN[1], list) else [IN[1]]

element_lst = []

for name in sheet_names:
    searchObj = re.search(regex_str, name)
    element_lst.append(searchObj.group())

OUT = element_lst
