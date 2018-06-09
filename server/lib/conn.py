## Library for handling client connections.

from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver

class GameProtocol(LineReceiver):
    def __init__(self, factory):
        self.factory = factory
        self.name = None
        self.state = "CONNECT"

    def connectionMade(self):
        # Put initial handshaking/security checks here.
        return

    def connectionLost(self, reason):
        # Handle client disconnects here.
        return

    def lineReceived(self, line):
        # Do different things depending on what the client's state is.
        return

    def broadcastAction(self, action):
        # Broadcast various Actions to connected clients.
        for name, protocol in self.factory.clients.iteritems():
            pass

        return

class GameFactory(Factory):
    def __init__(self):
        # Dictionary to hold active clients. (e.g. clients['username'])
        self.clients = {}

    def buildProtocol(self, addr):
        return GameProtocol(self)
