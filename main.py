import pandas as pd
import datetime as dt
from email_manager import send_birthday_reminder
from error_manager import FileValidator
from dates_compiler import format_next_birthday_day
import os
import argparse

REMINDER_DAYS = 135
today = dt.datetime.now()
target_day = today + dt.timedelta(days=REMINDER_DAYS)
target_year = target_day.year
filename = "birthdays.csv"
all_birth_dates = {}

# CLI arguments
parser = argparse.ArgumentParser(description="Validate birthday file and send reminders",
                                 epilog="To run full program do not pass any arguments.")
parser.add_argument("-v", "--validate", action="store_true", help="only validate file, but not send emails")
cmd_args = parser.parse_args()
command = cmd_args.validate

# Validate data in file, reformat dates to next birthday or exit if there are mistakes.
validation = FileValidator(today, target_day)
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
if cmd_args.validate:
    exit()

# Get mailing lists
only_birthdays = []
not_birthdays = []

for n in all_birth_dates:
    next_birthday = format_next_birthday_day(all_birth_dates[n]["Birthday"], target_year)
    all_birth_dates[n]["Next birthday"] = next_birthday
    if next_birthday == target_day.strftime("%Y-%m-%d"):
        only_birthdays.append(all_birth_dates[n])
    else:
        not_birthdays.append(all_birth_dates[n])

# Send emails if there are birthdays in chosen days
#  1.For all not birthday people
if len(only_birthdays):
    send_birthday_reminder(only_birthdays, not_birthdays, REMINDER_DAYS)

#  2. If there are more than one birthday person, inform each about another
    if len(only_birthdays) > 1:
        for n in only_birthdays:
            send_to = [n]
            about_birthday = [pers for pers in only_birthdays if pers != n]
            send_birthday_reminder(about_birthday, send_to, REMINDER_DAYS)
