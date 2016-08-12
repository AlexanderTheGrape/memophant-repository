#memophant v0.2.3

#imports the needed program extentions.
import math
import sys
import json
import random
import os.path
from tkinter import *


root = Tk()

#'Frame' creates a frame, in this case using the main directory 'root'. This process will be repeated for creating new 'screens' throughout the program.

root.title('Memophant v1')
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
global currentColour
currentColour='#F0F0F0'



#The following functions are used in various parts of the program. The use of functions reduces the amount of repeated code that needs to be used.

#deletes the frame, clears the tkinter window so that new content can replace it. Input: frame. Output: deletes the frame.
def deleteFrame(frame):
	frame.destroy()


#Loads a default user
global currentUsername
currentUsername = "User 1"

#The user class allows for the changing the colour of buttons throughout the program.
class userClass:
	#This function is used for determining what colour all buttons in the program should be. Input: current frame, colour name (used as 'username'). Output: creates a variable able to be referenced to create coloured buttons.
	def chooseUser(frame, username):
		global currentUsername
		currentUsername = username
		global currentColour
		colourList = ['#F0F0F0', 'light blue', 'light yellow']
		try:
			currentColour = (colourList)[(int(username[-1:]))-1]
		except:
			currentColour = 'light red'

		openMainMenu(frame)
	
	#this function is used for changing the colour of buttons within the program. Input: current frame, colour name (used as 'username'). Output: Updates the button colour variable.
	def changeColour(frame, username):
		global currentUsername
		currentUsername = username
		global currentColour
		colourList = ['#F0F0F0', 'light blue', 'light yellow']
		try:
			currentColour = (colourList)[(int(username[-1:]))-1]
		except:
			currentColour = 'light red'

	#This function is for creating the starting page that opens upon running the program, which is used for allowing the user to choose what colour the buttons should be. Input: current frame. Output: creates a screen with the necessary buttons and text.
	def logOnScreen(frame):
		deleteFrame(frame)
		frame= Frame(root)
		frame.pack()

		global currentColour

		img = PhotoImage(file = "memophant logo edited gif.gif")
		label = Label(frame, image=img)
		label.img = img # to keep the reference for the image.
		label.pack()

		mainMenuText = Label(frame, fg="black", text= "Choose colour scheme", font="Calibri 12 bold", padx=200, pady=20)
		mainMenuText.pack()


		user1Button = Button(frame, width = 20, height=3, bd=4, text="Default", fg="black", font='Calibri 12 bold', command= lambda: usableUserClass.chooseUser(frame, 'user 1'))
		user1Button.pack()
		user1Button.config(bg=currentColour)

		user2Button = Button(frame, width = 20, height=3, bd=4, text="Light blue", fg="black", font='Calibri 12 bold', command= lambda: usableUserClass.chooseUser(frame, 'user 2'))
		user2Button.pack()
		user2Button.config(bg='light blue')

		user3Button = Button(frame, width = 20, height=3, bd=4, text="Light yellow", fg="black", font='Calibri 12 bold', command= lambda: usableUserClass.chooseUser(frame, 'user 3'))
		user3Button.pack()
		user3Button.config(bg='light yellow')

usableUserClass = userClass




#creates the top menu
topMenu = Menu(root)
root.config(menu=topMenu)

fileSubMenu = Menu(topMenu)
topMenu.add_cascade(label="Colour schemes", menu=fileSubMenu)

fileSubMenu.add_command(label="Default", command=lambda: usableUserClass.changeColour(frame, "User 1"))
fileSubMenu.add_command(label="Light blue", command=lambda: usableUserClass.changeColour(frame, "User 2"))
fileSubMenu.add_command(label="Light yellow", command=lambda: usableUserClass.changeColour(frame, "User 3"))

fileSubMenu.add_separator()

#clears the frame and loads content for the main menu. Input: current frame. Output: creates a screen for the main menu.
def openMainMenu(frame):
	deleteFrame(frame)
	frame= Frame(root)
	frame.pack()

	global currentColour

	img = PhotoImage(file = "memophant logo edited gif.gif")
	label = Label(frame, image=img)
	label.img = img # to keep the reference for the image.
	label.pack()

	mainMenuText = Label(frame, fg="black", text= "Main Menu", font="Calibri 12 bold", padx=200, pady=20)
	mainMenuText.pack()


	learnButton = Button(frame, width = 20, height=3, bd=4, text="Learn", fg="black", font='Calibri 12 bold', command= lambda: openLearningListOptions(frame))
	learnButton.pack()
	learnButton.config(bg=currentColour)

	newLearningListButton = Button(frame, width = 20, height=3, bd=4, text="New Learning List", fg="black", font='Calibri 12 bold', command= lambda: newLearningList(frame))
	newLearningListButton.pack()
	newLearningListButton.config(bg=currentColour)





