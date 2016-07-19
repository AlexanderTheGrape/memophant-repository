#memophant v0.2.3

import math
import sys
import time
from tkinter import *







root = Tk()

#'Frame' creates a frame, in this case using the main directory 'root'.

root.title('Memophant v0.2.3')

frame= Frame(root)
frame.pack()

#The following functions are used in various parts of the program. The use of functions reduces the amount of repeated code that needs to be used.

#deletes the frame, clears the tkinter window so that new content can replace it.
def deleteFrame(frame):
	frame.destroy()

#clears the frame and loads content for the main menu
def openMainMenu(frame):
	deleteFrame(frame)
	frame= Frame(root)
	frame.pack(side=TOP)

	mainMenuText = Label(frame, fg="black", text= "Main Menu", font="Calibri 12 bold", padx=200, pady=20)
	mainMenuText.pack()

	learnButton = Button(frame, padx=32, pady=16, bd=8, text="Learn", fg="black", font='Calibri 12 bold', command= lambda: openLearningListOptions(frame))
	learnButton.pack()

	newLearningListButton = Button(frame, padx=32, pady=16, bd=8, text="New Learning List", fg="black", font='Calibri 12 bold')
	newLearningListButton.pack()

#clears the tkinter frame and loads buttons for each learning list.
def openLearningListOptions(frame):
	deleteFrame(frame)
	frame= Frame(root)
	frame.pack()

	from os import walk

	f = []
	for (dirpath, dirnames, filenames) in walk('D:\Documents\School Subjects\Misc\Python\learningSets'):
		f.extend(filenames)
		break	
	print('directories are:', f)

	fileNameList = []
	for i in range(len(f)):
		fileNameList.append(f[i])
	print('asdfasdf ', fileNameList)
	
	buttons = []
	iCounter = -1
	for i in fileNameList:
		listButton = Button(frame, padx=32, pady=16, bd=8, text="%s" %(i), fg="black", font='Calibri 12 bold', command= lambda i=i: openLearningListContent(frame, i))
		listButton.pack()
		buttons.append(listButton)

#opens the learning list selected and reads the file to derive the questions and answers needed to test the user.
def openLearningListContent(frame, j):
	print('opening learning lists.')
	print('j is:', j)
	deleteFrame(frame)


	currentLearningSet = []
	currentAnswerSet = []

	paragraphCheck = 0
	with open('D:\Documents\School Subjects\Misc\Python\learningSets\\' + j) as f:
		for line in f:
			print('got to here')
			if line == 'Q:\n':
				print('got dem Qs')
				continue
			if line == '\n':
				print('got em!')
				paragraphCheck = 1
			if paragraphCheck == 0:
				currentLearningSet.append(line.strip('\n'))
			else:
				if line == 'A:\n' or line == '\n':
					continue
				else:
					print('this should be an answer:', line)
					currentAnswerSet.append(line.strip('\n'))


	print('questions:', currentLearningSet)
	print('answers:', currentAnswerSet)

	deleteFrame(frame)
	questionCounter = -1

	nextQuestion(frame, questionCounter, currentLearningSet, currentAnswerSet)

#clears the frame and loads the next question to ask. If the user just clicked the button of the file they'd like to use, it'll show the first question.			
def nextQuestion(frame, questionCounter,currentLearningSet, currentAnswerSet):
	deleteFrame(frame)

	print('question counter is:', questionCounter)
	if questionCounter + 1 == len(currentLearningSet):
		print('questions finished.')
		listCompleteScreen(questionCounter)
		return

	questionCounter += 1

	frame = Frame(root)
	frame.pack()

	questionNumberText = Label(frame, text="Question %s:" %(questionCounter + 1), font="Calibri 12 bold", pady=20)
	questionNumberText.pack()
	print(questionCounter)
	print('debug:', currentLearningSet[questionCounter])
	questionText = Label(frame, text="%s:" %(currentLearningSet[questionCounter]), font="Calibri 12 bold", pady=40, padx=20)
	questionText.pack()
	answerButton = Button(frame, padx=32, pady=16, bd=8, text="Answer", fg="black", font='Calibri 12 bold', command= lambda: showAnswer(frame, questionCounter, currentLearningSet, currentAnswerSet))
	answerButton.pack()

#clears the frame and shows the answer for the question previously asked.
def showAnswer(frame, questionCounter, currentLearningSet, currentAnswerSet):
	deleteFrame(frame)
	frame = Frame(root)
	frame.pack()

	questionNumberText = Label(frame, text="Answer for question %s:" %(questionCounter + 1), font="Calibri 12 bold", pady=20, padx=20)
	questionNumberText.pack()
	print(questionCounter)
	print('debug:', currentLearningSet[questionCounter])
	answerText = Label(frame, text="%s" %(currentAnswerSet[questionCounter]), font="Calibri 12 bold", pady=40, padx=20)
	answerText.pack()
	answerButton = Button(frame, padx=32, pady=16, bd=8, text="Next", fg="black", font='Calibri 12 bold', command= lambda: nextQuestion(frame, questionCounter, currentLearningSet, currentAnswerSet))
	answerButton.pack()

#clears the frame and shows how many things the user has learnt, with a congratulations.
def listCompleteScreen(questionCounter):

	frame=Frame(root)
	frame.pack()

	congratsText = Label(frame, text="Congratulations! You\'ve further memorised %s things!" %(questionCounter + 1), font="Calibri 18 bold", pady=40, padx=20)
	congratsText.pack()

	backButton = Button(frame, padx=32, pady=16, bd=8, text="Back to main menu", fg="black", font='Calibri 12 bold', command= lambda: openMainMenu(frame))
	backButton.pack()

	currentLearningSet = []
	currentAnswerSet = []

#resets the saved values for the question set and answer set so 
currentLearningSet = []
currentAnswerSet = []

#initiates the main menu to open upon opening the program.
openMainMenu(frame)

#part of the code needed to create the windows frame around the tkinter program.
root.mainloop()