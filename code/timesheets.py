from hoursholder import HoursHolder
import datetime as dt
import csv

def format_output(end_date, rows_json):
    rows_json = process_json(rows_json)
    if not rows_json:
        print("No rows found")
        return
    
    all_hours = aggregate_data(end_date, rows_json)
    output_csv(end_date, all_hours)

def process_json(rows_json):
    # Determine columns to remove
    keep_keys = {"Employee", "Date", "StartTime", "EndTime", "MealbreakSlots", "TotalTime", "LeaveType", "ManagerComment"}
    all_keys = set(rows_json[0].keys())
    del_keys = all_keys-keep_keys
    leave_types = {
        '1': "Sick leave",
        '2': "Holiday leave",
        '3': "Long service leave",
        '4': "Parental leave",
        '5': "Bereavement leave",
        '6': "Carer's leave",
        '7': "Unpaid leave",
        '8': "Time in lieu",
        '9': "Training"
    }

    for i, row in enumerate(rows_json):
        # Grab displayname from employeeobject and add as key-value to row
        row["Employee"] = row["EmployeeObject"]["DisplayName"]

        # Get rid of datetime nonsense
        row["Date"] = dt.date.fromisoformat(row["Date"].split("T")[0])
        row["StartTime"] = dt.datetime.fromtimestamp(row["StartTime"]).time().isoformat()
        row["EndTime"] = dt.datetime.fromtimestamp(row["EndTime"]).time().isoformat()

        # Add leave type to row (sick or unpaid)
        if row["IsLeave"]:
            row["LeaveType"] = leave_types[row["LeaveRuleObject"]["Type"]]
            row.pop("LeaveRuleObject")
        else:
            row["LeaveType"] = None

        # Convert mealbreaks to human-readable times
        if row["MealbreakSlots"]:
            meal_keys = list(row["MealbreakSlots"].keys())
            for key in meal_keys:
                row["MealbreakSlots"][dt.datetime.fromtimestamp(int(key)).time().isoformat()] = row["MealbreakSlots"][key]
                row["MealbreakSlots"].pop(key)

        # Create comment for Validation flag
        if row["ValidationFlag"] == 16384:
            row["ManagerComment"] = "Time sheet was automatically closed"
        else:
            row["ManagerComment"] = None

        '''
        row["Mealbreak"] = 0
        if row["MealbreakSlots"]:
            if type(row["MealbreakSlots"]) != dict or len(row["MealbreakSlots"]) != 2:
                print("Something went wrong with meal breaks because they're programmed poorly")
                print(row)

            else:
                break_timestamps = list(row["MealbreakSlots"].keys())
                row["Mealbreak"] = abs(int(break_timestamps[1])-int(break_timestamps[0]))/3600
        '''

        # Remove unneeded columns
        for key in del_keys:
            row.pop(key)
    
    return rows_json
                

def aggregate_data(end_date, rows_json):
    employee_hours_dict = {}
    for row in rows_json:
        curr_employee = row["Employee"]
        if curr_employee not in employee_hours_dict:
            employee_hours_dict[curr_employee] = HoursHolder(end_date)
        
        employee_hours_dict[curr_employee].add_row(row)

    return employee_hours_dict


def output_csv(end_date, all_hours):
    # Hack to get headers from dictionary
    for employee in all_hours:
        fieldnames = list(all_hours[employee].all_rows[0].keys())
        break


    try:
        with open (f'output/payroll_ending_{end_date.isoformat()}.csv', mode='x', newline='') as output_csv:
            csv_dictwriter = csv.DictWriter(output_csv, fieldnames=fieldnames)
            csv_writer = csv.writer(output_csv)

            for employee in all_hours:
                csv_dictwriter.writeheader()
                for row in all_hours[employee].all_rows:
                    csv_dictwriter.writerow(row)

                total_worked = all_hours[employee].all_hours["week1"]["worked"] + all_hours[employee].all_hours["week2"]["worked"]
                total_break = all_hours[employee].all_hours["week1"]["break"] or all_hours[employee].all_hours["week2"]["break"]
                total_leave = all_hours[employee].all_hours["week1"]["leave"] + all_hours[employee].all_hours["week2"]["leave"]
                total_sick = all_hours[employee].all_hours["week1"]["sick"] + all_hours[employee].all_hours["week2"]["sick"]

                csv_writer.writerow(["","Worked Hours", "Break Hours", "Leave Hours", "Sick Hours"])
                csv_writer.writerow(["Week 1", all_hours[employee].all_hours["week1"]["worked"], all_hours[employee].all_hours["week1"]["break"], all_hours[employee].all_hours["week1"]["leave"], all_hours[employee].all_hours["week1"]["sick"]])
                csv_writer.writerow(["Week 2", all_hours[employee].all_hours["week2"]["worked"], all_hours[employee].all_hours["week2"]["break"], all_hours[employee].all_hours["week2"]["leave"], all_hours[employee].all_hours["week2"]["sick"]])
                csv_writer.writerow(["Total", total_worked, total_break, total_leave, total_sick])
                csv_writer.writerow(["\n"])
    
    except FileExistsError:
        print("Payroll csv for this period already exists. Please delete that file and try again. Aborting.")

    print("\r----------------------------\r")