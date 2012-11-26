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

#Import kivy colors
from kivy.graphics import Color, Rectangle

#Import kivy widgets
from kivy.uix.bubble import Bubble, BubbleButton
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton

helpRstText = '[size=20][color=000000][color=111111][b][size=24]Oh hai! It appears that you have reached the Help section, so here are some FAQ.[/size][/b][/color]\n\n[i]What is HowA?[/i]\n\nHowA is an activity administration program. Add activities ([b]homeworks[/b], [b]projects[/b] or [b]fixed activities[/b])\nto its calendar so you can easily see them in a list.\n\n[i]What is an [b]Activity[/b]?[/i]\n\nIt is a task related with your school or educational life that you must do,\nlike a project, a school assignment or extracurricular activities.\n\n[i]What is a [b]Fixed Activity[/b]?[/i]\n\nAn activity that you do frequently and regularly, like playing basketball or taking piano lessons.\nYou must specify the frequency of this activity (which days and how many hours).\n\n[i]What is a [b]Project[/b]?[/i]\n\nA schooltask that you must complete before a certain\ndue date, you must also actType in the approximate hours you will dedicate to completing this task.\n\n[i]What is a [b]Homework[/b]?[/i]\n\nIt is a task that you must hand in before a certain due date, you must also actType in the approximate\nhours you will dedicate to completing this task.\n\n[/size][/color]'
maxActivities = 20
timeFormat = re.compile('^(([0-1]?[0-9|2[0-3]):[0-5][0-9])')
weekDaysNumbers = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
months = ['January', ' February', ' March', ' April', ' May', ' June', ' August', ' September', ' October', ' November', ' December']
weekDays = {'':False, 'Tuesday':False, 'Wednesday':False, 'Thursday':False, 'Friday':False, 'Saturday':False, 'Sunday':False}
daysList, actList, assList = [[] for i in range(7)], [], []
actPointer, assPointer = 0, 0

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


#Change activities list and redraw calendar

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

def changeActivity():
	print('Change')

def removeActivity():
	print('Remove')

##################################################
##########             GUI 				##########
##################################################

#Selected Fixed activity
class FActivityOption(GridLayout):

	def __init__(self, parameters='', **kwargs):
		#Design
		self.cols = 1
		self.size_hint_y = None
		self.pos_hint={'center_x':0.5, 'center_y':0.5}
		self.spacing = 10
		self.height = 170

		#Return parameters 
		self.activityName = ''

		#Change case variables
		self.parameters = parameters

		super(FActivityOption, self).__init__(**kwargs)

		#Add the activity name text box
		self.activityNameInstance = ActivityNameLayout(width=150)
		self.add_widget(self.activityNameInstance)

		#Make the day buttons
		self.daysBoxLayout = BoxLayout(size_hint_y=None, height=50,  orientation='horizontal')
		self.daysBoxLayout.add_widget(Label(text='Fixed activity days', size_hint_x=None, width=150))
		self.daysBoxList = []
		for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
			self.daysBoxList.append(ToggleButton(text=day, size_hint_x=None, width=90))
			self.daysBoxLayout.add_widget(self.daysBoxList[-1])
		self.add_widget(self.daysBoxLayout)

		#Generate the layout for the start and end textboxes
		self.timeBoxLayout = GridLayout(cols=2, size_hint_y=None, height=80)

		#Add the textboxes for the start time
		self.timeBoxLayout.add_widget(Label(text='Activity hour start:', size_hint_x=None, width=150))
		self.textInputStart = TextInput(multiline=False, size_hint_x=None, width=200, font_size=16)
		self.timeBoxLayout.add_widget(self.textInputStart)

		#Add the textboxes for the end time
		self.timeBoxLayout.add_widget(Label(text='Activity hour end:', size_hint_x=None, width=150))
		self.textInputEnd = TextInput(multiline=False, size_hint_x=None, width=200, font_size=16)
		self.timeBoxLayout.add_widget(self.textInputEnd)

		#Add the time widget
		self.add_widget(self.timeBoxLayout)

		#Add the activation button to invoke validation
		self.activateButton = AddActivityButton()
		self.add_widget(self.activateButton)
	

