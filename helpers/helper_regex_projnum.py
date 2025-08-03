"""
Regular Expression Search of Project Numbers
---------------------------------------------
This script searches for project numbers in a list of messages using regular expressions.
It uses two methods: `re.findall` to find all occurrences of the pattern in each message,
"""
import sys
import re

# Sample messages
message_lst = ["Hello, I need help with project 12775.000. Thanks!",
                "Hi Helpdesk, could you add me to project 14663.00",
                "@Revit I need to add members to 24813 and 25576 thanks in advance!",
                "Hi, can I also add a consultant to 12775.000 please.",
                "Hi, @IT Support can you help with setting up a Mural? Thank you"]

project_lst = []

grouped_project_lst = []

re_pattern = r"\d{5}\.\d{2,3}|\d{5,8}"

# Use this to FindAll
for message in message_lst:
    project_num = re.findall(re_pattern, message)
    project_lst.append(project_num)

# OR Use this alternative to Search AND Group
for msg in message_lst:
    searchObj = re.search(re_pattern, msg)
    if searchObj is None:
        continue
    grouped_project_lst.append(searchObj.group())


print(project_lst)
print(set(grouped_project_lst))