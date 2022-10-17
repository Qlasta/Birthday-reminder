def is_leap_year(year):
    year = int(year)
    if year % 4 == 0 and year % 100 != 0:
        return True
    elif year % 400 == 0:
        return True
    else:
        return False

def format_next_birthday_day(birthday, target_year):
    """ Requires birthdate string in "%m-%d" or "%Y-%m-%d" format and year. Returns birthday string date in given year."""
    month_day = birthday[-5:]
    if not is_leap_year(target_year) and month_day == "02-29":
        return str(target_year) + "-03-01"
    else:
        return str(target_year) + "-" + month_day


