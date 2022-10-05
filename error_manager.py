import datetime as dt
import pandas as pd


class ValidateFile:
    def __init__(self):
        self.error_list = []

    def check_formats(self, all_birthdates, todays_date, birthday_year):
        for n in all_birthdates:
            if pd.isna(all_birthdates[n]["Name"]):
                error = f"Error in row {n + 1}. Missing data: Name."
                self.error_list.append(error)
            else:
                pass
            if pd.isna(all_birthdates[n]["Email"]):
                error = f"Error in row {n + 1}. Missing data: Email."
                self.error_list.append(error)
            if pd.isna(all_birthdates[n]["Birthday"]):
                error = f"Error in row {n + 1}. Missing data: Birthday."
                self.error_list.append(error)
            else:
                try:
                    date = dt.datetime.strptime(all_birthdates[n]["Birthday"], "%Y-%m-%d")
                except ValueError:
                    try:
                        # does not validate 02-29
                        date = dt.datetime.strptime(all_birthdates[n]["Birthday"], "%m-%d")
                    except ValueError:
                        error = f"Error in row {n + 1}. Date format is not correct, please enter YYYY-MM-DD or MM-DD."
                        self.error_list.append(error)
                    else:
                        # format to next birthday date
                        all_birthdates[n]["Birthday"] = birthday_year + "-" + date.strftime("%m-%d")
                else:
                    if date > todays_date - dt.timedelta(days=1):
                        error = f"Error. Row {n + 1} -date format is not correct, date should be in the past."
                        self.error_list.append(error)
                    # format to next birthday date
                    all_birthdates[n]["Birthday"] = birthday_year + "-" + date.strftime("%m-%d")