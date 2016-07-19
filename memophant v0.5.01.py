#memophant v0.2.3

import math
import sys
import time
import json
import random
import os.path
from tkinter import *







root = Tk()

#'Frame' creates a frame, in this case using the main directory 'root'.

root.title('Memophant v0.5')
root.geometry('800x600+200+100')


global frame
frame= Frame(root)
frame.pack()

global namingQuestionCounter
namingQuestionCounter = 0

passedInstructionsPage = False

global mode
mode = 'mainMenu'

global currentText



#The following functions are used in various parts of the program. The use of functions reduces the amount of repeated code that needs to be used.

#deletes the frame, clears the tkinter window so that new content can replace it.
def deleteFrame(frame):
	frame.destroy()



#clears the frame and loads content for the main menu
def openMainMenu(frame):
	deleteFrame(frame)
	frame= Frame(root)
	frame.pack()

	mainMenuText = Label(frame, fg="black", text= "Main Menu", font="Calibri 12 bold", padx=200, pady=20)
	mainMenuText.pack()

	learnButton = Button(frame, width = 20, height=3, bd=4, text="Learn", fg="black", font='Calibri 12 bold', command= lambda: openLearningListOptions(frame))
	learnButton.pack()

	newLearningListButton = Button(frame, width = 20, height=3, bd=4, text="New Learning List", fg="black", font='Calibri 12 bold', command= lambda: newLearningList(frame))
	newLearningListButton.pack()

	print('size:', root.winfo_screenwidth(), 'x', root.winfo_screenheight())






#OPTION 1: 'LEARN'




#clears the tkinter frame and loads buttons for each learning list.
def openLearningListOptions(frame):
	deleteFrame(frame)
	frame= Frame(root)
	frame.pack()

	from os import walk

	f = []
	for (dirpath, dirnames, filenames) in walk('D:\Documents\School Subjects\Misc\Python\learningSets2'):
		f.extend(filenames)
		break
	print('directories are:', f)

	fileNameList = []
	for i in range(len(f)):
		fileNameList.append(f[i])
	
	buttons = []
	iCounter = -1
	for i in fileNameList:
		listButton = Button(frame, width = 40, height = 3, bd=4, text="%s" %(i), fg="black", font='Calibri 12 bold', command= lambda i=i: openLearningListContent(frame, i))
		listButton.pack()
		buttons.append(listButton)





#opens the learning list selected and reads the file to derive the questions and answers needed to test the user.
def openLearningListContent(frame, j):
	deleteFrame(frame)

	global fileName
	fileName = j
	print('fileName is:', fileName)

#f.write(json.dumps(new_entry) + '\n')
	QsAndAs = []

	paragraphCheck = 0
	debugCounter = 0
	with open('D:\Documents\School Subjects\Misc\Python\learningSets2\\' + j) as f:
		for line in f:
			debugCounter += 1
			try:
				strippedLine = line.strip('\n')
				QsAndAs.append(json.loads(strippedLine))
			except:
				print('didnt work!')


	#now to randomise the questions
	random.shuffle(QsAndAs)

	#answerHistory = []
	#for i in QsAndAs:
#		answerHistory.append(i[2:])


	answerHistory = QsAndAs[2:]
	print('-----------answerHistory is:', answerHistory)

	questionCounter = -1

	sessionAnswerInfo = [0, 0]

	nextQuestion(frame, questionCounter, QsAndAs, sessionAnswerInfo)

