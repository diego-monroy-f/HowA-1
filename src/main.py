#encoding:UTF-8
#Autor: Saul de Nova Caballero

#Python libraries
import pickle
from pprint import pprint

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

#Personal libraries imports
import CalendarUtils
from Activities import *
from HelpScreen import *
from ActivityLayouts import *

maxActivities = 20
daysList, actList, assList = [[] for i in range(7)], {}, []
actPointer, assPointer = 0, 0

#Change activities list and redraw calendar
def addActivity(activity):
	global assPointer, actPointer, daysList, actList, assList
	#print('LOL')
	if activity.actType == 1:
		activity.setId(actPointer)
		actList[actPointer] = activity
		for i in range(len(weekDaysNumbers)):
			if activity.days[weekDaysNumbers[i]]:
				daysList[i].append(actPointer)

		actPointer += 1
	else:
		assList.append(activity)
		assPointer += 1
	
	#print(actList, assList)
	#pprint(daysList)

def changeActivity(activity):
	removeActivity(activity)
	mainScreen.current = 'Activities Screen'
	HowAInstance.activitiesLayout.changeParameters(activity)

def removeActivity(activity):
	global daysList, actList, assList
	if activity.actType == 1:
		actId = activity.getId()
		daysList = [filter(lambda a: a!=actId, elem) for elem in daysList]
		actList.pop(actId)
		HowAInstance.mainContent.drawCalendar()
	else:
		actId = activity.getId()
		assList = filter(lambda a: a.getId() != actId, assList)
		HowAInstance.mainContent.proHomeContent.updateCalendar()

##################################################
##########             GUI 				##########
##################################################

#Main activityScreen
class ActivityScreen(GridLayout):

	def __init__(self, parameters='', **kwargs):

		self.cols = 1
		self.spacing = 10

		self.parameters = parameters
		self.exiting = False
		self.currentActivity = Activity()
		self.currentOption = ''

		super(ActivityScreen, self).__init__(**kwargs)
		
		self.actLayType = BoxLayout(orientation='horizontal', height=40, size_hint_y=None)
		self.actLayType.add_widget(Label(text='Activity Type: ', size_hint_x=None, width=150))
		self.actLayTypeButtons = []
		for posibleType in ['Fixed Activity','Project/Homework']:
			self.actLayTypeButtons.append(ToggleButton(text=posibleType, group='actTypes', size_hint_x=None, width=200))
			self.actLayTypeButtons[-1].bind(state=self.changeActivitiesLayout)
			self.actLayType.add_widget(self.actLayTypeButtons[-1])
		self.add_widget(self.actLayType)
		
		#Add personalized options on layout
		self.activitiesLayoutOptions = self.ActivitiesLayoutOptionsFun()
		self.add_widget(self.activitiesLayoutOptions)
	
	def changeParameters(self, activity):
		self.actLayTypeButtons[activity.actType-1].state = 'down'
		self.activitiesLayoutOptions.activityNameInstance.actNameTextInput.text = activity.name
		self.currentActivity = activity
		if activity.actType == 1:
			index = 0
			#print(activity.days)
			for elem in self.activitiesLayoutOptions.daysBoxList:
				if activity.days[weekDaysNumbers[index]]:
					#print(weekDaysNumbers[index])
					elem.state = 'down'
				index += 1

			self.activitiesLayoutOptions.textInputStart.text = activity.start
			self.currentActivity.start = activity.start
			self.activitiesLayoutOptions.textInputEnd.text = activity.end
			self.currentActivity.end = activity.end
		else:
			self.activitiesLayoutOptions.textInputAprox.text = activity.duration
			self.currentActivity.duration = activity.duration

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

		elif option == 'Project/Homework':
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
		if not self.exiting:
			if value == 'down':
				self.currentActivity.days[instance.text] = True
			else:
				self.currentActivity.days[instance.text] = False
	
	def changeStartTime(self, instance):
		#print('lol3')
		if validateTime(instance.text):
			self.currentActivity.start = instance.text
		else:
			button = Button(text='Invalid time')
			popup = Popup(title='ERROR!', content=button, size_hint=(None, None), height=250, width=250)
			button.bind(on_press=popup.dismiss)
			popup.open()
	
	def changeEndTime(self, instance):
		#print('lol4')
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
			popup.bind(on_dismiss=self.closeWindow)
			popup.open()
			addActivity(self.currentActivity)
		else:
			button = Button(text='There are fields missing\nor the data is incorrect!')
			popup = Popup(title='ERROR!', content=button, size_hint=(None, None), height=250, width=250)
			button.bind(on_press=popup.dismiss)
			popup.open()

	def closeWindow(self, *l):
		HowAInstance.mainContent.drawCalendar()
		HowAInstance.mainContent.proHomeContent.updateCalendar()
		self.exiting = True
		self.clearWindow()
		mainScreen.current = 'Main Screen'

	def clearWindow(self):
		self.activitiesLayoutOptions.activityNameInstance.actNameTextInput.text = ''
		if self.currentActivity.actType == 1:
			for elem in self.activitiesLayoutOptions.daysBoxList:
				elem.state='normal'
			self.activitiesLayoutOptions.textInputStart.text = ''
			self.activitiesLayoutOptions.textInputEnd.text = ''
		elif self.currentActivity.actType == 2:
			self.activitiesLayoutOptions.textInputAprox.text = ''
		else:
			raise ValueError
		for button in self.actLayTypeButtons:
			button.state = 'normal'
		self.currentActivity = Activity()


