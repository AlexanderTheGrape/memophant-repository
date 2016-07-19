#memophant v0.1

import math
import sys
from tkinter import *

root = Tk()

#'Frame' creates a frame, in this case using the main directory 'root'.
frame= Frame(root)
frame.pack(side=TOP)

frame2 = Frame(root)
frame2.pack(side=BOTTOM)

root.title('Memophant v0.1')

LearningSet1=StringVar()

def openLearningLists():
	print('opening learning lists.')
	mainMenuText.pack_forget()

def deleteFrame(frame):
	frame.destroy()

def openMainMenu():
	mainMenuText = Label(frame, fg="black", text= "Main Menu", font="Calibri 12 bold", padx=200, pady=20)
	mainMenuText.pack(side=TOP)

	learnButton = Button(frame, padx=32, pady=16, bd=8, text="Learn", fg="black", font='Calibri 12 bold', command=openLearningLists)
	learnButton.pack(side=TOP)

	b = Button(frame, text="Click me", command= lambda: deleteFrame(frame))
	b.pack()



	d = Button(frame2, text="Click me 2", command= lambda: deleteFrame(frame2))
	d.pack()



openMainMenu()
root.mainloop()