import smtplib
import os
import time

username = os.environ.get("USERNAME")
password = os.environ.get("PASSWORD")
smtp_server = "smtp.gmail.com"
port = 587
email_send_retries = 3
seconds_to_next_retry = 5


class SendEmails:
    def send_birthday_reminder(self,only_birthday_people, not_birthday_people, reminder_days):
        birthday_people_names = []
        for b_person in only_birthday_people:
            birthday_people_names.append(b_person['Name'])
        try_to_send = True
        for n in range(email_send_retries):
            if try_to_send:
                try:
                    with smtplib.SMTP(smtp_server, port=port) as connection:
                        connection.starttls()
                        connection.login(user=username, password=password)
                        for person in not_birthday_people:
                            print(person["Email"])
                            print(f"For: {person['Name']}")
                            print(f"About: {' and '.join(birthday_people_names)}")
                            print(only_birthday_people[0]['Birthday'])
                            print(reminder_days)
                            # connection.sendmail(from_addr=username,
                            #                     to_addrs=person["Email"],
                            #                     msg=f"Subject: Birthday reminder\n\n Hi {person['Name']},\n "
                            #                         f"the birthday of {birthday_people_names} are coming. Be ready to congratulate "
                            #                         f"on {' and '.join(birthday_people_names)} !\n It is in {reminder_days} "
                            #                         f"days,do not miss it ;)")
                        try_to_send = False
                except smtplib.SMTPRecipientsRefused:
                    print(f"Wrong email address, email sending has stopped.")
                    try_to_send = False
                except:
                    try_to_send = True
                    time.sleep(seconds_to_next_retry)
                    print("attempt")
            else:
                pass