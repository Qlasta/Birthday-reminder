import pandas as pd
import datetime as dt
from email_manager import SendEmails
from error_manager import ValidateFile
import sys

cmd_args = sys.argv


filename = "birthdays.csv"
try:
    df = pd.read_csv(filename, header=None, names=["Name", "Email", "Birthday"])
except FileNotFoundError:
    print(f"No such file in directory, please upload {filename} and try again.")
    exit()


all_birth_dates = df.to_dict(orient="index")

reminder_days = 7
today = dt.datetime.now()
day_after_week = today + dt.timedelta(days=reminder_days)
birthday_year = str(day_after_week.year)
validation = ValidateFile()
validation.check_formats(all_birth_dates, today, birthday_year)
print(all_birth_dates)


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
# Send emails
## 1.For all not birthday people
if len(only_birthdays):
    SendEmails().send_birthday_reminder(only_birthdays, not_birthdays, reminder_days)

## 2. If there are more than one birthday person, we inform each about another
    if len(only_birthdays) > 1:
        for n in only_birthdays:
            send_to = [n]
            about = [pers for pers in only_birthdays if pers != n]
            SendEmails().send_birthday_reminder(about, send_to, reminder_days)



print(not_birthdays)
print(only_birthdays)