#clears the tkinter frame and loads buttons for each learning list that's been saved. Input: current frame. Output: Creates buttons for each of the different learning lists that the user can choose from.
def openLearningListOptions(frame):
	deleteFrame(frame)
	frame= Frame(root)
	frame.pack()

	from os import walk

	f = []
	for (dirpath, dirnames, filenames) in walk('D:\Documents\Memophant\learningSets'):
		f.extend(filenames)
		break

	fileNameList = []
	for i in range(len(f)):
		fileNameList.append(f[i])
	
	buttons = []
	iCounter = -1
	for i in fileNameList:
		listButton = Button(frame, width = 40, height = 3, bd=4, text="%s" %(i), fg="black", font='Calibri 12 bold', command= lambda i=i: openLearningListContent(frame, i))
		listButton.pack()
		listButton.config(bg=currentColour)
		buttons.append(listButton)



#opens the learning list selected and reads the file to derive the questions and answers needed to test the user. Input: current frame, current file name.
def openLearningListContent(frame, j):
	deleteFrame(frame)

	global fileName
	fileName = j

	QsAndAs = []

	paragraphCheck = 0
	debugCounter = 0
	with open('D:\Documents\Memophant\learningSets\\' + j) as f:
		for line in f:
			debugCounter += 1
			try:
				strippedLine = line.strip('\n')
				QsAndAs.append(json.loads(strippedLine))
			except:
				pass


	#now to randomise the questions
	random.shuffle(QsAndAs)

	questionCounter = -1
	sessionAnswerInfo = [0, 0]
	nextQuestion(frame, questionCounter, QsAndAs, sessionAnswerInfo)

#clears the frame and loads the next question to ask. If the user just clicked the button of the file they'd like to use, it'll show the first question. Input: current frame, question number, questions and answers for this file, number of questions answered correctly and answered incorrectly so far.	
def nextQuestion(frame, questionCounter, QsAndAs, sessionAnswerInfo):
	deleteFrame(frame)
	frame = Frame(root)
	frame.pack()

	if questionCounter + 1 == len(QsAndAs):
		listCompleteScreen(frame, questionCounter, QsAndAs, sessionAnswerInfo)
		return

	global mode
	mode = 'askingQuestion'

	questionCounter += 1

	questionNumberText = Label(frame, text="Question %s:" %(questionCounter + 1), font="Calibri 12 bold", pady=20)
	questionNumberText.pack()

	questionText = Message(frame, text="%s" %((QsAndAs[questionCounter])[0]), font="Calibri 12 bold", pady=40, width = 760)
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

	if len(splitWordList) > 5:
		answerButton = Button(frame, width = 20, height = 3, bd=4, text="Answer", fg="black", font='Calibri 12 bold', command= lambda: selfCheckAnswer(frame, questionCounter, QsAndAs, txtDisplay.get(), sessionAnswerInfo))
		answerButton.pack()
		answerButton.config(bg=currentColour)
	else:
		checkButton = Button(frame, width = 20, height = 3, bd=4, text="Check answer", fg="black", font='Calibri 12 bold', command= lambda: checkAnswer(frame, questionCounter, QsAndAs, txtDisplay.get(), sessionAnswerInfo))
		checkButton.pack()
		checkButton.config(bg=currentColour)

	mainMenuButton = Button(frame, width = 20, height = 3, bd=4, text="Main Menu", fg="black", font='Calibri 12 bold', command= lambda: listCompleteScreen(frame, questionCounter, QsAndAs, sessionAnswerInfo))
	mainMenuButton.pack()
	mainMenuButton.config(bg=currentColour)