#Draw calendar objects definitions
class CalendarButton(FloatLayout):

	def __init__(self, activity, **kwargs):
		self.activity = activity

		super(CalendarButton, self).__init__()
		
		self.buttonInstance = Button(size_hint=(1, 1), pos_hint={'center_x':0.5, 'center_y':0.5}, **kwargs)
		self.buttonInstance.bind(on_release=self.onPressBubble)
		self.add_widget(self.buttonInstance)

		self.bubbleInstance = Bubble(size_hint=(None, None), size=(100, 40), pos_hint={'center_x':0.5, 'center_y':0.5}, arrow_pos='bottom_mid')
		
		self.bubbleChange = BubbleButton(text='Change', font_size=8)
		self.bubbleChange.bind(on_release=self.onPressChange)
		self.bubbleRemove = BubbleButton(text='Remove', font_size=8)
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
		changeActivity(self.activity)
	
	def onPressRemove(self, instance):
		self.remove_widget(self.bubbleInstance)
		removeActivity(self.activity)


class Calendar(GridLayout):
	
	def __init__(self, minSize, mode='week', **kwargs):
		self.cols = 1

		super(Calendar, self).__init__(**kwargs)
		
		self.bind(minimum_height=minSize)
		self.setMode(mode)
	
	def setMode(self, mode):
		self.clear_widgets()
		if mode == 'week':
			self.setWeekMode()
		elif mode == 'day':
			self.setDayMode()
	
	def setWeekMode(self):
		#TODO
		pass
	
	def setDayMode(self):
		weekDay = CalendarUtils.getCurrentWeekDay()
		self.calendarScreen = BoxLayout(orientation='vertical')
		#print(daysList[weekDay])
		for index in sorted(daysList[weekDay], key=(lambda x: convertTime(actList[x].start))):
			activity = actList[index]
			#print(activity.name)
			tempLayout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
			tempLayout.add_widget(Button(size_hint_x=None, width=150, text=activity.start + ' - ' + activity.end))
			tempLayout.add_widget(CalendarButton(activity=activity, text=activity.name))
			self.calendarScreen.add_widget(tempLayout)
		self.add_widget(self.calendarScreen)

class ProHomeContent(GridLayout):

	def __init__(self, minSize, **kwargs):
		self.cols=1

		super(ProHomeContent, self).__init__(**kwargs)
		self.bind(minimum_height=minSize)
		self.updateCalendar()
		
	def updateCalendar(self):
		self.clear_widgets()
		self.calendarScreen = BoxLayout(orientation='vertical')
		for activity in sorted(assList, key=(lambda x: x.duration)):
			#print(activity.name)
			tempLayout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
			tempLayout.add_widget(CalendarButton(activity=activity, text=activity.duration + " : " + activity.name))
			self.calendarScreen.add_widget(tempLayout)
		self.add_widget(self.calendarScreen)
			