#clears the frame and loads the next question to ask. If the user just clicked the button of the file they'd like to use, it'll show the first question.			
def nextQuestion(frame, questionCounter, QsAndAs, sessionAnswerInfo):
	deleteFrame(frame)
	frame = Frame(root)
	frame.pack()

	print('question counter is:', questionCounter)
	print('------------Next question initiated')
	if questionCounter + 1 == len(QsAndAs):
		listCompleteScreen(frame, questionCounter, QsAndAs, sessionAnswerInfo)
		return

	global mode
	mode = 'askingQuestion'

	questionCounter += 1

	if questionCounter == 1:
		print()


	questionNumberText = Label(frame, text="Question %s:" %(questionCounter + 1), font="Calibri 12 bold", pady=20)
	questionNumberText.pack()

	questionText = Label(frame, text="%s" %((QsAndAs[questionCounter])[0]), font="Calibri 12 bold", pady=40, padx=20)
	questionText.pack()

	#the following checks if the answer contains more than 8 words to determine what the program will do with the user input answer.
	splitWordList = ((QsAndAs[questionCounter])[1]).split()

	txtDisplay = Entry(frame, textvariable = frame, bd=20, insertwidth=1, font=30)

	if len(splitWordList) > 8:
		txtDisplay.bind('<Return>', lambda event: selfCheckAnswer(frame, questionCounter, QsAndAs, txtDisplay.get(), sessionAnswerInfo))
	else:
		txtDisplay.bind('<Return>', lambda event: checkAnswer(frame, questionCounter, QsAndAs, txtDisplay.get(), sessionAnswerInfo))
	txtDisplay.bind('<Escape>', lambda event: openMainMenu(frame))
	txtDisplay.pack()
	txtDisplay.focus()
	txtDisplay.delete(0, END)

	if len(splitWordList) > 8:
		print('------------ word count over 8!')
		answerButton = Button(frame, padx=32, pady=16, bd=4, text="Answer", fg="black", font='Calibri 12 bold', command= lambda: selfCheckAnswer(frame, questionCounter, QsAndAs, txtDisplay.get(), sessionAnswerInfo))
		answerButton.pack()
	else:
		#CHANGE THE FOLLOWING FUNCTION TO THE NEW MADE ONE
		checkButton = Button(frame, padx=32, pady=16, bd=4, text="Check answer", fg="black", font='Calibri 12 bold', command= lambda: checkAnswer(frame, questionCounter, QsAndAs, txtDisplay.get(), sessionAnswerInfo))
		checkButton.pack()

	mainMenuButton = Button(frame, padx=32, pady=16, bd=4, text="Main Menu", fg="black", font='Calibri 12 bold', command= lambda: listCompleteScreen(frame, questionCounter, QsAndAs, sessionAnswerInfo))
	mainMenuButton.pack()

#def checkAnswer(frame, questionCounter, QsAndAs, userAnswer):
	


























def selfCheckAnswer(frame, questionCounter, QsAndAs, userAnswer, sessionAnswerInfo):
	deleteFrame(frame)
	frame = Frame(root)
	frame.pack()






	answerText = Label(frame, text="The correct answer is: %s" % (QsAndAs[questionCounter])[1], font="Calibri 12", pady=20, padx=20)
	answerText.pack()

	yourAnswerText = Label(frame, text="Your answer was: %s" % userAnswer, font="Calibri 12", pady=20, padx=20)
	yourAnswerText.pack()



	selfCheckText = Label(frame, text="Did you think you answered to a satisfactory standard?", font="Calibri 12 bold", pady=20, padx=20)
	selfCheckText.pack()

	noButton = Button(frame, padx=32, pady=16, bd=4, text="No", fg="black", font='Calibri 12 bold', command= lambda: checkAnswer(frame, questionCounter, QsAndAs, '***Wrong answer***', sessionAnswerInfo))
	noButton.bind('<Return>', lambda event: checkAnswer(frame, questionCounter, QsAndAs, '***Wrong answer***', sessionAnswerInfo))
	noButton.pack()
	noButton.focus()

	yesButton = Button(frame, padx=32, pady=16, bd=4, text="Yes", fg="black", font='Calibri 12 bold', command= lambda: checkAnswer(frame, questionCounter, QsAndAs, yourAnswerText, sessionAnswerInfo))
	yesButton.bind('<Return>', lambda event: checkAnswer(frame, questionCounter, QsAndAs, yourAnswerText, sessionAnswerInfo))
	yesButton.pack()

	mainMenuButton = Button(frame, padx=32, pady=16, bd=4, text="Main Menu", fg="black", font='Calibri 12 bold', command= lambda: listCompleteScreen(frame, questionCounter, QsAndAs, sessionAnswerInfo))
	mainMenuButton.bind('<Escape>', lambda event: openMainMenu(frame))
	mainMenuButton.pack()



#	root.bind('<Right>', lambda event: tk_focusPrev(event))
#	root.bind('<Left>', lambda event: focus_next_window(event))

#def focus_next_window(event):
#	event.widget.tk_focusNext().focus()
#	print('---------------------STUFF WORKED SUCCESSFULLY')
#focus_get() 
#takeFocus()


