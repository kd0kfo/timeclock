def get_timestamp():
    import time
    return int(time.time())


def load_name_map(map_file_path):
    from os.path import isfile
    import ConfigParser

    config = ConfigParser.RawConfigParser()
    config.read(map_file_path)

    if not config.has_section("effort"):
        raise Exception("Missing effort in {}".format(map_file_path))

    retval = {}
    for options in config.items("effort"):
        retval[options[0]] = options[1]

    return retval