class MainScreen(GridLayout):
	
	def __init__(self, **kwargs):
		self.cols = 2
		self.currentMode = 'week'
		self.calendar = Calendar(self.height-60)

		super(MainScreen, self).__init__(**kwargs)

		self.bind(height=self.drawCalendar)
		self.bind(width=self.drawCalendar)
		self.drawCalendar()

	def openScreenButtons(self, instance):
		if self.openSelectScreen == False:
			self.openSelectScreen = True
			self.selectScreen.open(instance)
		else:
			self.openSelectScreen = False
			self.selectScreen.dismiss()
	
	def changeSelectText(self, value):
		self.screenMode = value
		if value == 'day':
			self.calendar.setMode('day')
			self.selectScreenButton.text = CalendarUtils.returnCurrentDate()
		else:
			self.calendar.setMode('week')
			self.selectScreenButton.text = CalendarUtils.returnCurrentMonth()
	
	def changeCurrentScreen(self, instance):
		self.openSelectScreen = False
		self.selectScreen.dismiss()
		if instance.text == 'Day mode':
			self.currentMode = 'day'
			self.calendar.setMode('day')
			self.changeSelectText('day')
		elif instance.text == 'Week mode':
			self.currentMode = 'week'
			self.calendar.setMode('week')
			self.changeSelectText('week')
		elif instance.text == 'Add activity':
			mainScreen.current = 'Activities Screen'
		elif instance.text == 'Help Screen':
			mainScreen.current = instance.text
		else:
			raise ValueError
	
	def drawCalendar(self, *l):
		self.clear_widgets()
		#Main title design
		self.leftScreen = GridLayout(rows=2, size_hint_x=None, width=int(3*self.width//5))
		self.mainTitle = BoxLayout(background_color=(9, 9, 9, 1), size_hint_y=None, height=60)
		self.selectScreen = DropDown()
		self.openSelectScreen = False
		for option in ['Day mode', 'Week mode', 'Add activity', 'Help Screen']:
			tempButton = Button(text=option, size_hint_y=None, height=60)
			tempButton.bind(on_release=self.changeCurrentScreen)
			self.selectScreen.add_widget(tempButton)
		self.selectScreenButton = Button(text='Screens', size_hint=(None, None), font_size=16, height=60, width=300)
		self.selectScreenButton.bind(on_release=self.openScreenButtons)
		self.changeSelectText(self.currentMode)
		self.mainTitle.add_widget(self.selectScreenButton)

		#Initialize Main Calendar
		self.calendar = Calendar(self.height-60)
		self.calendar.setMode(self.currentMode)
		self.mainCalendar = ScrollView()
		self.mainCalendar.add_widget(self.calendar)

		#Add the main title and the calendar to the screen
		self.leftScreen.add_widget(self.mainTitle)
		self.leftScreen.add_widget(self.mainCalendar)
		self.add_widget(self.leftScreen)

		#Initialize homeworks and projects lists
		self.rightScreen = GridLayout(cols=1)

		#Change right up screen values Homeworks
		self.rightScreen.add_widget(Button(text='Homeworks/Projects', font_size=16, size_hint_y=None, height=60))
		self.proHome = ScrollView()
		self.proHomeContent = ProHomeContent(ProHomeContent(self.height-60))
		self.proHome.add_widget(self.proHomeContent)
		self.rightScreen.add_widget(self.proHome)
		self.add_widget(self.rightScreen)


class HowA(App):
	
	def build(self):
		global mainScreen, mainScreenInstance, activitiesScreenInstance, helpScreenInstance

		#Main screen initialization
		self.mainContent = MainScreen()

		#Activities screen initialization

		self.activitiesLayout = ActivityScreen()

		#Help screen initialization
		self.helpScreen = HelpScreen()
		
		#Add screen instances
		mainScreenInstance.add_widget(self.mainContent)
		activitiesScreenInstance.add_widget(self.activitiesLayout)
		helpScreenInstance.add_widget(self.helpScreen)

		mainScreen.current = 'Main Screen'

		return mainScreen


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
		daysList, actList, assList, actPointer = pickle.load(open('howa.conf', 'rb'))
		assPointer = len(assList)
	except Exception as e:
		daysList, actList, assList, actPointer = [[] for i in range(7)], {}, [], 0
	HowAInstance = HowA()
	HowAInstance.run()
	pickle.dump([daysList, actList, assList, actPointer], open('howa.conf', 'wb'))