#clears the frame and shows the answer for the question previously asked.
def checkAnswer(frame, questionCounter, QsAndAs, userAnswer, sessionAnswerInfo):
	deleteFrame(frame)
	frame = Frame(root)
	frame.pack()

	global mode
	mode = 'checking answer'

	print('QsAndAs is:', QsAndAs)

	print('THE GIVEN USERANSWER IS:', userAnswer, 'THE ANSWER IS:', (QsAndAs[questionCounter])[1])


	

	if userAnswer == (QsAndAs[questionCounter])[1]:
		print('------Answer correct ---------')
		QsAndAs[questionCounter].append('correct')
		questionNumberText = Label(frame, text="You've answered correctly!", font="Calibri 12 bold", pady=20, padx=20)
		questionNumberText.pack()
		sessionAnswerInfo[0] += 1

	else:
		print('------Answer incorrect ---------')
		QsAndAs[questionCounter].append('incorrect')
		questionNumberText = Label(frame, text="You've answered incorrectly. The correct answer was:", font="Calibri 12 bold", pady=20, padx=20)
		questionNumberText.pack()
		questionNumberText = Label(frame, text="%s" %(QsAndAs[questionCounter])[1], font="Calibri 12 bold", pady=20, padx=20)
		questionNumberText.pack()
		sessionAnswerInfo[1] += 1



	answerHistory = QsAndAs[2:]
	print('-----------answerHistory is:', answerHistory)

	popCounter = -1
	for i in answerHistory:
		popCounter += 1
		if i != 'Correct' or i != 'Incorrect':
			answerHistory.pop(popCounter)

			popCounter -= 1

	print('after popping, answerHistory is:', answerHistory)

	lastFiveAnswersHistory = '***No value***'
	numberTestingCounter = -5
	while lastFiveAnswersHistory != '***No value***':	
		try:
			lastFiveAnswersHistory = (answerHistory[questionCounter])[numberTestingCounter:]
			print('lastFiveAnswersHistory success! : ', lastFiveAnswersHistory)
		except:
			numberTestingCounter += 1
			print('didn\'nt work bruh')

	timesAnsweredCorrectlyInLastFiveQuestions = lastFiveAnswersHistory.count('correct')
	print('timesAnsweredCorrectlyInLastFiveQuestions is:', timesAnsweredCorrectlyInLastFiveQuestions)

	timesAnsweredIncorrectlyInLastFiveQuestions = lastFiveAnswersHistory.count('incorrect')
	print('timesAnsweredIncorrectlyInLastFiveQuestions is:', timesAnsweredIncorrectlyInLastFiveQuestions)

	timesAnsweredCorrectly = answerHistory[questionCounter].count('correct')
	print('timesAnsweredCorrectly is:', timesAnsweredCorrectly)

	timesAnsweredIncorrectly = answerHistory[questionCounter].count('incorrect')
	print('timesAnsweredIncorrectly is:', timesAnsweredIncorrectly)

	questionNumberText = Label(frame, text="This question has been answered %s times correctly and %s times incorrectly." % (timesAnsweredCorrectly, timesAnsweredIncorrectly), font="Calibri 12 bold", pady=20, padx=20)
	questionNumberText.pack()


	#for i in range(5):
	try:
		percentageOfCorrectAnswers = ((100/(timesAnsweredCorrectlyInLastFiveQuestions + timesAnsweredIncorrectlyInLastFiveQuestions))*(timesAnsweredCorrectlyInLastFiveQuestions))
		print('timesAnsweredCorrectly is:', timesAnsweredCorrectly)
		print('timesAnsweredIncorrectly', timesAnsweredIncorrectly)
	except:
		print('percentage changed to zero')
		percentageOfCorrectAnswers = 0

	percentageText = Label(frame, text=("In the last 5 attempts in answering this question, it has been answered correctly %s" % (percentageOfCorrectAnswers) + "% of the time".format()), font="Calibri 12 bold", pady=20, padx=20)
	percentageText.pack()
	
	print('_______________------percentage of CorrectAnswers is:', percentageOfCorrectAnswers)


	print('after incorrect/correct answer, QsAndAs is:', QsAndAs) 

	answerButton = Button(frame, padx=32, pady=16, bd=4, text="Next", fg="black", font='Calibri 12 bold', command= lambda: nextQuestion(frame, questionCounter, QsAndAs, sessionAnswerInfo))
	answerButton.bind('<Return>', lambda event: nextQuestion(frame, questionCounter, QsAndAs, sessionAnswerInfo))
	answerButton.pack()
	answerButton.focus()

	mainMenuButton = Button(frame, padx=32, pady=16, bd=4, text="Main Menu", fg="black", font='Calibri 12 bold', command= lambda: listCompleteScreen(frame, questionCounter, QsAndAs, sessionAnswerInfo))
	mainMenuButton.bind('<Escape>', lambda event: openMainMenu(frame))
	mainMenuButton.pack()

