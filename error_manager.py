import datetime as dt
import pandas as pd
from email_manager import send_errors


class FileValidator:
    def __init__(self, today, target_day):
        self.error_list = []
        self.todays_date = today

    def check_csv_is_parsable(self, filename):
        try:
            df = pd.read_csv(filename, index_col=False)
        except pd.errors.ParserError:
            self.error_list.append(f"Data shape in file is not correct, please format to 3 valid columns and try "
                                   f"again.")
            return False
        else:
            if len(df.columns) != 3:
                self.error_list.append(f"Data shape in file is not correct, please format to 3 valid columns and try "
                                       f"again.")
                return False
            else:
                return True

    def check_formats(self, all_birthdates):
        """ Requires all birthdates data in dictionary format. Modifies dates to next birthday date.
        Ads errors to list if mistakes found."""
        if all_birthdates == {}:
            error = f"File is empty, please fill in the file and try again."
            self.error_list.append(error)
        for n in all_birthdates:
            if pd.isna(all_birthdates[n]["Name"]):
                error = f"Error in row {n + 2}. Missing data: Name."
                self.error_list.append(error)
            if pd.isna(all_birthdates[n]["Email"]):
                error = f"Error in row {n + 2}. Missing data: Email."
                self.error_list.append(error)
            if pd.isna(all_birthdates[n]["Birthday"]):
                error = f"Error in row {n + 2}. Missing data: Birthday."
                self.error_list.append(error)
            else:
                # Format validation
                # - to validate 02-29
                if all_birthdates[n]["Birthday"] == '02-29':
                    all_birthdates[n]["Birthday"] = '1904-02-29'
                try:
                    date = dt.datetime.strptime(all_birthdates[n]["Birthday"], "%Y-%m-%d")
                except ValueError:
                    try:
                        dt.datetime.strptime(all_birthdates[n]["Birthday"], "%m-%d")
                    except ValueError:
                        error = f"Error in row {n + 2}. Date is out of range or format is not correct, please enter " \
                                f"YYYY-MM-DD or MM-DD."
                        self.error_list.append(error)
                else:
                    if date > self.todays_date - dt.timedelta(days=1):
                        error = f"Error. Row {n + 2}. Date format is not correct, date should be in the past."
                        self.error_list.append(error)

    def show_errors(self):
        """Displays errors from list and sends by email."""
        error_string = ''
        for error in self.error_list:
            error_string += "\n" + error
        print("Errors found (list has been sent to admin email). Please correct and try again.")
        print(error_string)
        send_errors(error_string)
