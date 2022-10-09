import smtplib
import os
import time

USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")
admin_email = USERNAME
smtp_server = "smtp.gmail.com"
port = 587
email_send_retries = 3
seconds_to_next_retry = 5


class SendEmails:
    def send_birthday_reminder(self, only_birthday_people, not_birthday_people, reminder_days):
        """Requires birthday people list, not birthday people list, days to remind before.
        Compiles letter with variables and sends only to not birthday people. Returns errors if appeared."""
        birthday_people_names = [b_person['Name'] for b_person in only_birthday_people]
        try_to_resend = True
        # Tries to send emails for set amount of times until success
        for n in range(email_send_retries):
            if try_to_resend:
                try:
                    with smtplib.SMTP(smtp_server, port=port) as connection:
                        connection.starttls()
                        connection.login(user=USERNAME, password=PASSWORD)
                        for person in not_birthday_people:
                            connection.sendmail(from_addr=USERNAME,
                                                to_addrs=person["Email"],
                                                msg=f"Subject: Birthday reminder\n\n Hi {person['Name']},\n The "
                                                    f"birthday of {' and '.join(birthday_people_names)} are coming. "
                                                    f"Be ready to congratulate on {only_birthday_people[0]['Birthday']}!"
                                                    f"\n It is in {reminder_days} days, do not miss it ;)")
                        try_to_resend = False
                        print("Success: emails were sent.")
                except smtplib.SMTPRecipientsRefused:
                    error = "Wrong email address, email sending has stopped."
                    print(error)
                    self.send_errors(error)
                    try_to_resend = False
                except:
                    try_to_resend = True
                    print("Something is wrong in email sending process. Retrying.")
                    time.sleep(seconds_to_next_retry)
            else:
                pass
        if try_to_resend:
            error = "Something is wrong in email sending process. Emails were not sent."
            print(error)
            self.send_errors(error)

    def send_errors(self, errors):
        """Requires string of errors, sends email to admin."""
        with smtplib.SMTP(smtp_server, port=port) as connection:
            connection.starttls()
            connection.login(user=USERNAME, password=PASSWORD)
            connection.sendmail(from_addr=USERNAME,
                                to_addrs=admin_email,
                                msg=f"Subject: Errors in birthday file\n\n Error list:\n{errors}")
