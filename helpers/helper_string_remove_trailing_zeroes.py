"""
String.RemoveTrailingZeroes
---------------------------
Removes trailing zeroes from the given string.
"""

import sys
import clr


num_str = IN[0]

if num_str.Contains('.'):
	if num_str[0] == '0':
		i = num_str.Split('.')
		new_num_str = i[0] + '.' + i[1].strip('0')
	else:
		new_num_str = num_str.strip('0')
else:
	new_num_str = num_str
	
OUT = new_num_str