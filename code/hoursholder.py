import datetime as dt

class HoursHolder:
    def __init__(self, end_date):

        self.week_2_start = end_date-dt.timedelta(days=6)
        self.all_rows = []

        self.all_hours = {
            "week1": {
                "worked": 0,
                "break": False,
                "leave": 0,
                "sick": 0
                },
            "week2": {
                "worked": 0,
                "break": False,
                "leave": 0,
                "sick": 0
            }
                }


    def add_row(self, row):
        self.all_rows.append(row)

        # Determine leave
        if row["Date"] < self.week_2_start:
            week = "week1"
        else:
            week = "week2"

        if row["LeaveType"] == "Sick leave":
            time_type = "sick"
        elif row["LeaveType"] == "Unpaid leave":
            time_type = "leave"
        else:
            time_type = "worked"
        
        self.all_hours[week][time_type] += row["TotalTime"]

        self.all_hours[week]["break"] =  self.all_hours[week]["break"] or bool(row["MealbreakSlots"])
