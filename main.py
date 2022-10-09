import pandas as pd
import datetime as dt
from email_manager import SendEmails
from error_manager import ValidateFile
import sys
import os

cmd_args = sys.argv
reminder_days = 7
today = dt.datetime.now()
target_day = today + dt.timedelta(days=reminder_days)
filename = "birthdays.csv"
all_birth_dates = {}

# Validate data in file, reformat dates to next birthday or exit if there are mistakes.
validation = ValidateFile(today, target_day)
if os.path.exists(filename):
    if validation.check_csv_is_parsable(filename):
        df = pd.read_csv(filename, index_col=False)
        df.columns = ["Name", "Email", "Birthday"]
        all_birth_dates = df.to_dict(orient="index")
        validation.check_formats(all_birth_dates)
        if not len(validation.error_list):
            print("Success: file is valid.")
        else:
            validation.show_errors()
            exit()
    else:
        validation.show_errors()
        exit()
else:
    validation.error_list.append(f"No such file in directory, please upload {filename} and try again.")
    validation.show_errors()
    exit()


# Exit code if chosen command was only to validate
if len(cmd_args) > 1:
    if len(cmd_args) == 2 and cmd_args[1] == "validate":
        exit()
    else:
        "Wrong command. Try again."
        exit()

# Get mailing lists
only_birthdays = []
not_birthdays = []

for n in all_birth_dates:
    if all_birth_dates[n]["Birthday"] == target_day.strftime("%Y-%m-%d"):
        only_birthdays.append(all_birth_dates[n])
    else:
        not_birthdays.append(all_birth_dates[n])

# Send emails if there are birthdays in chosen days
#  1.For all not birthday people
if len(only_birthdays):
    SendEmails().send_birthday_reminder(only_birthdays, not_birthdays, reminder_days)

#  2. If there are more than one birthday person, inform each about another
    if len(only_birthdays) > 1:
        for n in only_birthdays:
            send_to = [n]
            about_birthday = [pers for pers in only_birthdays if pers != n]
            SendEmails().send_birthday_reminder(about_birthday, send_to, reminder_days)
