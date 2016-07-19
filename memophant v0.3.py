#memophant v0.2.3

import math
import sys
import time
import json
import random
from tkinter import *







root = Tk()

#'Frame' creates a frame, in this case using the main directory 'root'.

root.title('Memophant v0.3')

frame= Frame(root)
frame.pack()

global namingQuestionCounter
namingQuestionCounter = 1

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

	newLearningListButton = Button(frame, padx=32, pady=16, bd=8, text="New Learning List", fg="black", font='Calibri 12 bold', command= lambda: newLearningList(frame))
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


	QsAndAs = []

	paragraphCheck = 0
	debugCounter = 0
	with open('D:\Documents\School Subjects\Misc\Python\learningSets\\' + j) as f:
		for line in f:
			debugCounter += 1
			QsAndAs.append(json.loads(line))
			print('THE PARSED LINE IS:', json.loads(line))
			print('LINE %s HAS PASSED!' %debugCounter)

	print('QsAndAs is:', QsAndAs)

	#now to randomise the questions
	random.shuffle(QsAndAs)
	print('the randomised QsAndAs is:', QsAndAs)

	deleteFrame(frame)
	questionCounter = -1

	nextQuestion(frame, questionCounter, QsAndAs)

#clears the frame and loads the next question to ask. If the user just clicked the button of the file they'd like to use, it'll show the first question.			
def nextQuestion(frame, questionCounter, QsAndAs):
	deleteFrame(frame)

	print('question counter is:', questionCounter)
	if questionCounter + 1 == len(QsAndAs):
		print('questions finished.')
		listCompleteScreen(questionCounter)
		return

	questionCounter += 1

	frame = Frame(root)
	frame.pack()

	questionNumberText = Label(frame, text="Question %s:" %(questionCounter + 1), font="Calibri 12 bold", pady=20)
	questionNumberText.pack()
	print(questionCounter)
	#print('debug:', QsAndAs[questionCounter[0])
	questionText = Label(frame, text="%s:" %((QsAndAs[questionCounter])[0]), font="Calibri 12 bold", pady=40, padx=20)
	questionText.pack()
	answerButton = Button(frame, padx=32, pady=16, bd=8, text="Answer", fg="black", font='Calibri 12 bold', command= lambda: showAnswer(frame, questionCounter, QsAndAs))
	answerButton.pack()

#clears the frame and shows the answer for the question previously asked.
def showAnswer(frame, questionCounter, QsAndAs):
	deleteFrame(frame)
	frame = Frame(root)
	frame.pack()

	questionNumberText = Label(frame, text="Answer for question %s:" %(questionCounter + 1), font="Calibri 12 bold", pady=20, padx=20)
	questionNumberText.pack()
	print(questionCounter)
	answerText = Label(frame, text="%s" %((QsAndAs[questionCounter])[1]), font="Calibri 12 bold", pady=40, padx=20)
	answerText.pack()
	answerButton = Button(frame, padx=32, pady=16, bd=8, text="Next", fg="black", font='Calibri 12 bold', command= lambda: nextQuestion(frame, questionCounter, QsAndAs))
	answerButton.pack()

#clears the frame and shows how many things the user has learnt, with a congratulations.
def listCompleteScreen(questionCounter):

	frame=Frame(root)
	frame.pack()

	congratsText = Label(frame, text="Congratulations! You\'ve further memorised %s things!" %(questionCounter + 1), font="Calibri 18 bold", pady=40, padx=20)
	congratsText.pack()

	backButton = Button(frame, padx=32, pady=16, bd=8, text="Back to main menu", fg="black", font='Calibri 12 bold', command= lambda: openMainMenu(frame))
	backButton.pack()

	QsAndAs = []

