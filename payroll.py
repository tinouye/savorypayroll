import sys
from os import listdir
import datetime as dt
sys.path.append("./code")

import deputyapi
import timesheets

from mastertimesheet import MasterTimesheet

if __name__ == "__main__":
    end_date = None
    debug_mode = True

    # Bypass user input
    if debug_mode:
        end_date = dt.date.fromisoformat("2020-09-18")
    
    else:
        # Loop continues while end_date has no value
        while not end_date:
            text_input = input("Enter payroll end date: ")
            try:
                end_date = dt.date.fromisoformat(text_input)
                # Loop y/n question while answer isn't y nor n
                while True:
                    print(end_date.strftime("Processing payroll period ending on %A %B %d, %Y"))
                    if end_date.weekday() != 3:
                        print(end_date.strftime("WARNING: %A is not a valid end date for a payroll period!"))
                    proceed = input("Proceed? (y/n): ")
                    if proceed == "y":
                        break
                    elif proceed == "n":
                        # Wipe end date and start loop from top
                        end_date = None
                        break
                    else:
                        continue

            except ValueError:
                print("Date must be in format 'YYYY-MM-DD' (eg 2020-01-03)")
    
    start_date = end_date - dt.timedelta(days=13)

    timesheet_json = deputyapi.get_raw_data(start_date, end_date)
    
    timesheets.format_output(end_date, timesheet_json)

    input("Press any key to exit: ")