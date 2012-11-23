#encoding:UTF-8
#Autor: Saul de Nova Caballero

#Python libraries

import calendar
import pickle
import re
from datetime import datetime

#Start by importing kivy
import kivy
kivy.require('1.4.1')

#Import kivy application
from kivy.app import App

#Import kivy widgets
from kivy.uix.bubble import Bubble, BubbleButton
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton

helpRstText = '[size=20][color=000000][color=111111][b][size=24]Oh hai! It appears that you have reached the Help section, so here are some FAQ.[/size][/b][/color]\n\n[i]What is HowA?[/i]\n\nHowA is an activity administration program. Add activities ([b]homeworks[/b], [b]projects[/b] or [b]fixed activities[/b])\nto its calendar so you can easily see them in a list.\n\n[i]What is an [b]Activity[/b]?[/i]\n\nIt is a task related with your school or educational life that you must do,\nlike a project, a school assignment or extracurricular activities.\n\n[i]What is a [b]Fixed Activity[/b]?[/i]\n\nAn activity that you do frequently and regularly, like playing basketball or taking piano lessons.\nYou must specify the frequency of this activity (which days and how many hours).\n\n[i]What is a [b]Project[/b]?[/i]\n\nA schooltask that you must complete before a certain\ndue date, you must also actType in the approximate hours you will dedicate to completing this task.\n\n[i]What is a [b]Homework[/b]?[/i]\n\nIt is a task that you must hand in before a certain due date, you must also actType in the approximate\nhours you will dedicate to completing this task.\n\n[/size][/color]'
maxActivities = 20
timeFormat = re.compile('^(([0-1]?[0-9|2[0-3]):[0-5][0-9])')
weekDaysNumbers = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
months = ['January', ' February', ' March', ' April', ' May', ' June', ' August', ' September', ' October', ' November', ' December']
weekDays = {'Monday':False, 'Tuesday':False, 'Wednesday':False, 'Thursday':False, 'Friday':False, 'Saturday':False, 'Sunday':False}
daysList, actList, assList = [[] for i in range(7)], [], []
actPointer, assPointer = 0, 0

def convertTime(*args):
	value = []
	for time in args:
		if validateTime(time):
			hours, minutes=time.split(':')
			value.append(int(hours) * 60 + int(minutes))
	return value


def validateTime(time):
	if timeFormat.match(time) == None:
		return False
	return True

class Activity:
	def __init__(self, name='', actType=0):
		self.name = name
		self.actType = actType

	def getName(self):
		return self.name

	def getType(self):
		return self.actType

	def isComplete(self):
		return (self.name != '' and self.actType != 0)


class FixedActivity(Activity):
	
	def __init__(self, name='', days=weekDays, start='0:00', end='0:00', endDate=''):
		
		self.name = name
		self.actType = 1
		self.days = days
		self.start = start
		self.end = end
		self.endDate = endDate
		self.id = 0

	def setId(self, objId):
		self.id = objId
	
	def getStartTime(self):
		return self.start

	def getEndTime(self):
		return self.end

	def getDuration(self):
		return convertTime(self.end) - convertTime(self.start)
	
	def isComplete(self):
		return(self.name != '' and sum([int(day) for key, day in self.days.items()]) > 0 and (convertTime(self.end) - convertTime(self.start)) > 0)


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


def addActivity(activity):
	global assPointer, actPointer, daysList, actList, assList
	if activity.actType == 1:
		activity.setId(actPointer)
		actList.append(activity)
		for i in range(len(weekDaysNumbers)):
			if activity.days[weekDaysNumbers[i]]:
				daysList[i].append(actPointer)

		actPointer += 1
	else:
		assList.append(activity)
		assPointer += 1
	
class CalendarButton(Button):

	def __init__(self, **kwargs):
		super(CalendarButton, self).__init__(**kwargs)

		self.bubbleInstance = Bubble(size_hint=(None, None), size=(150, 50), arrow_pos='bottom_mid')
		self.bubbleInstance.bind(on_press=self.on_press_action)
		self.bubbleInstance.add_widget(BubbleButton())

	def on_press_action(self, instance):
		pass

class Calendar(FloatLayout):
	
	def __init__(self, mode='week', **kwargs):
		super(Calendar, self).__init__(**kwargs)

		self.setMode(mode)
	
	def setMode(self, mode):
		if mode == 'week':
			self.setWeekMode()
		elif mode == 'day':
			self.setDayMode()
	
	def setWeekMode(self):
		pass
	
	def setDayMode(self):
		currentDateTime = datetime.today()
		currentDay = weekDaysNumbers[currentDateTime.weekday()]
		currentDay = ''.join(list(currentDay)[:3]) + currentDateTime.day + ' ' + months[currentDateTime.month] + ' ' + currentDateTime.year()
		self.calendarScreen = GridLayout(cols=2)
		for index in daysList(currentDateTime.weekday()):
			activity = actList[index]
			tempButton = CalendarButton(text=activity.name)
			self.calendarScreen.add_widget(tempButton)
			
		return currentDay