#This function is used for allowing the user to check if their answer is correct. This feature is used if the answer is longer than 6 words long. Input: current frame, question number, questions and answers for this file, the user's answer, number of questions answered correctly and answered incorrectly so far.
def selfCheckAnswer(frame, questionCounter, QsAndAs, userAnswer, sessionAnswerInfo):
	deleteFrame(frame)
	frame = Frame(root)
	frame.pack()

	answerText = Message(frame, text="The correct answer is: %s" % (QsAndAs[questionCounter])[1], font="Calibri 12", pady=20, width = 760)
	answerText.pack()

	yourAnswerText = Message(frame, text="Your answer was: %s" % userAnswer, font="Calibri 12", pady=20, width = 760)
	yourAnswerText.pack()



	selfCheckText = Label(frame, text="Did you think you answered to a satisfactory standard?", font="Calibri 12 bold", pady=20, padx=20)
	selfCheckText.pack()

	noButton = Button(frame, width = 20, height = 3, bd=4, text="No", fg="black", font='Calibri 12 bold', command= lambda: checkAnswer(frame, questionCounter, QsAndAs, '***Wrong answer***', sessionAnswerInfo))
	noButton.bind('<Return>', lambda event: checkAnswer(frame, questionCounter, QsAndAs, '***Wrong answer***', sessionAnswerInfo))
	noButton.pack()
	noButton.focus()
	noButton.config(bg=currentColour)

	yesButton = Button(frame, width = 20, height = 3, bd=4, text="Yes", fg="black", font='Calibri 12 bold', command= lambda: checkAnswer(frame, questionCounter, QsAndAs, yourAnswerText, sessionAnswerInfo))
	yesButton.bind('<Return>', lambda event: checkAnswer(frame, questionCounter, QsAndAs, yourAnswerText, sessionAnswerInfo))
	yesButton.pack()
	yesButton.config(bg=currentColour)

	mainMenuButton = Button(frame, width = 20, height = 3, bd=4, text="Main Menu", fg="black", font='Calibri 12 bold', command= lambda: listCompleteScreen(frame, questionCounter, QsAndAs, sessionAnswerInfo))
	mainMenuButton.bind('<Escape>', lambda event: openMainMenu(frame))
	mainMenuButton.pack()
	mainMenuButton.config(bg=currentColour)

#clears the frame and shows the answer for the question previously asked. Input: current frame, question number, questions and answers for this file, the user's answer, number of questions answered correctly and answered incorrectly so far.
def checkAnswer(frame, questionCounter, QsAndAs, userAnswer, sessionAnswerInfo):
	deleteFrame(frame)
	frame = Frame(root)
	frame.pack()

	global mode
	mode = 'checking answer'

	if userAnswer == (QsAndAs[questionCounter])[1]:
		QsAndAs[questionCounter].append('correct')
		questionNumberText = Message(frame, text="You've answered correctly!", font="Calibri 12 bold", pady=20, width = 760)
		questionNumberText.pack()
		sessionAnswerInfo[0] += 1

	else:
		QsAndAs[questionCounter].append('incorrect')
		questionNumberText = Message(frame, text="You've answered incorrectly. The correct answer was:", font="Calibri 12 bold", pady=20, width = 760)
		questionNumberText.pack()
		questionNumberText = Message(frame, text="%s" %(QsAndAs[questionCounter])[1], font="Calibri 12 bold", pady=20, width = 760)
		questionNumberText.pack()
		sessionAnswerInfo[1] += 1


	currentAnswerHistory = (QsAndAs[questionCounter])[2:]

	#determining the last 5 values (consisting of 'correct' or 'incorrect')
	try:
		lastFiveValues = currentAnswerHistory[-5:]
	except:
		try:
			lastFiveValues = currentAnswerHistory[-4:]
		except:
			try:
				lastFiveValues = currentAnswerHistory[-3:]
			except:
				try:
					lastFiveValues = currentAnswerHistory[-2:]
				except:
					try:
						lastFiveValues = currentAnswerHistory[-1:]
					except:
						lastFiveValues = []

	a = int(lastFiveValues.count('correct'))
	b = int(lastFiveValues.count('incorrect'))

	answerCount = a + b


	percentageOfCorrectAnswers = ((100/(a + b))*(a))

	if percentageOfCorrectAnswers - math.floor(percentageOfCorrectAnswers) < 0.5:
		percentageOfCorrectAnswers = int(math.floor(percentageOfCorrectAnswers))
	else:
		percentageOfCorrectAnswers = int(math.ceil(percentageOfCorrectAnswers))


	if answerCount > 0:
		percentageText = Message(frame, text=("In the last 5 attempts in answering this question, it has been answered correctly %s" % (percentageOfCorrectAnswers) + "% of the time.".format()), font="Calibri 12 bold", pady = 20, width = 760)
		percentageText.pack()

	timesAnsweredCorrectly = QsAndAs[questionCounter].count('correct')


	timesAnsweredIncorrectly = QsAndAs[questionCounter].count('incorrect')

	questionNumberText = Message(frame, text="This question has been answered %s times correctly and %s times incorrectly." % (timesAnsweredCorrectly, timesAnsweredIncorrectly), font="Calibri 12 bold", pady=20, width = 760)
	questionNumberText.pack()

	answerButton = Button(frame, width = 20, height = 3, bd=4, text="Next", fg="black", font='Calibri 12 bold', command= lambda: nextQuestion(frame, questionCounter, QsAndAs, sessionAnswerInfo))
	answerButton.bind('<Return>', lambda event: nextQuestion(frame, questionCounter, QsAndAs, sessionAnswerInfo))
	answerButton.pack()
	answerButton.focus()
	answerButton.config(bg=currentColour)


	mainMenuButton = Button(frame, width = 20, height = 3, bd=4, text="Main Menu", fg="black", font='Calibri 12 bold', command= lambda: listCompleteScreen(frame, questionCounter, QsAndAs, sessionAnswerInfo))
	mainMenuButton.bind('<Escape>', lambda event: openMainMenu(frame))
	mainMenuButton.pack()
	mainMenuButton.config(bg=currentColour)

