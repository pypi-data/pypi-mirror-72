import re
import os
import yaml
import ujson as json
import logging
import logging.config

import coloredlogs

def findfile(pattern, *folders):
    regexp = re.compile(pattern)
    folders = ['.', *folders, os.path.dirname(__file__)]
    for top in folders:
        for root, _, files in os.walk(top):
            for name in files:
                if regexp.match(name):
                    filename = os.path.join(root, name)
                    return filename

def get_logconfig(config_file='logging.yaml', *folders):
    "Load the log config file"
    filename = findfile(config_file, *folders)

    ext = os.path.splitext(filename)[-1]
    loader = {'.yaml': yaml.load, '.json': json.load}

    with open(filename, 'r') as stream:
        log_config = loader[ext](stream)
    return log_config

def setup_config(config_file='logging.yaml', *folders):
    config = get_logconfig(config_file, *folders)
    logging.config.dictConfig(config)
    return config
