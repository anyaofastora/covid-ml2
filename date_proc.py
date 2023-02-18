def date_to_number(date):
    time = date.split("-")
    year = time[0]
    month = time[1]
    day = time[2]
    if int(year)%4 == 0:
        leap_year = 1
    else:
        leap_year = 0
    year_day = [365,366]
    month_day = [31,28+leap_year,31,30,31,30,31,31,30,31,30,31]
    result = 0
    for i in range(int(year)-2020):
        if i % 4 == 0:
            leap = 1
        else:
            leap= 0
        result += year_day[leap]
    for i in range(int(month)-1):
        result += month_day[i]
    result += int(day)
    return result



def is_added_year(year):
    if year%4 == 0:
        return 366
    else:
        return 365

def number_to_date(num):
    # print(num)
    for i in range(2020,2100):
        if num - is_added_year(i) < 0:
            break
        else:
            num = num - is_added_year(i)
    year = i
    if year%4 == 0:
        leap = 1
    else:
        leap = 0
    num += year-2020
    if num == 365+leap:
        year += 1
        num = 1
    # print(num)
    month_list = [31,28+leap,31,30,31,30,31,30,30,31,30,31]
    for i in range(12):
        if num - month_list[i] <= 0:
            break
        else:
            num -= month_list[i]
    month = i+1
    if month < 10:
        month = "0" + str(month)
    else:
        month = str(month)
    date = num
    if date < 10:
        date = "0" + str(date)
    else:
        date = str(date)
    return str(year) + "-" + month + "-" + date

if __name__ == "__main__":
    print(number_to_date(913))