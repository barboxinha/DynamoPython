"""
String.RemoveSpecialChars
-------------------------
Removes forbidden ASCII characters from the given string.
"""

import re


strings = IN[0] if isinstance(IN[0],list) else [IN[0]]
clean_strings = []

for char in strings:
	#remove spaces
	clean_strings.append("".join(re.findall(r"[a-zA-Z0-9 _éè-]+", char) ))
	
OUT = clean_strings if isinstance(IN[0], list) else clean_strings[0]