#Selected Proyect/Homework activity
class PActivityOption(GridLayout):

	def __init__(self, parameters='', **kwargs):

		#Design
		self.cols = 1
		self.spacing = 10

		#Return variables
		self.activityName = ''
		self.duration = '-1'

		#Change activity values
		self.parameters = parameters

		super(PActivityOption, self).__init__(**kwargs)

		#Add the activity name text box
		self.activityNameInstance = ActivityNameLayout()
		self.add_widget(self.activityNameInstance)

		#Add question label
		self.timeAproxLayout = GridLayout(cols=2, size_hint_y=None, height=40)
		self.timeAproxLayout.add_widget(Label(text='Approximate hours:', size_hint_x=None, width=150))
		self.textInputAprox = TextInput(multiline=False, size_hint_x=None, width=200)
		self.timeAproxLayout.add_widget(self.textInputAprox)
		self.add_widget(self.timeAproxLayout)

		#Add the data collection button
		self.activateButton = AddActivityButton()
		self.add_widget(self.activateButton)
		

#Collect all data from parameters and validate it
class AddActivityButton(Button):
	
	def __init__(self, **kwargs):
		self.text = 'Add the next activity'
		self.size_hint = (None, None)
		self.width = 150
		self.height = 100
		self.pos_hint = {'center_x':0.5, 'center_y':1}

		super(AddActivityButton, self).__init__(**kwargs)
	

#A class for collecting the activity name
#Missing bind command
class ActivityNameLayout(BoxLayout):
	
	def __init__(self, **kwargs):
		self.orientation = 'horizontal'
		self.height = 40
		self.size_hint_y = None
		self.activityName = ''

		super(ActivityNameLayout, self).__init__(**kwargs)

		self.add_widget(Label(text='Activity name: ', size_hint_x=None, width=150))
		self.actNameTextInput=TextInput(multiline=False, font_size=16)
		self.add_widget(self.actNameTextInput)
	

#Main activityScreen
class ActivityScreen(GridLayout):

	def __init__(self, parameters='', **kwargs):

		self.cols = 1
		self.spacing = 10

		self.parameters = parameters
		self.currentActivity = Activity()
		self.currentOption = ''

		super(ActivityScreen, self).__init__(**kwargs)
		
		self.actLayType = BoxLayout(orientation='horizontal', height=40, size_hint_y=None)
		self.actLayType.add_widget(Label(text='Activity Type: ', size_hint_x=None, width=150))
		for posibleType in ['Fixed Activity','Project','Homework']:
			tempButton=ToggleButton(text=posibleType, group='actTypes', size_hint_x=None)
			tempButton.bind(state=self.changeActivitiesLayout)
			self.actLayType.add_widget(tempButton)
		self.add_widget(self.actLayType)
		
		#Add personalized options on layout
		self.activitiesLayoutOptions = self.ActivitiesLayoutOptionsFun()
		self.add_widget(self.activitiesLayoutOptions)

	def ActivitiesLayoutOptionsFun(self, option=''):
		if option == 'Fixed Activity':
			layout = FActivityOption(parameters=self.parameters)

			#Make bindings
			layout.activityNameInstance.actNameTextInput.bind(on_text_validate=self.changeName)
			for elem in layout.daysBoxList:
				elem.bind(state=self.changeDays)
			layout.textInputStart.bind(on_text_validate=self.changeStartTime)
			layout.textInputEnd.bind(on_text_validate=self.changeEndTime)
			layout.activateButton.bind(on_press=self.collectData)

		elif option == 'Project' or option == 'Homework':
			layout = PActivityOption(parameters=self.parameters)

			#Make bindings
			layout.activityNameInstance.actNameTextInput.bind(on_text_validate=self.changeName)
			layout.textInputAprox.bind(on_text_validate=self.changeAprox)
			layout.activateButton.bind(on_press=self.collectData)
		else:
			layout = GridLayout(cols=1, size_hint_y=None, height=40)

		return layout


	def changeActivitiesLayout(self, instance, value):
		self.remove_widget(self.activitiesLayoutOptions)
		if value == 'down':
			if instance.text == 'Fixed Activity':
				self.currentActivity = FixedActivity(name=self.currentActivity.name)
			else:
				self.currentActivity = HomeProActivity(name=self.currentActivity.name)
			self.currentOption = instance.text
			self.activitiesLayoutOptions = self.ActivitiesLayoutOptionsFun(instance.text)
		else:
			self.currentActivity = Activity(name=self.currentActivity.name)
			self.currentOption = ''
			self.activitiesLayoutOptions = self.ActivitiesLayoutOptionsFun()
		self.add_widget(self.activitiesLayoutOptions)
	
	def changeName(self, instance):
		#print('lol1')
		self.currentActivity.name = str(instance.text)
	
	def changeDays(self, instance, value):
		#print('lol2')
		self.currentActivity.name = str(instance.text)
		if value == 'down':
			self.currentActivity.days[instance.text] = True
		else:
			self.currentActivity.days[instance.text] = False
	
	def changeStartTime(self, instance):
		#print('lol3')
		self.currentActivity.name = str(instance.text)
		if validateTime(instance.text):
			self.currentActivity.start = instance.text
		else:
			button = Button(text='Invalid time')
			popup = Popup(title='ERROR!', content=button, size_hint=(None, None), height=250, width=250)
			button.bind(on_press=popup.dismiss)
			popup.open()
	
	def changeEndTime(self, instance):
		#print('lol4')
		self.currentActivity.name = str(instance.text)
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
			button = Button(text='Activity successfully added')
			popup = Popup(title='SUCCESS!', content=button, size_hint=(None, None), height=250, width=250)
			button.bind(on_press=popup.dismiss)
			popup.open()

			#Clear activity parameters
			if self.currentActivity.actType == 1:
				#print(self.activitiesLayoutOptions.activityNameInstance.actNameTextInput.text)
				self.activitiesLayoutOptions.activityNameInstance.actNameTextInput.text = ''
				for elem in self.activitiesLayoutOptions.daysBoxList:
					#print(elem.state)
					elem.state='normal'
				#print(self.activitiesLayoutOptions.textInputStart.text)
				#print(self.activitiesLayoutOptions.textInputEnd.text)
				self.activitiesLayoutOptions.textInputStart.text = ''
				self.activitiesLayoutOptions.textInputEnd.text = ''

			addActivity(self.currentActivity)
			mainScreen.current = 'Main Screen'
		else:
			button = Button(text='There are fields missing\nor the data is incorrect!')
			popup = Popup(title='ERROR!', content=button, size_hint=(None, None), height=250, width=250)
			button.bind(on_press=popup.dismiss)
			popup.open()


