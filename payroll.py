import sys
from os import listdir
sys.path.append("./code")

from mastertimesheet import MasterTimesheet

if __name__ == "__main__":
    full_original_timesheet = '20200101-20200912.csv'
    master_timesheet_path = 'timesheet-master.csv'
    new_csv_path = '20200906-20200912.csv'

    master_timesheet = MasterTimesheet(master_timesheet_path)
    timesheets = [f for f in listdir('timesheets')]
    for sheet in timesheets:
        master_timesheet.add_to_master(sheet)
    # master_timesheet.dump_data("Sierra Simmons", "payroll", "2020-09-04")

    text_input = input("Enter Command: ")
    mode, start_date = text_input.split(" ")
    if mode != "ESD" and mode != "payroll":
        raise("Invalid Mode")

    master_timesheet.get_full_hours(mode, start_date) # thru sept 3

