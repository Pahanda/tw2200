## Library for handling client connections.

from twisted.internet.protocol import Factory, ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor, task, defer

from os import linesep

class GameReceiver(LineReceiver):
    def __init__(self, factory):
        self.factory = factory
        self.name = 'GameReceiverProtocol'
        self.state = "ERROR"
        self.shutdown = None

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

class GameClientProtocol(GameReceiver):
    def __init__(self, factory):
        self.factory = factory
        self.name = 'GameClientProtocol'
        self.state = "CONNECT"

class GameConsoleProtocol(GameReceiver):
    delimiter = linesep.encode("ascii")

    def __init__(self, factory):
        self.factory = factory
        self.name = 'GameConsoleProtocol'
        self.state = "CONSOLE"

    def connectionMade(self):
        self.console('Console connected.  Type "help" for help.')

    def lineReceived(self, line):
        console_command = line.split()

        if console_command[0].lower() == 'help':
            self.console('TW2200 Console Help:')
            self.console('There is no help for you... yet.')
        elif console_command[0].lower() == 'shutdown':
            self.console('Sending termination signal for TW2200 Server by console request.')
            self.shutdown = reactor.callLater(5, self.factory.GameShutdown)
    def console(self, message):
        self.transport.write(b'[CON] ' + message + '\n')


class GameFactory(Factory):
    def __init__(self, config):

        # Dictionary to hold active clients.
        self.clients = {}

        # Passed-in game configuration.
        self.configuration = config

        # Init main game loop.
        self.game_loop = task.LoopingCall(self.GameLoop)
        self.game_loop.start(30)

    def buildProtocol(self, addr):
        if addr.host == '127.0.0.1':
            return GameConsoleProtocol(self)
        else:
            return GameClientProtocol(self)

    def GameShutdown(self):
        print 'TW2200 Server shutting down.'
        reactor.stop()

    def GameLoop(self):
        print 'Tick!'