#Help Screen Class
class HelpScreen(BoxLayout):
	
	def __init__(self, **kwargs):
		
		super(BoxLayout, self).__init__(**kwargs)

		self.add_widget(Label(text=helpRstText, markup=True))

#Draw calendar objects definitions
class CalendarButton(FloatLayout):

	def __init__(self, **kwargs):
		self.pos_hint={'center_x':0.5, 'center_y':0.5}
		self.size_hint=(1, 1)

		super(CalendarButton, self).__init__()
		
		self.buttonInstance = Button(size_hint=(1, 1), pos_hint={'center_x':0.5, 'center_y':0.5}, **kwargs)
		self.buttonInstance.bind(on_release=self.onPressBubble)
		self.add_widget(self.buttonInstance)

		self.bubbleInstance = Bubble(size_hint=(None, None), size=(150, 50), pos_hint={'center_x':0.5, 'center_y':0.5}, arrow_pos='bottom_mid')
		
		self.bubbleChange = BubbleButton(text='Change')
		self.bubbleChange.bind(on_release=self.onPressChange)
		self.bubbleRemove = BubbleButton(text='Remove')
		self.bubbleRemove.bind(on_release=self.onPressRemove)
		
		self.bubbleInstance.add_widget(self.bubbleChange)
		self.bubbleInstance.add_widget(self.bubbleRemove)

	def onPressBubble(self, instance):
		if self.bubbleInstance.parent == None:
			self.add_widget(self.bubbleInstance)
		else:
			self.remove_widget(self.bubbleInstance)
	
	def onPressChange(self, instance):
		self.remove_widget(self.bubbleInstance)
		changeActivity()
	
	def onPressRemove(self, instance):
		self.remove_widget(self.bubbleInstance)
		removeActivity()

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
		global mainScreen, mainScreenInstance, activitiesScreenInstance, helpScreenInstance
		self.currentOption = ''
		self.currentActivity = Activity()

		#Main content tab initialization
		self.mainContent = GridLayout(rows=2)

		#Main title design
		self.mainTitle = BoxLayout(background_color=(9, 9, 9, 1), size_hint_y=None, height=100)
		self.selectScreen = DropDown()
		self.openSelectScreen = False
		for option in ['Main Screen', 'Activities Screen', 'Help Screen']:
			tempButton = Button(text=option, size_hint_y=None, height=60)
			tempButton.bind(on_release=self.changeCurrentScreen)
			self.selectScreen.add_widget(tempButton)
		self.selectScreenButton = Button(text='Screens', size_hint=(None, None), height=60, width=150)
		self.selectScreenButton.bind(on_release=self.openScreenButtons)
		self.mainTitle.add_widget(self.selectScreenButton)

		#Initialize Main Calendar
		self.mainCalendar = ScrollView()
		self.drawCalendar()
		self.mainContent.add_widget(self.mainTitle)
		self.mainContent.add_widget(self.mainCalendar)

		#Activities screen initialization

		self.activitiesLayout = ActivityScreen()
		#self.activitiesLayout = GridLayout(cols=1, spacing=10, size_hint_y=None)
		#self.activitiesLayout.bind(minimum_height=self.activitiesLayout.setter('height'))
		
		#self.actLayName = BoxLayout(orientation='horizontal', height=40, size_hint_y=None)
		#self.actLayName.add_widget(Label(text='Activity name: ', size_hint_x=None))
		#self.actNameTextInput=TextInput(multiline=False)
		#self.actNameTextInput.bind(on_text_validate=self.getNameActivity)
		#self.actLayName.add_widget(self.actNameTextInput)
		#self.activitiesLayout.add_widget(self.actLayName)

		#self.actLayType = BoxLayout(orientation='horizontal', height=40, size_hint_y=None)
		#self.actLayType.add_widget(Label(text='Activity actType: ', size_hint_x=None))
		#for posibleType in ['Fixed Activity','Project','Homework']:
		#	tempButton=ToggleButton(text=posibleType, group='actTypes', size_hint_x=None)
		#	tempButton.bind(state=self.changeActivitiesLayout)
		#	self.actLayType.add_widget(tempButton)
		#self.activitiesLayout.add_widget(self.actLayType)
		
		#Button to process addition
		#self.buttonAdd = Button(text="Add the next activity", size_hint_x=None, width=250)
		#self.buttonAdd.bind(on_press=self.collectData)

		#Add personalized options on layout
		#self.activitiesLayoutOptions = self.ActivitiesLayoutOptions()
		#self.activitiesLayout.add_widget(self.activitiesLayoutOptions)

		#Help screen initialization

		self.helpScreen = HelpScreen()
		
		mainScreenInstance.add_widget(self.mainContent)
		activitiesScreenInstance.add_widget(self.activitiesLayout)
		helpScreenInstance.add_widget(self.helpScreen)

		mainScreen.current = 'Main Screen'

		return mainScreen

	def openScreenButtons(self, instance):
		if self.openSelectScreen == False:
			self.openSelectScreen = True
			self.selectScreen.open(instance)
		else:
			self.openSelectScreen = False
			self.selectScreen.dismiss()
	
	def changeCurrentScreen(self, instance):
		self.openSelectScreen = False
		self.selectScreen.dismiss()
		mainScreen.current = instance.text
	
	def drawCalendar(self):
		global daysList
		#Initialize scrolling
		self.mainCalendarContent = GridLayout(cols=1, spacing=10, size_hint_y=None)
		self.mainCalendarContent.bind(minimum_height=self.mainCalendarContent.setter('height'))

		if actPointer > 0 or assPointer > 0:
			index = 0
			for day in weekDays:
				if len(daysList[index]) > 0:
					self.mainCalendarContent.add_widget(Label(size_hint_y=None, height=40, text=day, font_size=40))
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
				self.mainCalendarContent.add_widget(Label(size_hint_y=None, height=40, text='Assignments', font_size=40))
				for activity in assList[:assPointer]:
					param1 = str(activity.getDuration())
					param2 = str(activity.getName())

					tempBoxLayout = BoxLayout(size_hint_y=None, height=(40 * (activity.getNumDuration()/60)), orientation='horizontal')
					tempBoxLayout.add_widget(Button(text=param1, size_hint_x=None, width=100, background_color=(5, 5, 5, 0.5)))
					tempBoxLayout.add_widget(Button(text=param2, background_color=(5, 5, 5, 0.5)))
					self.mainCalendarContent.add_widget(tempBoxLayout)

		else:
			self.mainCalendarContent.add_widget(CalendarButton(text='Add some activities to start', font_size=12))

		#Generate the scroll view
		self.mainCalendar.add_widget(self.mainCalendarContent)


if __name__ in ('__main__', '__android__'):
	#Global variables
	mainScreen = ScreenManager(transition=SlideTransition())
	mainScreenInstance = Screen(name='Main Screen')
	activitiesScreenInstance = Screen(name='Activities Screen') 
	helpScreenInstance = Screen(name='Help Screen')
	mainScreen.add_widget(mainScreenInstance)
	mainScreen.add_widget(activitiesScreenInstance)
	mainScreen.add_widget(helpScreenInstance)

	try:
		daysList, actList, assList = pickle.load(open('howa.conf', 'rb'))
		actPointer = len(actList)
		assPointer = len(assList)
	except Exception as e:
		print(e)
		daysList, actList, assList = [[] for i in range(7)], [], []
	HowA().run()
	pickle.dump([daysList, actList, assList], open('howa.conf', 'wb'))

