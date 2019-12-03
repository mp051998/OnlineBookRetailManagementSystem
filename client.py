import socket
from tkinter import *

BUFSIZE = 4096

master = Tk()
master.title("Online Book Rental Management System")

toSend = StringVar()
toServer = StringVar()

ClientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 33333
ClientSock.connect(('127.0.0.1', port))


def CheckCall():
	choice = toSend.get()
	ClientSock.send(choice.encode())
	CallServer()

def createQuery():
	global query
	query = Toplevel()
	query.title("Option "+ toSend.get())

def QuerySubmit():
	global ClientSock
	ClientSock.send((toServer.get()).encode())
	CallServer()

def CallServer():
	global master
	global ClientSock
	global toSend
	global toServer

	try:
		query.destroy()
	except:
		pass

	createQuery()

	toServer = StringVar()
	received = ClientSock.recv(BUFSIZE).decode()
	if received == '0':
		#End of Query
		ClientSock.send('OK'.encode())
		LastMessage = ClientSock.recv(BUFSIZE).decode()
		queryLabel = Label(query, text = LastMessage, width = 60, anchor = 'w', justify = "left").pack()
		buttonFinal = Button(query, text = 'OK', command = query.destroy)
		query.mainloop()
	
	elif toSend.get() in ['1','2','3','4','5','6']:
		queryLabel = Label(query, text = received, width = 60, anchor = 'w', justify = "left").pack()
		response = Entry(query, textvariable = toServer, width = 35).pack()
		buttonOption = Button(query, text = "Submit", command = QuerySubmit)
		buttonOption.pack()
		query.mainloop()
	else:
		queryLabel = Label(query, text = received, width = 60, anchor = 'w', justify = "left").pack()
		buttonOk = Button(query, text = "Ok", command = query.destroy)
		buttonOk.pack()
		query.mainloop()


MainBody = "Book Rental Management System\n\nMENU:\n1.  Inserting books\n2.  Removing books\n3.  Modify Inventory's BookCount\n4.  Add Rental\n5.  Add Customer\n6.  Accept Return\n7.  Display Book Table\n8.  Display Inventory Table\n9.  Display Customer Table\n10. Display Rental Table\n\n0.  -----SHUT DOWN SERVER-----\n"


MainMenu = Label(master, text = MainBody, width = 50, justify = 'left', anchor = 'w').pack(side = "left")
SelectionLabel = Label(master, text = 'Your Choice : ').pack()

choice = Entry(master, textvariable = toSend).pack()

buttonSelection = Button(master, text="Submit", command = CheckCall)
buttonSelection.pack()
master.mainloop()

ClientSock.close()




