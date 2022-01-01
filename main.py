#!/usr/bin/env python3

import argparse
import logging
import sys

from core import add_scholar
from db.utils import create_db

_version = "0.0.0"


class Command:
    actions = ['help_action', 'init_db', 'add_scholar']
    def __init__(self):
        parser = argparse.ArgumentParser(description='Axie Scholar Tracker')
        self.add_arguments(parser)
        self.handle(**vars(parser.parse_args()))

    def add_arguments(self, parser):
        actions_help = ' | '.join(self.actions)        
        parser.add_argument('action', action='store', help=actions_help)
        parser.add_argument('data', action='store', nargs='*',
                            help='data to pass to action (list of key=value '
                                 ' pairs)')

    def handle(self, **options):
        action = options['action']
        data = options.get('data', None)

        if action in self.actions:
            method = getattr(self, f"_action_{action}", None)
            if method is not None:
                return method(data) 
            raise NotImplementedError            
        else:
            raise RuntimeError(f"Unsupported action: {action}")

    def _action_help_action(self, data):
        """Print an example about how to use the selected action
        """
        cmd = data[0] if data else ''
        if cmd not in self.actions:
            raise RuntimeError(f"Unsupported action: {cmd}")
        
        msg = f"E.g.:\n{sys.argv[0]} {cmd} "
        if cmd == 'help_cmd':
            msg = f"E.g.:\n{sys.argv[0]} <cmd> "
        elif cmd == 'init_db':
            pass
        elif cmd == 'add_scholar':
            msg += "name=antani ronin_id=1234567890..abcdef ..." 
        
        print(msg)

    def _action_init_db(self, data):
        """Init the new db.
        
        It must not exist. It creates a new empty sqlite db file.
        """
        create_db()

    def _action_add_scholar(self, data):
        """Manage the args and add the new scholar in the db.
        """
        pairs = {}
        for item in data:
            unpack = item.split('=')
            if len(unpack) != 2:
                err = f"Error: item '{item}' is not a key=value pair"
                raise RuntimeError(err)
            pairs[unpack[0]] = unpack[1]

        required_fields = ('name', 'ronin_id')
        for field in required_fields:
            if field not in pairs:
                err = f"Missing required field '{field}'"
                raise RuntimeError(err)

        name = pairs.pop('name')
        ronin_id = pairs.pop('ronin_id')
        add_scholar(name, ronin_id, **pairs)


if __name__ == "__main__":
    # logging
    logger = logging.root
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())

    c = Command()
