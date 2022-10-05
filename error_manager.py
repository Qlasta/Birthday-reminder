import datetime as dt
import pandas as pd


class ValidateFile:
    def __init__(self):
        self.error_list = []

    def check_formats(self, all_birthdates, todays_date, day_after_week):
        """ Takes all birthdates data in dictionary format, today's date and the day we check for birthday.
        Modifies dates to next birthday date. Returns errors if mistakes found."""
        birthday_year = str(day_after_week.year)
        for n in all_birthdates:
            if pd.isna(all_birthdates[n]["Name"]):
                error = f"Error in row {n + 2}. Missing data: Name."
                self.error_list.append(error)
            else:
                pass
            if pd.isna(all_birthdates[n]["Email"]):
                error = f"Error in row {n + 2}. Missing data: Email."
                self.error_list.append(error)
            if pd.isna(all_birthdates[n]["Birthday"]):
                error = f"Error in row {n + 2}. Missing data: Birthday."
                self.error_list.append(error)
            else:
                try:
                    date = dt.datetime.strptime(all_birthdates[n]["Birthday"], "%Y-%m-%d")
                except ValueError:
                    try:
                        # does not validate 02-29
                        date = dt.datetime.strptime(all_birthdates[n]["Birthday"], "%m-%d")
                    except ValueError:
                        error = f"Error in row {n + 2}. Date format is not correct, please enter YYYY-MM-DD or MM-DD."
                        self.error_list.append(error)
                    else:
                        # format to next birthday date
                        all_birthdates[n]["Birthday"] = birthday_year + "-" + date.strftime("%m-%d")
                else:
                    if date > todays_date - dt.timedelta(days=1):
                        error = f"Error. Row {n + 2} -date format is not correct, date should be in the past."
                        self.error_list.append(error)
                    # format to next birthday date
                    all_birthdates[n]["Birthday"] = birthday_year + "-" + date.strftime("%m-%d")