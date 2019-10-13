from tkinter import Tk, Frame, Button, Label, Entry, Checkbutton, IntVar, END, StringVar
import server
import client

def switchMode():
    global inClientMode
    if 'client' in modeLabel["text"]:
        modeLabel.config(text = "VPN in server mode")
        hostDetails.config(state='disabled')
        hostField.config(state='disabled')
        nameOrIP.config(state='disabled')
        inClientMode = False
    else:
        modeLabel.config(text = "VPN in client mode")
        hostDetails.config(state='active')
        hostField.config(state='active')
        nameOrIP.config(state='active')
        inClientMode= True
    print('switching', inClientMode)

def connectStep():
    connect(True)

def connectSubmit():
    connect(False)

def connect(willStep):
    if inClientMode:
        client.getUIFields(recText, statusText, root)
        client.connectClient(int(ss_field.get()), hostField.get(), nameIPState.get(), int(portField.get()), willStep)
    else: 
        server.getUIFields(recText, statusText, root)
        server.openServer(int(ss_field.get()), int(portField.get()), willStep)

def sendData():
    if inClientMode:
        client.encryptAndSend(sendField.get())
    else:
        server.encryptAndSend(sendField.get())

def closeConnection():
    if inClientMode:
        root.quit()
        client.closeConnection()
    else:
        root.quit()
        server.closeConnection()


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
connectStep = Button(root, text='Step Through Connection', command=connectStep)
connectButton = Button(root, text='Submit Connection Details', command=connectSubmit)

connectStep.pack()
connectButton.pack()

# data to send
sendLabel = Label(root, text="Data to send: ")
sendField = Entry(root)

sendLabel.pack()
sendField.pack()

# received data
recLabel = Label(root, text="Received data: ")
recText = StringVar()
recData = Entry(root, textvariable=recText)
recLabel.config(state='disabled')

recLabel.pack()
recData.pack()

# Automatic Run
runButton = Button(root, text='Send Data', command=sendData)
runButton.pack()

# program status
statusText = StringVar()
statusText.set('program state')
status = Label(root, textvariable=statusText)
status.pack()

# disconnect
closeButton = Button(root, text='Close And Quit', command=closeConnection)
closeButton.pack()

root.mainloop()