#clears the frame and shows how many things the user has learnt, with a congratulations. Input: current frame, question number, questions and answers for this file, number of questions answered correctly and answered incorrectly so far.
def listCompleteScreen(frame, questionCounter, QsAndAs, sessionAnswerInfo):
	deleteFrame(frame)
	frame = Frame(root)
	frame.pack()


	with open(('D:\Documents\Memophant\learningSets\\' + fileName), 'r+') as f:
		for i in QsAndAs:
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

	


	backButton = Button(frame, width = 40, height = 3, bd=4, text="Back to main menu", fg="black", font='Calibri 12 bold', command= lambda: openMainMenu(frame))
	backButton.bind('<Return>', lambda event: openMainMenu(frame))
	backButton.pack()
	backButton.focus()
	backButton.config(bg=currentColour)

	QsAndAs = []

#Creates a button to direct to making a new learning list. Input: current frame.
def newLearningList(frame):
	deleteFrame(frame)
	frame=Frame(root)
	frame.pack()

	createListButton =  Button(frame, width = 20, height = 3, bd=4, text="Create List", fg="black", font='Calibri 12 bold', command= lambda: instructionsPage(frame))
	createListButton.pack()
	createListButton.config(bg=currentColour)

	global isThisAQuestion
	isThisAQuestion = True


#Opens the instructions page for how to create a learning list, and prompts the user to write a name for creating a new file. Input: current frame.
def instructionsPage(frame):
	deleteFrame(frame)
	frame=Frame(root)
	frame.pack()

	instructions = Message(frame, fg="black", text= "Instructions for making new Learning Sets:", font="Calibri 12 bold", pady = 40, width = 760)
	instructions.pack()

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

	OkButton = Button(frame, width = 20, height = 3, bd=4, text="OK", fg="black", font='Calibri 12 bold', command= lambda: writeToFile(txtDisplay.get(), frame))
	OkButton.pack()
	OkButton.config(bg=currentColour)

	questionCounter = 0

	mainMenuButton = Button(frame, width = 20, height = 3, bd=4, text="Main Menu", fg="black", font='Calibri 12 bold', command= lambda: openMainMenu(frame))
	mainMenuButton.bind('<Escape>', lambda event: openMainMenu(frame))
	mainMenuButton.pack()
	mainMenuButton.config(bg=currentColour)

