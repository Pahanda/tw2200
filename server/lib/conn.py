## Library for handling client connections.

from twisted.internet.protocol import Factory, ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor, task
from twisted.logger import LogLevelFilterPredicate, LogLevel, textFileLogObserver
from twisted.logger import FilteringLogObserver, Logger, globalLogBeginner
from twisted.python.log import addObserver

from os import linesep
import sys

class GameReceiver(LineReceiver):
    def __init__(self, factory):
        self.factory = factory
        self.name = 'GameReceiverProtocol'
        self.state = "ERROR"

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
        self.factory.log.debug('Console command received: ' + line)
        console_command = line.split()

        if console_command[0].lower() == 'help':
            self.console('TW2200 Console Help:')
            self.console('There is no help for you... yet.')
        elif console_command[0].lower() == 'shutdown':
            self.console('Sending termination signal for TW2200 Server by console request.')
            self.factory.log.info('Console requested server shutdown in 5 seconds.')
            self.factory.shutdown = reactor.callLater(5, self.factory.GameShutdown, 'console request')
    def console(self, message):
        self.transport.write(b'[CON] ' + message + '\n')


class GameFactory(Factory):
    def __init__(self, config):

        # Dictionary to hold active clients.
        self.clients = {}

        # Set up logging.
        # TODO: Use config parameters here.
        self.log = Logger()

        # Logging target.
        log_observer = textFileLogObserver(sys.stdout)
        # Filter out levels to the specified severity.
        logging_level_predicate = [LogLevelFilterPredicate(LogLevel.debug)]
        # Set up an Observer to actually perform the filtering.
        log_filter = FilteringLogObserver(textFileLogObserver(sys.stdout), predicates=logging_level_predicate)
        # And register global logging for the filtering observer.
        globalLogBeginner.beginLoggingTo([log_filter])
        # Passed-in game configuration.
        self.configuration = config

        # Init main game loop.
        self.game_loop = task.LoopingCall(self.GameLoop)
        self.game_loop.start(30)

        # Holds a (cancelable! - just "self.shutdown.cancel()") callback for shutting down the server as needed.
        self.shutdown = None

    def buildProtocol(self, addr):
        if addr.host == '127.0.0.1':
            self.log.info('Console connection established from ' + addr.host)
            return GameConsoleProtocol(self)
        else:
            self.log.info('Incoming client connection established from ' + addr.host)
            return GameClientProtocol(self)

    def GameShutdown(self, reason):
        print 'TW2200 Server shutting down. Reason: ' + reason
        self.log.info('Terminating server. Reason: ' + reason)
        reactor.stop()

    def GameLoop(self):
        print 'Tick!'
