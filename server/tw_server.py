#!/usr/bin/env python2

# Library imports.
import sys, os, ConfigParser, traceback

# Local imports.

# Global variables.
server_config = {}

if __name__ == '__main__':
    # Default to ./tw2200.ini unless we're given another config file to use.
    if len(sys.argv) < 2:
        config_file = os.path.join(os.getcwd(),"tw2200.ini")
    else:
        config_file = sys.argv[1]

    print "Initializing Trade Wars 2200 server with configuration file '"+config_file+"'..."

    try:
        # Load and parse config file.
        raw_config = ConfigParser.RawConfigParser(
            defaults = {
                "ServerName":"Sample TW2200 Server",
                "ServerPort":"22001",
                "ServerIP":"127.0.0.1",

                "ServerMaxListeners":"5",
                "ServerMaxPlayers":"20",
                "ServerReserveAdminSlots":"1",
                "ServerReserveBotSlots":"2",

                "ServerLogFile":"/var/log/tw2200.log",
                "ServerLogLevel":"5",

                "ServerBroadcast":"False"
            }
        )
        raw_config.read(config_file)

        # Convert to global dictionary for later use.
        for key in raw_config.options('Configuration'):

            # Handle integers.
            if ("port" in key) or ("max" in key) or ("level" in key) or ("slots" in key):
                server_config[key] = raw_config.getint('Configuration', key)

            # And booleans.
            elif ("broadcast" in key):
                server_config[key] = raw_config.getboolean('Configuration', key)

            # And fall back to strings.
            else:
                server_config[key] = raw_config.get('Configuration', key)

    except:
        print "FATAL: Error reading or parsing configuration file!"
        traceback.print_exc()
        sys.exit(2)

    print server_config

