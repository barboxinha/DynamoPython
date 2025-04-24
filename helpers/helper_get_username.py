"""
System.Username
---------------
Retrieves the current user's username from the operating system.
"""

# NOTE: Choose one method. Comment out the other.

# .NET lib method #1
from System import Environment

# Python lib method #2
import getpass

username = Environment.UserName
username2 = getpass.getuser()

OUT = username