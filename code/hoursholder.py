import datetime as dt

class HoursHolder:
    def __init__(self):
        self.week2 = False

        self.week_1_worked_hours = 0
        self.week_1_break_hours = dt.timedelta(0)
        self.week_1_leave_hours = 0
        self.week_1_sick_hours = 0

        self.week_2_worked_hours = 0
        self.week_2_break_hours = dt.timedelta(0)
        self.week_2_leave_hours = 0
        self.week_2_sick_hours = 0
    
    def increment_hours(self, worked_hours=0, break_hours=dt.timedelta(0), leave_hours=0, sick_hours=0):
        if not self.week2:
            self.week_1_worked_hours += worked_hours
            self.week_1_break_hours += break_hours
            self.week_1_leave_hours += leave_hours
            self.week_1_sick_hours += sick_hours
        
        else:
            self.week_2_worked_hours += worked_hours
            self.week_2_break_hours += break_hours
            self.week_2_leave_hours += leave_hours
            self.week_2_sick_hours += sick_hours


    def format_for_csv(self):
        to_return = [["", "Worked hours", "Break hours", "Leave hours", "Sick hours"]]

        to_return.append(["Week 1", self.week_1_worked_hours,
                                    self.week_1_break_hours,
                                    self.week_1_leave_hours,
                                    self.week_1_sick_hours])
        
        to_return.append(["Week 2", self.week_2_worked_hours,
                                    self.week_2_break_hours,
                                    self.week_2_leave_hours,
                                    self.week_2_sick_hours])

        to_return.append(["Total", self.week_1_worked_hours + self.week_2_worked_hours,
                                    self.week_1_break_hours + self.week_2_break_hours,
                                    self.week_1_leave_hours + self.week_2_leave_hours,
                                    self.week_2_sick_hours + self.week_2_sick_hours])
        
        to_return.append([])

        return to_return
