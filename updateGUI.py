import vpn

def showRecData():
    #TODO:
    vpn.recText.set("test")
    print('added stuff')

def updateProgramState(status):
    #TODO:
    vpn.statusText.set('some update ' + status)