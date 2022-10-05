import pandas as pd
import datetime as dt
from email_manager import SendEmails
from error_manager import ValidateFile
import sys

cmd_args = sys.argv
reminder_days = 7
today = dt.datetime.now()
day_after_week = today + dt.timedelta(days=reminder_days)
filename = "birthdays.csv"

# Validate file and get data
try:
    df = pd.read_csv(filename)
    df.columns = ["Name", "Email", "Birthday"]
except FileNotFoundError:
    error_string = f"No such file in directory, please upload {filename} and try again."
    print(error_string)
    SendEmails().send_errors(error_string)
    exit()
all_birth_dates = df.to_dict(orient="index")

# Validate data format in file, exit if there are mistakes
validation = ValidateFile()
validation.check_formats(all_birth_dates, today, day_after_week)
if len(validation.error_list):
    print("Errors found (list has been sent to admin email). Please correct and try again.")
    error_string = ''
    for error in validation.error_list:
        error_string += "\n" + error
    print(error_string)
    SendEmails().send_errors(error_string)
    exit()
else:
    print("Success: file is valid.")

# Exit code if chosen command was only to validate
if len(cmd_args) > 1:
    if cmd_args[1] == "validate":
        exit()

# Get mailing lists
only_birthdays = []
not_birthdays = []

for n in all_birth_dates:
    if all_birth_dates[n]["Birthday"] == day_after_week.strftime("%Y-%m-%d"):
        only_birthdays.append(all_birth_dates[n])
    else:
        not_birthdays.append(all_birth_dates[n])

# Send emails if there are birthdays in chose days
## 1.For all not birthday people
if len(only_birthdays):
    SendEmails().send_birthday_reminder(only_birthdays, not_birthdays, reminder_days)

## 2. If there are more than one birthday person, we inform each about another
    if len(only_birthdays) > 1:
        for n in only_birthdays:
            send_to = [n]
            about = [pers for pers in only_birthdays if pers != n]
            SendEmails().send_birthday_reminder(about, send_to, reminder_days)