#clears the frame and shows how many things the user has learnt, with a congratulations.
def listCompleteScreen(frame, questionCounter, QsAndAs, sessionAnswerInfo):
	deleteFrame(frame)
	frame = Frame(root)
	frame.pack()

	print('where it is needed, the FileName is:', fileName)

	with open(('D:\Documents\School Subjects\Misc\Python\learningSets2\\' + fileName), 'r+') as f:
		for i in QsAndAs:
			print('------------ line written to file is: %r' % i)
			f.truncate()
			f.write(json.dumps(i))
			f.write('\n')
	f.close()


	congratsText = Label(frame, text="Congratulations! You\'ve further memorised %s things!" %(questionCounter + 1), font="Calibri 12 bold", pady=40, padx=20)
	congratsText.pack()

	if sessionAnswerInfo[0] != 1 and sessionAnswerInfo[1] != 1:
		sessionAnswerInfoText = Label(frame, text="You've answered %s questions correctly and answered %s answers incorrectly." %(sessionAnswerInfo[0], sessionAnswerInfo[1]), font="Calibri 11 bold", pady=40, padx=20)
	elif sessionAnswerInfo[0] == 1 and sessionAnswerInfo[1] == 1:
		sessionAnswerInfoText = Label(frame, text="You've answered %s question correctly and answered %s answer incorrectly." %(sessionAnswerInfo[0], sessionAnswerInfo[1]), font="Calibri 11 bold", pady=40, padx=20)
	elif sessionAnswerInfo[0] == 1:
		sessionAnswerInfoText = Label(frame, text="You've answered %s question correctly and answered %s answers incorrectly." %(sessionAnswerInfo[0], sessionAnswerInfo[1]), font="Calibri 11 bold", pady=40, padx=20) 
	elif sessionAnswerInfo[1] == 1:
		sessionAnswerInfoText = Label(frame, text="You've answered %s questions correctly and answered %s answer incorrectly." %(sessionAnswerInfo[0], sessionAnswerInfo[1]), font="Calibri 11 bold", pady=40, padx=20)
	sessionAnswerInfoText.pack()

	


	backButton = Button(frame, padx=32, pady=16, bd=4, text="Back to main menu", fg="black", font='Calibri 12 bold', command= lambda: openMainMenu(frame))
	backButton.bind('<Return>', lambda event: openMainMenu(frame))
	backButton.pack()
	backButton.focus()

	QsAndAs = []

def newLearningList(frame):
	deleteFrame(frame)
	frame=Frame(root)
	frame.pack()

	createListButton =  Button(frame, width = 20, pady=10, bd=4, text="Create List", fg="black", font='Calibri 12 bold', command= lambda: instructionsPage(frame))
	createListButton.pack()

	preMadeListButton = Button(frame, width = 20, pady=10, bd=4, text="Premade List", fg="black", font='Calibri 12 bold', command= lambda: testingScreen(frame))
	preMadeListButton.pack()

	global isThisAQuestion
	isThisAQuestion = True



