"""
Utility functions for the Book-Alchemy application.
"""
from datetime import datetime

def parse_date(date_string):
    """
    Parse a date string in YYYY-MM-DD format into a date object.
    Returns None if the string is empty or None.
    """
    return datetime.strptime(date_string, '%Y-%m-%d').date() if date_string else None