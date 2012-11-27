#!/usr/bin/python3
#encoding:UTF-8
#Autor: Sauλ de Nova

#Kivy local libraries requierements
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton

#Personal libraries requierements

from Activities import weekDaysNumbers

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
		for day in weekDaysNumbers:
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
		self.textInputAprox = TextInput(multiline=False, size_hint_x=None, width=200, font_size=16)
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
	

