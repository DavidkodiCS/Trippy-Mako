class TURN:
    def __init__(self, clientTransportIP, clientPort, serverTransportIP, serverPort, transportProtocol):
        self.clientTransportIP = clientTransportIP
        self.clientPort = clientPort
        self.serverTransportIP = serverTransportIP
        self.serverPort = serverPort
        self.transportProtocol = transportProtocol
        self.turnTuple = (self.clientTransportIP, self.clientPort, self.serverTransportIP, self.serverPort, self.transportProtocol)

    ## Description of function
    def sendAllocation(self):
        #send 5 tuple to TURN server
        return 0
    
    ##Description of function
    def sendRefresh(self):
        return 0