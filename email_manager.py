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
        """Takes birthday people list, not birthday people list, days to remind before.
        Compiles letter with variables and sends only to not birthday people. Returns errors if appeared."""
        birthday_people_names = []
        for b_person in only_birthday_people:
            birthday_people_names.append(b_person['Name'])
        try_to_send = True
        # Tries to send emails for set amount of times until success
        for n in range(email_send_retries):
            if try_to_send:
                try:
                    with smtplib.SMTP(smtp_server, port=port) as connection:
                        connection.starttls()
                        connection.login(user=USERNAME, password=PASSWORD)
                        for person in not_birthday_people:
                            connection.sendmail(from_addr=USERNAME,
                                                to_addrs=person["Email"],
                                                msg=f"Subject: Birthday reminder\n\n Hi {person['Name']},\n "
                                                    f"the birthday of {' and '.join(birthday_people_names)} are coming. Be ready to congratulate "
                                                    f"on {only_birthday_people[0]['Birthday']}!\n It is in {reminder_days} "
                                                    f"days, do not miss it ;)")
                        try_to_send = False
                        print("Success: emails were sent.")
                except smtplib.SMTPRecipientsRefused:
                    error = "Wrong email address, email sending has stopped."
                    print(error)
                    self.send_errors(error)
                    try_to_send = False
                except:
                    try_to_send = True
                    print("Something is wrong in email sending process. Retrying.")
                    time.sleep(seconds_to_next_retry)
            else:
                pass
        if try_to_send == True:
            error = "Something is wrong in email sending process. Emails were not sent."
            print(error)
            self.send_errors(error)

    def send_errors(self, errors):
        """ Sends email to admin, by giving errors in string format."""
        with smtplib.SMTP(smtp_server, port=port) as connection:
            connection.starttls()
            connection.login(user=USERNAME, password=PASSWORD)
            connection.sendmail(from_addr=USERNAME,
                                    to_addrs=admin_email,
                                    msg=f"Subject: Errors in birthday file\n\n Error list:\n{errors}")