def newLearningList(frame):
	deleteFrame(frame)
	frame=Frame(root)
	frame.pack()

	createListButton =  Button(frame, padx=32, pady=16, bd=8, text="Create List", fg="black", font='Calibri 12 bold', command= lambda: instructionsPage(frame))
	createListButton.pack()

	preMadeListButton = Button(frame, padx=32, pady=16, bd=8, text="Premade List", fg="black", font='Calibri 12 bold', command= lambda: testingScreen(frame))
	preMadeListButton.pack()



def instructionsPage(frame):
	deleteFrame(frame)
	frame=Frame(root)
	frame.pack()

	instructions = Label(frame, fg="black", text= "Instructions for making new Learning Sets:", font="Calibri 12 bold", padx=200, pady=20)
	instructions.pack()

	instructions = Label(frame, fg="black", text= "Learning sets consist of groups of a question and answer. You will be prompted to provide a question and then the corresponding answer. Enter the required text in the box provided and click 'next' or press the ENTER button. After at least one question and answer has been provided, you will be able to complete the set by pressing the 'finish' and it will be saved", font="Calibri 12", padx=200, pady=20)
	instructions.pack()

	instructions = Label(frame, fg="black", text= "You will be prompted to provide a question and then the corresponding answer. Enter the required text in the box provided and click 'next' or press the ENTER button. After at least one question and answer has been provided, you will be able to complete the set by pressing the 'finish' and it will be saved", font="Calibri 12", padx=200, pady=20)
	instructions.pack()

	OkButton = Button(frame, padx=32, pady=16, bd=8, text="OK", fg="black", font='Calibri 12 bold', command= lambda: createLearningList(frame))
	OkButton.pack()

def createLearningList(frame):
	deleteFrame(frame)
	frame=Frame(root)
	frame.pack()

	global namingQuestionCounter

	#Asks for user input in the form of a question
	questionPrompt = Label(frame, fg="black", text= "What is question %s going to be?" % namingQuestionCounter, font="Calibri 12 bold", padx=200, pady=20)
	questionPrompt.pack()

	txtDisplay = Entry(frame, textvariable = frame, bd=20, insertwidth=1, font=30)
	txtDisplay.pack(side =TOP)

	txtDisplay.bind('<KeyPress>', keyPress)
	txtDisplay.pack()
	txtDisplay.focus()

def keyPress(event):

	currentText = txtDisplay.get()

	if event.keysym in ('Return'):
		print('Return encountered')
		#now retrieve the current text in the box and save it to the file. Then ask for the corresponding answer.
		
		print('currentText is:', currentText)
		print('debug:', namingQuestionCounter)


	elif event.keysym not in ('Alt_r', 'Alt_L', 'F4', 'Left', 'Right','Delete', 'BackSpace', 'Return'):
		print(event.keysym)

def writeToFile():
	print('the current namingQuestionCounter is:', namingQuestionCounter)

























#
##Currenlty working  below on making the enter button start the 'asking' of the next question, and possibly include the number of question it is currently on. Get the typed question to be saved as a text file.
#

















def inputNextQuestion(frame):
	deleteFrame(frame)
	frame=Frame(root)
	frame.pack()

	#Asks for user input in the form of a question
	questionPrompt = Label(frame, fg="black", text= "What is your question going to be?", font="Calibri 12 bold", padx=200, pady=20)
	questionPrompt.pack()

	txtDisplay = Entry(frame, textvariable = frame, bd=20, insertwidth=1, font=30)
	txtDisplay.pack(side =TOP)

	txtDisplay.bind('<KeyPress>', keyPress)
	txtDisplay.pack()
	txtDisplay.focus()

def testingScreen(frame):
	deleteFrame(frame)
	frame=Frame(root)
	frame.pack()

	OkButton = Button(frame, padx=32, pady=16, bd=8, text="OK", fg="black", font='Calibri 12 bold', command= lambda: testingScreen(frame))
	OkButton.pack()

#resets the saved values for the questions and answers.
QsAndAs = []


#initiates the main menu to open upon opening the program.
openMainMenu(frame)

#part of the code needed to create the windows frame around the tkinter program.
root.mainloop()