#Asks the next learning list question and prompts the user to answer it. Input: Current frame, name of newly made file, questions and answers to be written to this file.
def askNewQuestion(frame, newFile, newFileText):
	deleteFrame(frame)
	frame=Frame(root)
	frame.pack()

	global namingQuestionCounter
	namingQuestionCounter += 1

	global passedInstructionsPage
	passedInstructionsPage = True

	#Asks for user input in the form of a question
	questionPrompt = Message(frame, fg="black", text= "What is question %s going to be?" % namingQuestionCounter, font="Calibri 12 bold", width = 760, pady=20)
	questionPrompt.pack()

	txtDisplay = Entry(frame, textvariable = frame, bd=20, insertwidth=1, font=30)
	txtDisplay.bind('<Return>', lambda event: appendQuestion(frame, newFile, newFileText, txtDisplay.get()))
	txtDisplay.bind('<Escape>', lambda event: openMainMenu(frame))
	txtDisplay.pack()
	txtDisplay.focus()
	txtDisplay.delete(0, END)

	OkButton = Button(frame, width = 20, height = 3, bd=4, text="OK", fg="black", font='Calibri 12 bold', command= lambda: appendQuestion(frame, newFile, newFileText, txtDisplay.get()))
	OkButton.pack()
	OkButton.config(bg=currentColour)

	mainMenuButton = Button(frame, width = 20, height = 3, bd=4, text="Exit", fg="black", font='Calibri 12 bold', command= lambda: openMainMenu(frame))
	mainMenuButton.bind('<Escape>', lambda event: openMainMenu(frame))
	mainMenuButton.pack()
	mainMenuButton.config(bg=currentColour)

#Displays the corresponding answer for the last answered question. Input: Current frame, name of newly made file, questions and answers to be written to this file.
def askNewAnswer(frame, newFile, newFileText):
	deleteFrame(frame)
	frame=Frame(root)
	frame.pack()

	#Asks for user input in the form of a question
	answerPrompt = Message(frame, fg="black", text= "What is answer for question %s going to be?" % namingQuestionCounter, font="Calibri 12 bold", width = 760, pady=20)
	answerPrompt.pack()

	txtDisplay = Entry(frame, textvariable = frame, bd=20, insertwidth=1, font=30)
	txtDisplay.bind('<Return>', lambda event: appendAnswer(frame, newFile, newFileText, txtDisplay.get(), False))
	txtDisplay.bind('<Escape>', lambda event: openMainMenu(frame))
	txtDisplay.pack()
	txtDisplay.focus()
	txtDisplay.delete(0, END)

	additionalQuestionButton = Button(frame, width = 30, height = 3, bd=4, text="Add another question", fg="black", font='Calibri 12 bold', command= lambda: appendAnswer(frame, newFile, newFileText, txtDisplay.get(), False))
	additionalQuestionButton.pack()
	additionalQuestionButton.config(bg=currentColour)

	finishButton = Button(frame, width = 30, height = 3, bd=4, text="Finish", fg="black", font='Calibri 12 bold', command= lambda: appendAnswer(frame, newFile, newFileText, txtDisplay.get(), True))
	finishButton.pack()
	finishButton.config(bg=currentColour)

#The function used to create a new learning list file. Input: typed text, current frame.
def writeToFile(enteredText, frame):

	completeName = os.path.join('D:\Documents\Memophant\learningSets', enteredText + ".txt")
	global newFile
	newFile = open(completeName, 'a')

	deleteFrame(frame)
	frame= Frame(root)
	frame.pack()

	newFileText = []

	askNewQuestion(frame, newFile, newFileText)

#Adds a new question to the learning list being made. Input: Current frame, name of newly made file, questions and answers to be written to this file, typed text.
def appendQuestion(frame, newFile, newFileText, enteredText):

	stringToAppend = str("enteredText")


	newFileText.append([enteredText])
	runFunction = askNewAnswer(frame, newFile, newFileText)

#Adds a new answer to the learning list being made. Input: Current frame, name of newly made file, questions and answers to be written to this file, typed input, boolean variable.
def appendAnswer(frame, newFile, newFileText, enteredText, finishedOrNot):

	newFileText[((len(newFileText))-1)].append(enteredText)

	if finishedOrNot == True:
		runFunction = saveNewFile(frame, newFile, newFileText)
	else:
		askNewQuestion(frame, newFile, newFileText)

#Saves the new learning list file. Input: Current frame, name of newly made file, questions and answers to be written to this file.
def saveNewFile(frame, newFile, newFileText):

	for i in newFileText:
		newFile.write(json.dumps(i))
		newFile.write('\n')
	newFile.close()

	openMainMenu(frame)



#resets the saved values for the questions and answers.
QsAndAs = []

#initiates the main menu to open upon opening the program.
usableUserClass.logOnScreen(frame)

#part of the code needed to create the windows frame around the tkinter program.
root.mainloop()