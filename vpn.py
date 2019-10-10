from tkinter import Tk, Frame, Button, Label, Entry, Checkbutton, IntVar, END, StringVar
import server
import client

# def callback():
#     print("clicked")


def switchMode():
    #TODO: implement ui switching
    global inClientMode
    if 'client' in modeLabel["text"]:
        modeLabel.config(text = "VPN in server mode")
        hostDetails.config(state='disabled')
        nameOrIP.config(state='disabled')
        inClientMode = False
    else:
        modeLabel.config(text = "VPN in client mode")
        hostDetails.config(state='active')
        nameOrIP.config(state='active')
        inClientMode= True
    print('switching', inClientMode)

def submitSecret():
    if inClientMode:
        client.setSecret(ss_field.get())
    else: 
        server.setSecret(ss_field.get())
    print(ss_field.get())

def connectSubmit():
    #TODO:

    print(inClientMode)
    if inClientMode:
        client.clientSend(hostField.get(), nameIPState.get(), portField.get())
    else:
        server.openServer(portField.get())

    print(hostField.get(), nameIPState.get(), portField.get())

def sendData():
    #TODO:
    print(sendField.get())

def nextStep():
    #TODO:
    updateProgramState('stepping')

def executeFull():
    #TODO:
    updateProgramState('running')

def showRecData():
    #TODO:
    recText.set("test")
    print('added stuff')

def updateProgramState(status):
    #TODO:
    statusText.set('some update ' + status)

# initialize GUI area
root = Tk()
root.title('Team AMAZ VPN')
frame = Frame(root, width=500)
frame.pack()
inClientMode = True

# create Toggle button
labelText="VPN in client mode"
toggleText="Toggle mode"
modeLabel = Label(root, text=labelText)
toggle_button = Button(root, text=toggleText, command=switchMode)

modeLabel.pack()
toggle_button.pack()

# connection details
connectInfo = Label(root, text='Enter host name/IP (client only) and port number')
hostDetails = Label(root, text='Host Name/IP')
hostField = Entry(root)
nameIPState = IntVar()
nameOrIP = Checkbutton(root, text='Check if submitting IP address', variable=nameIPState)
portLabel = Label(root, text='Enter port number:')
portField = Entry(root)

connectInfo.pack()
hostDetails.pack()
hostField.pack()
nameOrIP.pack()
portLabel.pack()
portField.pack()

# shared secret field
ss_label = Label(root, text="Shared Secret Values: ")
ss_field = Entry(root)

ss_label.pack()
ss_field.pack()

# submit connection details
connectSubmit = Button(root, text='Submit Connection Details', command=connectSubmit)
connectSubmit.pack()

# data to send
sendLabel = Label(root, text="Data to send: ")
sendField = Entry(root)

sendLabel.pack()
sendField.pack()

# received data
recLabel = Label(root, text="Received data: ")
recText = StringVar()
recData = Entry(root, textvariable=recText)

recLabel.pack()
recData.pack()

# Continue button
continueButton = Button(root, text='Continue (step through)', command=nextStep)
continueButton.pack()

# Automatic Run
runButton = Button(root, text='Run automatically', command=executeFull)
runButton.pack()

# program status
statusText = StringVar()
statusText.set('program state')
status = Label(root, textvariable=statusText)
status.pack()

showRecData()
root.mainloop()
