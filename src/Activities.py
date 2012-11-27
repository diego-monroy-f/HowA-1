#!/usr/bin/python3
#encoding:UTF-8
#Autor: Sauλ de Nova

import re

timeFormat = re.compile('^(([0-1]?[0-9|2[0-3]):[0-5][0-9])')
weekDaysNumbers = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
months = ['January', ' February', ' March', ' April', ' May', ' June', ' August', ' September', ' October', ' November', ' December']
weekDays = {'Monday':False, 'Tuesday':False, 'Wednesday':False, 'Thursday':False, 'Friday':False, 'Saturday':False, 'Sunday':False}

#Converts a time HH:MM to the number of minutes
def convertTime(time):
	if validateTime(time):
		hours, minutes=time.split(':')
		return int(hours) * 60 + int(minutes)
	return -1

def validateTime(time):
	if timeFormat.match(time) == None:
		return False
	return True

class Activity:
	def __init__(self, name='', actType=0):
		self.name = name
		self.actType = actType
		self.objId = 0

	def setId(self, objId):
		self.objId = objId

	def getId(self):
		return self.objId

	def getName(self):
		return self.name

	def getType(self):
		return self.actType

	def isComplete(self):
		return (self.name != '' and self.actType != 0)


class FixedActivity(Activity):
	
	def __init__(self, name='', days=weekDays, start=-1, end=-1, endDate=''):
		
		self.name = name
		self.actType = 1
		self.days = days
		self.start = start
		self.end = end
		self.endDate = endDate
	
	def getStartTime(self):
		return self.start

	def getEndTime(self):
		return self.end

	def getDuration(self):
		return convertTime(self.end) - convertTime(self.start)
	
	def isComplete(self):
		return(self.name != '' and sum([int(day) for key, day in self.days.items()]) > 0 and validateTime(self.end) and validateTime(self.start) and
			   (convertTime(self.end) - convertTime(self.start)) > 0)


class HomeProActivity(Activity):

	def __init__(self, name='', duration='0:00'):
		
		self.name = name
		self.actType = 2
		self.duration = duration
	
	def getNumDuration(self):
		return convertTime(self.duration)
	
	def getDuration(self):
		return self.duration
	
	def isComplete(self):
		return (self.name != '' and convertTime(self.duration) > 0)


