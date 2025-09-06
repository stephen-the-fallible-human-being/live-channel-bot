"""
Staff Management Package
Handles all staff-related functionality
"""

from .core import StaffManagement
from .autocomplete import *

def setup(bot):
    bot.add_cog(StaffManagement(bot))
