#!/usr/bin/env python3
import calendar
import datetime
import re


def get_year_month(d):
    """
    :param datetime_obj: a datetime object ; for example : datetime.datetime.now()
    :return: a datetime object
    """
    return d.year, d.month


def get_pre_datetime(datetime_obj):
    """
    :param datetime_obj: a datetime object ; for example : datetime.datetime.now()
    :return: a datetime object
    """
    days_count = datetime.timedelta(days=datetime_obj.day)
    pre_month_last_day_datetime_obj = datetime_obj - days_count
    return pre_month_last_day_datetime_obj


def get_next_datetime(datetime_obj):
    """
    :param datetime_obj: a datetime object ; for example : datetime.datetime.now()
    :return: a datetime object
    """
    days_count = calendar.monthrange(datetime_obj.year, datetime_obj.month)[1]
    next_month_datetime = datetime_obj + datetime.timedelta(days=days_count+1) - datetime.timedelta(datetime.datetime.now().day)
    return next_month_datetime


def day_format(datetime_obj, cal_str):
    """
    :param datetime_obj: a datetime object ; for example : datetime.datetime.now()
    :param d: a datetime object ; for example : datetime.datetime.now()
    :return: a datetime object
    """
    day = datetime_obj.day
    reg_num = "\D{}\D".format(day)
    reg = re.search(reg_num, cal_str).group()
    ret = re.sub('\d+', "\033[31m{}\033[0m".format(day), reg)
    return re.sub(reg, ret, cal_str)

if __name__ == '__main__':
    currnet_time = datetime.datetime.now()

    pre_year_month = get_year_month(get_pre_datetime(currnet_time))
    currnet_year_month = get_year_month(currnet_time)
    next_year_month = get_year_month(get_next_datetime(currnet_time))


#    with open('/var/tmp/cal.log', 'w') as f:
#        f.write(calendar.month(*pre_year_month, w=3, l=1))
#        f.write(day_format(currnet_time, calendar.month(*currnet_year_month, w=3, l=1)))
#        f.write(calendar.month(*next_year_month, w=3, l=1))
    calendar.setfirstweekday(calendar.SUNDAY)
    print(calendar.month(*pre_year_month, w=3, l=1))
    print(day_format(currnet_time, calendar.month(*currnet_year_month, w=3, l=2)))
    print(calendar.month(*next_year_month, w=3, l=1))