def instructionsPage(frame):
	deleteFrame(frame)
	frame=Frame(root)
	frame.pack()

	instructions = Message(frame, fg="black", text= "Instructions for making new Learning Sets:", font="Calibri 12 bold", pady = 40, width = 760)
	instructions.pack()

	#scrollBar = Scrollbar(frame)
	#scrollBar.pack(side=RIGHT, fill=Y)

	#instructions.config(yscrollcommand=scrollBar.set)
	#scrollBar.config(command=scrollBar.yview)

	instructions = Message(frame, fg="black", text= "Learning sets consist of groups of a question and answer. You will be prompted to provide a question and then the corresponding answer. Enter the required text in the box provided and click 'next' or press the ENTER button. After at least one question and answer has been provided, you will be able to complete the set by pressing the 'finish' and it will be saved", font="Calibri 12", width = 760)
	instructions.pack()

	instructions = Message(frame, fg="black", text= "You will be prompted to provide a question and then the corresponding answer. Enter the required text in the box provided and click 'next' or press the ENTER button. After at least one question and answer has been provided, you will be able to complete the set by pressing the 'finish' and it will be saved", font="Calibri 12", width = 760)
	instructions.pack()

	instructions = Message(frame, fg="black", text= "Note: questions with and answer of over 8 words will not ask you to type your answer.", font="Calibri 12", width = 760, pady = 5)
	instructions.pack()

	instructions = Message(frame, fg="black", text= "Please enter the name of the new learning list:", font="Calibri 12", width = 760, pady = 10)
	instructions.pack()


	txtDisplay = Entry(frame, textvariable = frame, bd=20, insertwidth=1, font=30)
	txtDisplay.bind('<Return>', lambda event: writeToFile(txtDisplay.get(), frame))
	txtDisplay.bind('<Escape>', lambda event: openMainMenu(frame))
	txtDisplay.pack()
	txtDisplay.focus()
	txtDisplay.delete(0, END)

	global isThisAQuestion
	isThisAQuestion = True

	OkButton = Button(frame, padx=32, pady=16, bd=4, text="OK", fg="black", 
	font='Calibri 12 bold', command= lambda: writeToFile(txtDisplay.get(), frame))
	OkButton.pack()

	mainMenuButton = Button(frame, padx=32, pady=16, bd=4, text="Main Menu", fg="black", font='Calibri 12 bold', command= lambda: listCompleteScreen(frame, questionCounter, QsAndAs, sessionAnswerInfo))
	mainMenuButton.bind('<Escape>', lambda event: openMainMenu(frame))
	mainMenuButton.pack()

	#this creates a list that will contain future questions and answers
	#global newFileText
	#newFileText = []

def askNewQuestion(frame, newFile, newFileText):
	deleteFrame(frame)
	frame=Frame(root)
	frame.pack()

	global namingQuestionCounter
	namingQuestionCounter += 1

	global passedInstructionsPage
	passedInstructionsPage = True

	#Asks for user input in the form of a question
	questionPrompt = Label(frame, fg="black", text= "What is question %s going to be?" % namingQuestionCounter, font="Calibri 12 bold", padx=200, pady=20)
	questionPrompt.pack()

	txtDisplay = Entry(frame, textvariable = frame, bd=20, insertwidth=1, font=30)
	txtDisplay.bind('<Return>', lambda event: appendQuestion(frame, newFile, newFileText, txtDisplay.get()))
	txtDisplay.bind('<Escape>', lambda event: openMainMenu(frame))
	txtDisplay.pack()
	txtDisplay.focus()
	txtDisplay.delete(0, END)

	#txtDisplay.focus()

	OkButton = Button(frame, padx=32, pady=16, bd=4, text="OK", fg="black", font='Calibri 12 bold', command= lambda: appendQuestion(frame, newFile, newFileText, txtDisplay.get()))
	OkButton.pack()

	mainMenuButton = Button(frame, padx=32, pady=16, bd=4, text="Exit", fg="black", font='Calibri 12 bold', command= lambda: openMainMenu(frame))
	mainMenuButton.bind('<Escape>', lambda event: openMainMenu(frame))
	mainMenuButton.pack()

	#scrollbar = Scrollbar(frame)
	#scrollbar.pack(side=RIGHT, fill=Y)
	#scrollbar.config(command=listbox.yview)

def askNewAnswer(frame, newFile, newFileText):
	deleteFrame(frame)
	frame=Frame(root)
	frame.pack()

	#Asks for user input in the form of a question
	answerPrompt = Label(frame, fg="black", text= "What is answer for question %s going to be?" % namingQuestionCounter, font="Calibri 12 bold", padx=200, pady=20)
	answerPrompt.pack()

	txtDisplay = Entry(frame, textvariable = frame, bd=20, insertwidth=1, font=30)
	txtDisplay.bind('<Return>', lambda event: appendAnswer(frame, newFile, newFileText, txtDisplay.get(), False))
	txtDisplay.bind('<Escape>', lambda event: openMainMenu(frame))
	txtDisplay.pack()
	txtDisplay.focus()
	txtDisplay.delete(0, END)

	#txtDisplay.focus()

	additionalQuestionButton = Button(frame, padx=32, pady=16, bd=4, text="Add another question", fg="black", font='Calibri 12 bold', command= lambda: appendAnswer(frame, newFile, newFileText, txtDisplay.get(), False))
	additionalQuestionButton.pack()

	finishButton = Button(frame, padx=32, pady=16, bd=4, text="Finish", fg="black", font='Calibri 12 bold', command= lambda: appendAnswer(frame, newFile, newFileText, txtDisplay.get(), True))
	finishButton.pack()

