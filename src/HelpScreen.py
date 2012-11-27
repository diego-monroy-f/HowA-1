#!/usr/bin/python3
#encoding:UTF-8
#Autor: Sauλ de Nova

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

helpRstText = '[size=20][color=000000][color=111111][b][size=24]Oh hai! It appears that you have reached the Help section, so here are some FAQ.[/size][/b][/color]\n\n[i]What is HowA?[/i]\n\nHowA is an activity administration program. Add activities ([b]homeworks[/b], [b]projects[/b] or [b]fixed activities[/b])\nto its calendar so you can easily see them in a list.\n\n[i]What is an [b]Activity[/b]?[/i]\n\nIt is a task related with your school or educational life that you must do,\nlike a project, a school assignment or extracurricular activities.\n\n[i]What is a [b]Fixed Activity[/b]?[/i]\n\nAn activity that you do frequently and regularly, like playing basketball or taking piano lessons.\nYou must specify the frequency of this activity (which days and how many hours).\n\n[i]What is a [b]Project[/b]?[/i]\n\nA schooltask that you must complete before a certain\ndue date, you must also actType in the approximate hours you will dedicate to completing this task.\n\n[i]What is a [b]Homework[/b]?[/i]\n\nIt is a task that you must hand in before a certain due date, you must also actType in the approximate\nhours you will dedicate to completing this task.\n\n[/size][/color]'

#Help Screen Class
class HelpScreen(BoxLayout):
	
	def __init__(self, **kwargs):
		
		super(BoxLayout, self).__init__(**kwargs)

		self.add_widget(Label(text=helpRstText, markup=True))
