#memophant v0.2

import math
import sys
import time
from tkinter import *







root = Tk()

#'Frame' creates a frame, in this case using the main directory 'root'.

root.title('Memophant v0.1')

frame= Frame(root)
frame.pack()






			


def changeResetCheck():
	resetCheck = 1

def deleteFrame(frame):
	frame.destroy()

def openMainMenu(frame):
	deleteFrame(frame)
	frame= Frame(root)
	frame.pack(side=TOP)

	mainMenuText = Label(frame, fg="black", text= "Main Menu", font="Calibri 12 bold", padx=200, pady=20)
	mainMenuText.pack()

	learnButton = Button(frame, padx=32, pady=16, bd=8, text="Learn", fg="black", font='Calibri 12 bold', command= lambda: openLearningLists(frame))
	learnButton.pack()

	newLearningListButton = Button(frame, padx=32, pady=16, bd=8, text="New Learning List", fg="black", font='Calibri 12 bold')
	newLearningListButton.pack()

#def openExistingLists():
	#with open('D:\Documents\School Subjects\Misc\Python\learningSets\%s'

def openLearningLists(frame):
	print('opening learning lists.')
	deleteFrame(frame)

	paragraphCheck = 0
	with open('Letter learning.txt') as f:
		for line in f:
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

	#for i in currentLearningSet:
	#	global resetCheck
	#	resetCheck = 0
		
		
		#frame = Frame(root)
		#frame.pack()

		#questionNumberText = Label(frame, text="Question %s:" %questionCounter, font="Calibri 12 bold", pady=20)
		#questionNumberText.pack()
		#questionText = Label(frame, text="%s:" %i, font="Calibri 12 bold", pady=40)
		#questionText.pack()
		#answerButton = Button(frame, padx=32, pady=16, bd=8, text="Answer", fg="black", font='Calibri 12 bold', command=changeResetCheck)
		#answerButton.pack()

		#while resetCheck == 0:
		#	time.sleep(5)
		#	pass
		#print('resetCheck loop finished')
		#frame.destroy()
		#continue
			
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
	answerButton = Button(frame, padx=32, pady=16, bd=8, text="Answer", fg="black", font='Calibri 12 bold', command= lambda: nextQuestion(frame, questionCounter, currentLearningSet, currentAnswerSet))
	answerButton.pack()

def listCompleteScreen(questionCounter):

	frame=Frame(root)
	frame.pack()

	congratsText = Label(frame, text="Congratulations! You\'ve helped yourself memorise %s new things!" %(questionCounter + 1), font="Calibri 18 bold", pady=40, padx=20)
	congratsText.pack()

	backButton = Button(frame, padx=32, pady=16, bd=8, text="Back to main menu", fg="black", font='Calibri 12 bold', command= lambda: openMainMenu(frame))
	backButton.pack()




currentLearningSet = []
currentAnswerSet = []






openMainMenu(frame)
root.mainloop()