def writeToFile(enteredText, frame):
	print('the current namingQuestionCounter is:', namingQuestionCounter)

	completeName = os.path.join('D:\Documents\School Subjects\Misc\Python\learningSets2\\', enteredText + ".txt")
	global newFile
	newFile = open(completeName, 'a')
	#newFile.close()

	deleteFrame(frame)
	frame= Frame(root)
	frame.pack()

	newFileText = []

	askNewQuestion(frame, newFile, newFileText)

def appendQuestion(frame, newFile, newFileText, enteredText):
	print('newFileText is:', newFileText)
	print('entered text is:', enteredText)


	#stringToAppend = enteredText.replace("'", '"')
	#print('---------stringToAppend is now:', stringToAppend)
	stringToAppend = str("enteredText")


	newFileText.append([enteredText])
	print('the new newFileText is:', newFileText, enteredText)
	runFunction = askNewAnswer(frame, newFile, newFileText)

	#try:
	#	
def appendAnswer(frame, newFile, newFileText, enteredText, finishedOrNot):
	print('newFileText is:', newFileText)
	print('entered text is:', enteredText)

	#textToAppend = ["%s" % enteredText]
	#print ('---------text to append:', textToAppend)

	newFileText[((len(newFileText))-1)].append(enteredText)
	print('the new newFileText is:', newFileText)

	if finishedOrNot == True:
		runFunction = saveNewFile(frame, newFile, newFileText)
	else:
		askNewQuestion(frame, newFile, newFileText)

def saveNewFile(frame, newFile, newFileText):

	for i in newFileText:
		print('------------ i is: %r' % i)
		newFile.write(json.dumps(i))
		newFile.write('\n')
	newFile.close()

	openMainMenu(frame)


	













#def keyPress(event):
#	if event.keysym in ('Return'):
#		print('Return encountered')
#		#now retrieve the current text in the box and save it to the file. Then ask for the corresponding answer.
#		#currentText = txtDisplay.get()
#		#print('namingQuestionCounter is currently', namingQuestionCounter, 'when return was pressed')
#		print('the global mode is:', mode)


		# *** This now attempts to do the enter() function ***
#		print(enter())



		#parent_name = widget.winfo_parent()
		#parent = widget._nametowidget(parent_name)


#----------- The following commented out text is used for allowing the return button to be used for text boxes. Is currently not completed. -------------------
#		if passedInstructionsPage == True:
#			if isThisAQuestion == True:
#				frame.destroy()
#				print('widgets destroyed')
#				frame=Frame(root)
#				frame.pack()
#
#				potato = askNewQuestion(frame)
#
#			else:
#				potato = askNewAnswer(frame)
#
#			#potato = writeToFile(txtDisplay.get(), frame)
#		
#		
#
#
#	elif event.keysym not in ('Alt_r', 'Alt_L', 'F4', 'Left', 'Right','Delete', 'BackSpace', 'Return'):
#		print('elif used. key pressed:', event.keysym)

	#print('The current text should be:', txtDisplay.get())




















#
##Currenlty working  below on making the enter button start the 'asking' of the next question, and possibly include the number of question it is currently on. Get the typed question to be saved as a text file.
#

















#def inputNextQuestion(frame):
#	deleteFrame(frame)
#	frame=Frame(root)
#	frame.pack()
#
#	#Asks for user input in the form of a question
#	questionPrompt = Label(frame, fg="black", text= "What is your question going to be?", font="Calibri 12 bold", padx=200, pady=20)
#	questionPrompt.pack()
#
#	txtDisplay = Entry(frame, textvariable = frame, bd=20, insertwidth=1, font=30)
#	txtDisplay.bind('<Return>', lambda event: enter(event, txtDisplay.get()))
#	txtDisplay.pack()


	#txtDisplay.focus()

def testingScreen(frame):
	deleteFrame(frame)
	frame=Frame(root)
	frame.pack()

	backButton = Button(frame, padx=32, pady=16, bd=4, text="Back to main menu", fg="black", font='Calibri 12 bold', command= lambda: openMainMenu(frame))
	backButton.pack()

#resets the saved values for the questions and answers.
QsAndAs = []

#initiates the main menu to open upon opening the program.
openMainMenu(frame)

#part of the code needed to create the windows frame around the tkinter program.
root.mainloop()