#!/usr/bin/python3
#encoding:UTF-8
#Autor: Sauλ de Nova

import calendar
from datetime import datetime
from pprint import pprint

mainCalendar = calendar.Calendar()
monthsNames = calendar.month_name
monthsThree = [''.join(list(x)[:3]) for x in calendar.month_name]
currDay = datetime.now().day
currMonth = datetime.now().month
currYear = datetime.now().year

def separateWeeks(daysList):
	for i in xrange(0, len(daysList), 7):
		yield daysList[i:i+7]

def getCurrentWeekDay():
	return calendar.weekday(currYear, currMonth, currDay)

def returnCurrentMonth():
	"""
	A function for returning the current week month in the format
	MMM : YYYY if the current week has more than two months, it returns
	MMM - MMM : YYYY
	"""
	monthDates = list(separateWeeks(list(mainCalendar.itermonthdays(currYear, currMonth))))
	for daysList in monthDates:
		if currDay in daysList:
			if daysList[0] == 0:
				return monthsThree[currMonth - 1] + ' - ' + monthsThree[currMonth] + ' : ' + str(currYear)
			if daysList[-1] == 0:
				return monthsThree[currMonth] + ' - ' + monthsThree[currMonth + 1] + ' : ' + str(currYear)
			return monthsThree[currMonth] + ' : ' + str(currYear)
	raise ValueError

def returnCurrentDate(americanTime=True):
	"""
	A function that returns the current date in the format DD MMM YYYY
	"""
	if americanTime:
		return "%s %s, %s" % (monthsNames[datetime.now().month], datetime.now().day, datetime.now().year)
	else:
		return "%s/%s/%s" % (datetime.now().day, monthsNames[datetime.now().month], datetime.now().year)

if __name__ == '__main__':
	print(returnCurrentDate(False))

