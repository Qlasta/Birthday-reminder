# Birthday-reminder
Program reads birthdays.cvs, validates data and sends birthday reminders

- Update file birthdays.csv with the list of people's birthdays. Name, Email and Birth date (in format YYYY-MM-DD or MM-DD) are required fields. First row sould be a header.
- Commit changes.
- Program will automaticaly start file validation. You can check the result in Actions→Workflows→All workflows→Check if file is valid.
- If there are any errors, you will see the list printed and copy will be sent to admin email.
- Program runs every day at 11:00 GMT+3, checks if there are upcoming birthdays after week and sends reminder letters to all except birthday people.
- Program will not send any emails if there are mistakes in the file.


How to launch on terminal:
- Make sure you have python3 installed (`sudo apt-get install python3`)
- Make sure you have git installed (`sudo apt-get install git`)
- Make sure you have pip installed (`sudo apt install python3-pip`)
- Make sure you have pandas installed (`python3 -m pip install --upgrade pip pandas`)
- Make sure you have env. variables set (USERNAME and PASSWORD).
- To clone program start: `git clone https://github.com/Qlasta/Birthday-reminder.git`
- Go into directory: `cd Birthday-reminder`
- Update file if needed: birthdays.csv in working directory.
- To run only validation of data in file, start: `python3 main.py validate`
- To run full program start: `python3 main.py`

