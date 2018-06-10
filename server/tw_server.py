#!/usr/bin/env python2

# Library imports.
import sys, os
from twisted.internet import reactor, task, stdio

# Local imports.
from lib import *

# Global variables.
server_config = {}
game_data = {}

# Program entry point.
if __name__ == '__main__':
    # Default to ./tw2200.ini unless we're given another config file to use.
    if len(sys.argv) < 2:
        config_file = os.path.join(os.getcwd(),"tw2200.ini")
    else:
        config_file = sys.argv[1]

    print "Initializing Trade Wars 2200 server with configuration file '"+config_file+"'..."

    server_config = config.parseConfig(config_file)

    # Set up the reactor to listen on the specified port.
    reactor.listenTCP(22001, conn.GameFactory(server_config))

    # And go!
    reactor.run()
