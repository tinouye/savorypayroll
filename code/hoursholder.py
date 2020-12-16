import datetime as dt

class HoursHolder:
    time_types = ["worked", "overtime", "break", "leave", "sick"]
    row_headers = ["Employee", "Date", "StartTime", "EndTime", "MealbreakSlots", "TotalTime", "LeaveType", "ManagerComment"]
    def __init__(self, end_date):
        
        self.week_2_start = end_date-dt.timedelta(days=6)
        self.all_rows = []

        self.all_hours = {
            "week1": {
                "worked": 0,
                "break": False,
                "leave": 0,
                "sick": 0,
                "overtime": 0
                },
            "week2": {
                "worked": 0,
                "break": False,
                "leave": 0,
                "sick": 0,
                "overtime": 0
            },
            "total": {
                "worked": 0,
                "break": False,
                "leave": 0,
                "sick": 0,
                "overtime": 0
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

        '''
        # Process overtime
        if time_type = "worked" and self.all_hours[week]["worked"] > 40:
            self.all_hours[week]["overtime"] += 40-self.all_hours[week]["worked"]
        '''

        self.all_hours[week]["break"] = self.all_hours[week]["break"] or bool(row["MealbreakSlots"])

    def post_processing(self):
        # Process overtime
        for week in self.all_hours:
            if self.all_hours[week]["worked"] > 40:
                self.all_hours[week]["overtime"] = self.all_hours[week]["worked"] - 40
                self.all_hours[week]["worked"] = 40
        
        # Sum week1 and week2 into total
        for time_type in self.time_types:
            self.all_hours["total"][time_type] = self.all_hours["week1"][time_type] + self.all_hours["week2"][time_type]
