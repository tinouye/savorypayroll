import csv
import datetime as dt
import calendar
from hoursholder import HoursHolder

class MasterTimesheet:
    def __init__(self, path):
        self.master_timesheet_path = path

        self.load_master()


    def load_master(self):
        self.master_timesheet_list = []
        self.master_timesheet_dict = []
        path = self.master_timesheet_path

        # Load into memory in list form
        with open(path) as master_csv:
            master_reader = csv.reader(master_csv)

            for row in master_reader:
                self.master_timesheet_list.append(row)

        # Load dictionary form as well (for querying)
        with open(path) as master_csv:
            master_reader = csv.DictReader(master_csv)
            for row in master_reader:
                self.master_timesheet_dict.append(row)


    def add_to_master(self, new_csv_path):
        added_counter = 0
        omitted_counter = 0
        new_csv_path = "timesheets/" + new_csv_path

        with open (new_csv_path) as new_csv:
            master_timesheet_path = self.master_timesheet_path
            master_timesheet_list = self.master_timesheet_list

            # Read incoming csv
            timesheet_reader = csv.reader(new_csv)

            with open (master_timesheet_path, 'a', newline='') as master_csv:
                # Write to master timesheet
                master_csv_writer = csv.writer(master_csv, quoting=csv.QUOTE_ALL)

                # Skip header
                timesheet_reader.__next__()

                for row in timesheet_reader:
                    if row not in master_timesheet_list:
                        master_csv_writer.writerow(row)
                        added_counter += 1
                    else:
                        omitted_counter += 1
                
                # master_csv.write("\n")

        # Reload master into local memory
        self.load_master()
            
        print(f"Done: {added_counter} entries added, {omitted_counter} redundant entries omitted")


    def print_row(self, row_idx):
        curr_row = self.master_timesheet_dict[row_idx]
        print_arr = []
        print_arr.append(curr_row['Employee Name'])
        print_arr.append(curr_row['Date'])
        print_arr.append(curr_row['Start'])
        print_arr.append(curr_row['End'])
        print_arr.append(curr_row['Mealbreak'])
        print_arr.append(curr_row['Total Hours'])
        if curr_row['Leave']:
            print_arr.append(curr_row['Leave'].split(" ", 1)[0])
        else:
            print_arr.append(curr_row['Leave'])
        print_arr.append(curr_row['Manager\'s Comment'])

        print(" ".join(print_arr))


    def get_full_hours(self, mode, start):
        start_date = dt.date.fromisoformat(start)

        if mode == "ESD":
            end_date = start_date + dt.timedelta(days=6)
        elif mode == "payroll":
            second_week_start = start_date + dt.timedelta(days=7)
            end_date = start_date + dt.timedelta(days=13)

        names = []
        for row in self.master_timesheet_dict:
            row_date = dt.date.fromisoformat(row['Date'])
            if row_date >= start_date and row_date <= end_date:
                row_name = row['Employee Name']
                if row_name not in names:
                    names.append(row_name)
        
        for name in names:
            self.dump_data(name, mode=mode, start=start)

    def dump_data(self, name, mode=None, start=None):
        master_timesheet_dict = self.master_timesheet_dict

        today = dt.date.today()
        today_weekday = today.weekday()

        try:
            start_date = dt.date.fromisoformat(start)
        except ValueError:
            raise("Invalid date format")
        if (mode == "ESD" and start_date.weekday() != 6) or mode == "payroll" and start_date.weekday() != 4:
            print(f"WARNING: {start_date} ({calendar.day_name[start_date.weekday()]}) is not a valid {mode} start date.")

        if mode == "ESD":
            end_date = start_date + dt.timedelta(days=6)
            second_week_start = end_date+dt.timedelta(days=1)
        elif mode == "payroll":
            second_week_start = start_date + dt.timedelta(days=7)
            end_date = start_date + dt.timedelta(days=13)
        
        queried_rows = []
        hours_holder = HoursHolder()

        for i, row in enumerate(master_timesheet_dict):
            if row['Employee Name'] == name:
                row_date = dt.date.fromisoformat(row['Date'])

                # Save week 1 and week 2 stats separately
                if row_date >= start_date and row_date <= end_date:
                    if not hours_holder.week2 and row_date >= second_week_start:
                        queried_rows.append("newline")
                        hours_holder.week2 = True

                    queried_rows.append(i)

                    hours = float(row['Total Hours'])

                    # Determine leave type, if any, using first word of "leave" note
                    leave_keyword = row['Leave'].split(' ', 1)[0]
                    if leave_keyword == "Unpaid":
                        hours_holder.increment_hours(leave_hours=hours)
                    elif leave_keyword == "Sick":
                        hours_holder.increment_hours(sick_hours=hours)
                    else:
                        hours_holder.increment_hours(worked_hours=hours)

                    # Parse and tally break hours
                    break_time = row['Mealbreak'].split(":")
                    hours_holder.increment_hours(break_hours=dt.timedelta(hours=int(break_time[0]),
                                                                          minutes=int(break_time[1]),
                                                                          seconds=int(break_time[2])))
        
        # Output results
        with open (f'output/{start_date.isoformat()}_{end_date.isoformat()}.csv', mode='a', newline='') as output_csv:
            csv_writer = csv.writer(output_csv)
            csv_writer.writerow(self.master_timesheet_list[0])

            for idx in queried_rows:
                # Summary week 1
                
                if idx == "newline":
                    pass
                else:
                    self.print_row(idx)
                    csv_writer.writerow(self.master_timesheet_list[idx+1])
            '''
            print(f"Hours worked: {worked_hours}")
            print(f"Break hours: {break_hours}")
            print(f"Unpaid leave: {leave_hours}")
            print(f"Sick leave: {sick_hours}")

            if mode == "payroll":
                print("")
                print(f"Total hours worked: {week_1_worked_hours + worked_hours}")
                print(f"Total break hours: {week_1_break_hours + break_hours}")
                print(f"Total unpaid leave: {week_1_leave_hours + leave_hours}")
                print(f"Total sick leave: {week_1_sick_hours + sick_hours}")
            '''

            csv_writer.writerows(hours_holder.format_for_csv())
            

        print("\r----------------------------\r")



                    




        


    headers_backup = [
        '"Employee Export Code"', 
        '"Employee Name"',
        '"Date"', 
        '"Start"', '"End"', 
        '"Mealbreak"', 
        '"Total Hours"', 
        '"Total Cost"', 
        '"Employee Comment"', 
        '"Area Export Code"', 
        '"Area Name"', 
        '"Location Code"', 
        '"Location Name"', 
        '"Leave"', 
        '"Manager\'s Comment"', 
        '"Firstname"', 
        '"Lastname"', 
        '"Health Check 1"', 
        '"Health Check 2"']