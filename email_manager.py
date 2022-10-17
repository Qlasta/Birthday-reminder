import smtplib
import os
import time

USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")
ADMIN_EMAIL = USERNAME
SMTP_SERVER = "smtp.gmail.com"
PORT = 587
EMAIL_SEND_RETRIES = 3
SECONDS_TO_NEXT_RETRY = 5

def send_birthday_reminder(only_birthday_people, not_birthday_people, reminder_days):
    """Requires birthday people list, not birthday people list, days to remind before.
    Compiles letter with variables and sends only to not birthday people. Returns errors if appeared."""
    birthday_people_names = [b_person['Name'] for b_person in only_birthday_people]
    try_to_resend = True
    # Tries to send emails for set amount of times until success
    for n in range(EMAIL_SEND_RETRIES):
        if try_to_resend:
            try:
                with smtplib.SMTP(SMTP_SERVER, port=PORT) as connection:
                    connection.starttls()
                    connection.login(user=USERNAME, password=PASSWORD)
                    for person in not_birthday_people:
                        connection.sendmail(from_addr=USERNAME,
                                            to_addrs=person["Email"],
                                            msg=f"Subject: Birthday reminder\n\n Hi {person['Name']},\n The "
                                                f"birthday of {' and '.join(birthday_people_names)} are coming. "
                                                f"Be ready to congratulate on {only_birthday_people[0]['Next birthday']}!"
                                                f"\n It is in {reminder_days} days, do not miss it ;)")
                    try_to_resend = False
                    print("Success: emails were sent.")
            except smtplib.SMTPRecipientsRefused:
                error = "Wrong email address, email sending has stopped."
                print(error)
                send_errors(error)
                try_to_resend = False
            except:
                try_to_resend = True
                print("Something is wrong in email sending process. Retrying.")
                time.sleep(SECONDS_TO_NEXT_RETRY)
        else:
            pass
    if try_to_resend:
        error = "Something is wrong in email sending process. Emails were not sent."
        print(error)
        send_errors(error)


def send_errors(errors):
    """Requires string of errors, sends email to admin."""
    with smtplib.SMTP(SMTP_SERVER, port=PORT) as connection:
        connection.starttls()
        connection.login(user=USERNAME, password=PASSWORD)
        connection.sendmail(from_addr=USERNAME,
                            to_addrs=ADMIN_EMAIL,
                            msg=f"Subject: Errors in birthday file\n\n Error list:\n{errors}")
