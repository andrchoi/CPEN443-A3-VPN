import vpn

def showRecData(data):
    #TODO:
    vpn.recText.set(data)
    print('added stuff')

def updateProgramState(status):
    #TODO:
    vpn.statusText.set('some update ' + status)