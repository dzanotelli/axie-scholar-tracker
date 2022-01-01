#!/usr/bin/env python3

import argparse
import logging
import sys

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
        print(data)

        if action in self.actions:
            method = getattr(self, f"_action_{action}", None)
            if method is not None:
                return method(data) 
            raise NotImplementedError            
        else:
            raise RuntimeError(f"Unsupported action: {action}")

    def _action_help_action(self, data):
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
        create_db()

    def _action_add_scholar(self, data):
        logger.info(data)
        pass



if __name__ == "__main__":
    # logging
    logger = logging.root
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())

    c = Command()