class HowA(App):
	def build(self):
		self.currentOption = ''
		self.currentActivity = Activity()
		self.mainScreen = TabbedPanel()
		self.mainScreen.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

		#Main content tab initialization
		self.mainContent = GridLayout(rows=2)

		#Main title design
		self.mainCalendar = ScrollView()
		self.drawCalendar()
		self.mainContent.add_widget(self.mainCalendar)

		#Activities screen initialization

		self.activitiesLayout = GridLayout(cols=1, spacing=10, size_hint_y=None)
		self.activitiesLayout.bind(minimum_height=self.activitiesLayout.setter('height'))
		
		self.actLayName = BoxLayout(orientation='horizontal', height=40, size_hint_y=None)
		self.actLayName.add_widget(Label(text='Activity name: ', size_hint_x=None))
		self.actNameTextInput=TextInput(multiline=False)
		self.actNameTextInput.bind(on_text_validate=self.getNameActivity)
		self.actLayName.add_widget(self.actNameTextInput)
		self.activitiesLayout.add_widget(self.actLayName)

		self.actLayType = BoxLayout(orientation='horizontal', height=40, size_hint_y=None)
		self.actLayType.add_widget(Label(text='Activity actType: ', size_hint_x=None))
		for posibleType in ['Fixed Activity','Proyect','Homework']:
			tempButton=ToggleButton(text=posibleType, group='actTypes', size_hint_x=None)
			tempButton.bind(state=self.changeActivitiesLayout)
			self.actLayType.add_widget(tempButton)
		self.activitiesLayout.add_widget(self.actLayType)
		
		#Button to process addition
		self.buttonAdd = Button(text="Add the next activity", size_hint_x=None, width=250)
		self.buttonAdd.bind(on_press=self.collectData)

		#Add personalized options on layout
		self.activitiesLayoutOptions = self.ActivitiesLayoutOptions()
		self.activitiesLayout.add_widget(self.activitiesLayoutOptions)

		#Help screen initialization

		self.helpScreen = BoxLayout()
		self.helpScreen.add_widget(Button(text=helpRstText, markup=True, shorten=True, background_color=(9, 9, 9, 0.5)))

		#Main screen headers construction
		self.th1 = TabbedPanelHeader(text='Activities')
		self.th1.content = self.activitiesLayout

		self.th2 = TabbedPanelHeader(text='Help')
		self.th2.content = self.helpScreen

		#Set the main screen constructors
		self.mainScreen.default_tab_text = 'Calendar'
		self.mainScreen.default_tab_content = self.mainContent
		self.mainScreen.add_widget(self.th1)
		self.mainScreen.add_widget(self.th2)
		
		return self.mainScreen
	
	def drawCalendar(self):
		global daysList
		#Initialize scrolling
		self.mainCalendarContent = GridLayout(cols=1, spacing=10, size_hint_y=None)
		self.mainCalendarContent.bind(minimum_height=self.mainCalendarContent.setter('height'))

		if actPointer > 0 or assPointer > 0:
			index = 0
			for day in weekDays:
				if len(daysList[index]) > 0:
					self.mainCalendarContent.add_widget(Label(size_hint_y=None, height=40, text='[b][size=40]'+day+'[/size][/b]', markup=True))
					for idActivity in daysList[index]:
						activity = actList[idActivity]
						param1 = str(activity.getStartTime()) + ' - ' + str(activity.getEndTime())
						param2 = str(activity.getName())

						tempBoxLayout = BoxLayout(size_hint_y=None, height=(40 * (activity.getDuration()//60)), orientation='horizontal')
						tempBoxLayout.add_widget(Button(text=param1, size_hint_x=None, width=100, background_color=(5, 5, 5, 0.5)))
						tempBoxLayout.add_widget(Button(text=param2, background_color=(5, 5, 5, 0.5)))
						self.mainCalendarContent.add_widget(tempBoxLayout)

				index += 1

			if assPointer > 0:
				self.mainCalendarContent.add_widget(Label(size_hint_y=None, height=40, text='[b][size=40]Assignments[/size][/b]', markup=True))
				for activity in assList[:assPointer]:
					param1 = str(activity.getDuration())
					param2 = str(activity.getName())

					tempBoxLayout = BoxLayout(size_hint_y=None, height=(40 * (activity.getNumDuration()/60)), orientation='horizontal')
					tempBoxLayout.add_widget(Button(text=param1, size_hint_x=None, width=100, background_color=(5, 5, 5, 0.5)))
					tempBoxLayout.add_widget(Button(text=param2, background_color=(5, 5, 5, 0.5)))
					self.mainCalendarContent.add_widget(tempBoxLayout)

		else:
			self.mainCalendarContent.add_widget(Label(text='Add some activities to start', font_size=12))

		#Generate the scroll view
		self.mainCalendar.add_widget(self.mainCalendarContent)

	def ActivitiesLayoutOptions(self, option=''):
		if option == 'Fixed Activity':
			layout = GridLayout(cols=1, size_hint_y=None, height=170)

			tempBoxLayout = BoxLayout(size_hint_y=None, height=50,  orientation='horizontal')
			tempBoxLayout.add_widget(Label(text='Fixed activity days', size_hint_x=None, width=150))
			for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
				tempButton = ToggleButton(text=day, size_hint_x=None, width=90)
				tempButton.bind(state=self.changeDays)
				tempBoxLayout.add_widget(tempButton)
			layout.add_widget(tempBoxLayout)

			tempBoxLayout = GridLayout(cols=2, size_hint_y=None, height=80)

			tempBoxLayout.add_widget(Label(text='Activity hour start', size_hint_x=None, width=150))
			textInputStart = TextInput(multiline=False, size_hint_x=None, width=630)
			textInputStart.bind(on_text_validate=self.changeHourStart)
			tempBoxLayout.add_widget(textInputStart)

			tempBoxLayout.add_widget(Label(text='Activity hour end', size_hint_x=None, width=150))
			textInputEnd = TextInput(multiline=False, size_hint_x=None, width=630)
			textInputEnd.bind(on_text_validate=self.changeHourEnd)
			tempBoxLayout.add_widget(textInputEnd)

			layout.add_widget(tempBoxLayout)
			layout.add_widget(self.buttonAdd)

		elif option == 'Proyect' or option == 'Homework':
			layout = GridLayout(cols=2, size_hint_y=None, height=80)

			layout.add_widget(Label(text='%s aproximate hours' % option, size_hint_x=None, width=250))
			textInputAprox = TextInput(multiline=False, size_hint_x=None, width=530)
			textInputAprox.bind(on_text_validate=self.changeAprox)
			layout.add_widget(textInputAprox)
			
			layout.add_widget(self.buttonAdd)
		else:
			layout = GridLayout(cols=1, size_hint_y=None, height=40)
			layout.add_widget(self.buttonAdd)
		return layout


	def changeActivitiesLayout(self, instance, value):
		self.buttonAdd = Button(text="Add the next activity", size_hint_x=None, width=250)
		self.buttonAdd.bind(on_press=self.collectData)
		self.activitiesLayout.remove_widget(self.activitiesLayoutOptions)
		if value == 'down':
			if instance.text == 'Fixed Activity':
				self.currentActivity = FixedActivity(name=self.currentActivity.name)
			else:
				self.currentActivity = HomeProActivity(name=self.currentActivity.name)
			self.currentOption = instance.text
			self.activitiesLayoutOptions = self.ActivitiesLayoutOptions(instance.text)
		else:
			self.currentActivity = Activity(name=self.currentActivity.name)
			self.currentOption = ''
			self.activitiesLayoutOptions = self.ActivitiesLayoutOptions()
		self.activitiesLayout.add_widget(self.activitiesLayoutOptions)
	
	def getNameActivity(self, instance):
		self.currentActivity.name = str(instance.text)
	
	def changeDays(self, instance, value):
		if value == 'down':
			self.currentActivity.days[instance.text] = True
		else:
			self.currentActivity.days[instance.text] = False
	
	def changeHourStart(self, instance):
		if validateTime(instance.text):
			self.currentActivity.start = instance.text
		else:
			button = Button(text='Invalid time')
			popup = Popup(title='ERROR!', content=button, size_hint=(None, None), height=250, width=250)
			button.bind(on_press=popup.dismiss)
			popup.open()
	
	def changeHourEnd(self, instance):
		if validateTime(instance.text):
			self.currentActivity.end = instance.text
		else:
			button = Button(text='Invalid time')
			popup = Popup(title='ERROR!', content=button, size_hint=(None, None), height=250, width=250)
			button.bind(on_press=popup.dismiss)
			popup.open()
	
	def changeAprox(self, instance):
		if validateTime(instance.text):
			self.currentActivity.duration = instance.text
		else:
			button = Button(text='Invalid time')
			popup = Popup(title='ERROR!', content=button, size_hint=(None, None), height=250, width=250)
			button.bind(on_press=popup.dismiss)
			popup.open()
	
	def collectData(self, instance):
		if self.currentOption != '' and self.currentActivity.isComplete():
			print("LOL")
			button = Button(text='Activity successfully added')
			popup = Popup(title='SUCCESS!', content=button, size_hint=(None, None), height=250, width=250)
			button.bind(on_press=popup.dismiss)
			popup.open()
			addActivity(self.currentActivity)
			self.mainCalendar.remove_widget(self.mainCalendarContent)
			self.drawCalendar()
			self.currentActivity = Activity()
		else:
			button = Button(text='There are fields missing\nor the data is incorrect!')
			popup = Popup(title='ERROR!', content=button, size_hint=(None, None), height=250, width=250)
			button.bind(on_press=popup.dismiss)
			popup.open()

if __name__ in ('__main__', '__android__'):
	#Global variables
	try:
		daysList, actList, assList = pickle.load(open('howa.conf', 'rb'))
		actPointer = len(actList)
		assPointer = len(assList)
	except Exception as e:
		print(e)
		daysList, actList, assList = [[] for i in range(7)], [], []
	HowA().run()
	pickle.dump([daysList, actList, assList], open('howa.conf', 'wb'))

