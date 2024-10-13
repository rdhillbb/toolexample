from datetime import datetime, timedelta
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

timeframedescription = """
The `gettimeframe` function calculates dates based on user input, always returning `mm/dd/yyyy` format.
Valid inputs include "current/today" (today's date), "last year" (date from a year ago), "N years ago" and "N days ago"
(date N years or days before today), "month" (current month/year), and "this year" (current year). For invalid inputs,
it returns today's date with an error message. Examples: "2 years ago" returns `04/06/2022`, "10 days ago" yields `03/27/2024`.
"""
timeframedescription = """
The gettimeframe function calculates dates based on user input, always returning mm/dd/yyyy format. Valid inputs include "current/today" (today's date), "last year" (date from a year ago), "N years ago" and "N days ago" (date N years or days before today), "N months ago" (date N months before today), "month" (current month/year), and "this year" (current year). For invalid inputs, it returns today's date with an error message. Examples: "2 years ago" returns 04/06/2022, "10 days ago" yields 03/27/2024, and "10 months ago" results in 06/23/2023.
"""

def gettimeframex(timeframe: str) -> str:
    """
    Returns the date based on the given timeframe, with an adjustment for handling invalid inputs
    by returning today's date and an error message.
    
    Args:
    - timeframe (str): The timeframe for the date calculation. Accepted values now also include 'year' and 'this year',
                       with a special handler for invalid inputs.
    
    Returns:
    - str: The date in 'mm/dd/yyyy' or 'mm/yyyy' format, or the year in 'yyyy' format, depending on the request.
           For invalid inputs, returns today's date and an error message.
    """
    now = datetime.now()
    if timeframe.lower() in ['current/today', 'today']:
        return now.strftime('%m/%d/%Y')
    elif timeframe.lower() in ['lastyear', 'last year']:
        last_year_date = now.replace(year=now.year - 1)
        return last_year_date.strftime('%m/%d/%Y')
    elif timeframe.lower().endswith('years ago'):
        try:
            years_ago = int(timeframe.split()[0])
            years_ago_date = now.replace(year=now.year - years_ago)
            return years_ago_date.strftime('%m/%d/%Y')
        except ValueError:
            return f"Invalid input. Returning today's date of {now.strftime('%m/%d/%Y')}"
    elif timeframe.lower().endswith('days ago'):
        try:
            days_ago = int(timeframe.split()[0])
            days_ago_date = now - timedelta(days=days_ago)
            return days_ago_date.strftime('%m/%d/%Y')
        except ValueError:
            return f"Invalid input. Returning today's date of {now.strftime('%m/%d/%Y')}"
    elif timeframe.lower() == 'month':
        return now.strftime('%m/%Y')
    elif timeframe.lower() in ['year', 'this year']:
        return now.strftime('%Y')
    else:
        return f"Invalid input. Returning today's date of {now.strftime('%m/%d/%Y')}."

class GetGTimeFrameInput(BaseModel):
     timeframe: str = Field(..., description="user input, always returning date format mm/dd/yyyy")


class TimeFrameTool(BaseTool):
    name = "gettimeframe"
    description: str  = timeframedescription 
    def _run(self, timeframe: str):
        resp = gettimeframe(timeframe)

        return resp

    def _arun(self, info: str):
        raise
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta  # This module helps with month arithmetic

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def gettimeframe(timeframe: str) -> str:
    """
    Returns the date based on the given timeframe, with an adjustment for handling invalid inputs
    by returning today's date and an error message.
    
    Args:
    - timeframe (str): The timeframe for the date calculation. Accepts phrases like 'X months from now', 'X days ago', etc.
    
    Returns:
    - str: The date in 'mm/dd/yyyy' format or 'mm/yyyy' format, or the year in 'yyyy' format, depending on the request.
           For invalid inputs, returns today's date and an error message.
    """
    now = datetime.now()
    timeframe = timeframe.lower().strip()

    try:
        if timeframe in ['current/today', 'today']:
            return now.strftime('%m/%d/%Y')
        elif timeframe in ['lastyear', 'last year']:
            return (now.replace(year=now.year - 1)).strftime('%m/%d/%Y')
        elif timeframe.endswith('years ago'):
            years_ago = int(timeframe.split()[0])
            return (now.replace(year=now.year - years_ago)).strftime('%m/%d/%Y')
        elif timeframe.endswith('days ago'):
            days_ago = int(timeframe.split()[0])
            return (now - timedelta(days=days_ago)).strftime('%m/%d/%Y')
        elif timeframe.endswith('months ago'):
            months_ago = int(timeframe.split()[0])
            return (now - relativedelta(months=months_ago)).strftime('%m/%d/%Y')
        elif timeframe.endswith('months from now'):
            months_from_now = int(timeframe.split()[0])
            return (now + relativedelta(months=months_from_now)).strftime('%m/%d/%Y')
        elif timeframe == 'month':
            return now.strftime('%m/%Y')
        elif timeframe in ['year', 'this year']:
            return now.strftime('%Y')
    except (ValueError, IndexError):
        # Handles cases where splitting does not work or conversion fails
        pass

    return f"Invalid input. Returning today's date of {now.strftime('%m/%d/%Y')}."


# Example usage:
"""
print(gettimeframex("3 months from now"))  # Expected output: Date three months in the future in 'mm/dd/yyyy' format

# Test statements, including handling for invalid input
print(gettimeframex("100 months ago"))
print(gettimeframe("year"))            # Expected to return the current year in yyyy format
print(gettimeframe("this month"))      # Invalid input, expected to return today's date and error message
print(gettimeframe("300 days ago"))    # Expected to return the date 300 days ago from today in mm/dd/yyyy format
print(gettimeframe("invalid input"))   # Invalid input, expected to return today's date and error message
print(gettimeframe("current/today"))  # Expected to return the current date in mm/dd/yyyy format
print(gettimeframe("lastyear"))       # Expected to return the date one year ago from today in mm/dd/yyyy format
print(gettimeframe("2 years ago"))    # Expected to return the date two years ago from today in mm/dd/yyyy format
print(gettimeframe("month"))          # Expected to return the current month and year in mm/yyyy format
print(gettimeframe("10 days ago"))    # Expected to return the date 10 days ago from today in mm/dd/yyyy format
print(gettimeframe("100 days ago"))   # Expected to return the date 100 days ago from today in mm/dd/yyyy format
print(gettimeframe("year"))           # Expected to return the current year in yyyy format
print(gettimeframe("this year"))      # Expected to return the current year in yyyy format
print(gettimeframe("invalid input"))  # Expected to return "Invalid input."
"""
