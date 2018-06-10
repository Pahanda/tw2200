# System defaults.
default_config = {
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

def parseConfig(config_file):
    import sys, traceback, ConfigParser
    parsed_config = {}
    try:
        # Load and parse config file.
        raw_config = ConfigParser.RawConfigParser(defaults = default_config)
        raw_config.read(config_file)
        # Convert to global dictionary for later use.
        for key in raw_config.options('Configuration'):

            # Handle integers.
            if ("port" in key) or ("max" in key) or ("level" in key) or ("slots" in key):
                parsed_config[key] = raw_config.getint('Configuration', key)

            # And booleans.
            elif ("broadcast" in key):
                parsed_config[key] = raw_config.getboolean('Configuration', key)

            # And fall back to strings.
            else:
                parsed_config[key] = raw_config.get('Configuration', key)

    except:
        print "FATAL: Error reading or parsing configuration file!"
        traceback.print_exc()
        sys.exit(2)

    return parsed_config
