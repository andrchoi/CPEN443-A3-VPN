from tkinter import Tk, Frame, Button, Label, Entry, Checkbutton, IntVar

# def callback():
#     print("clicked")


def switchMode():
    #TODO: implement ui switching
    if 'client' in modeLabel["text"]:
        modeLabel.config(text = "VPN in server mode")
        inClientMode = False
    else:
        modeLabel.config(text = "VPN in client mode")
        inClientMode = True
    print('switching', inClientMode)

def submitSecret():
    #TODO:
    print(ss_field.get())

def connectSubmit():
    #TODO:
    print(hostField.get(), nameIPState.get(), portField.get())\

def sendData():
    #TODO:
    print(sendField.get())

def nextStep():
    #TODO:
    print('Stepping')

def execute():
    #TODO:
    print('running')

# initialize GUI area
root = Tk()
root.title('Team AMAZ VPN')
frame = Frame(root, width=500)
frame.pack()
inClientMode = True

# create Toggle button
labelText="VPN in client mode"
toggleText="Go to server mode"
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
portField = Entry(root)
connectSubmit = Button(root, text='Submit connection information', command=connectSubmit)

connectInfo.pack()
hostDetails.pack()
hostField.pack()
nameOrIP.pack()
portField.pack()
connectSubmit.pack()

# shared secret field
ss_label = Label(root, text="Shared Secret Value: ")
ss_field = Entry(root)
ss_submit = Button(root, text="Submit Value", command=submitSecret)

ss_label.pack()
ss_field.pack()
ss_submit.pack()

# data to send
sendLabel = Label(root, text="Data to send: ")
sendField = Entry(root)
sendSubmit = Button(root, text="Submit Value", command=sendData)

sendLabel.pack()
sendField.pack()
sendSubmit.pack()

# received data
recLabel = Label(root, text="Received data: ")
recData = Entry(root)

recLabel.pack()
recData.pack()

# Continue button
continueButton = Button(root, text='Step through program', command=nextStep)
continueButton.pack()

# Automatic Run
runButton = Button(root, text='Run program automatically', command=execute)
runButton.pack()
root.mainloop()