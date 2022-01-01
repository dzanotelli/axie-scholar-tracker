#!/usr/bin/env python3

import argparse
import logging
import sys

from datetime import datetime

from db.models import Scholar
from db.utils import create_db


_version = "0.0.0"


class Command:
    actions = ['help_action', 'init_db', 'add_scholar', 'read_scholar']

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

    def _unpack_data(self, data):
        """Read the raw data (command line) and unpack to dict

        Args:
            data (str): 'key0=value0 key1=value1 ..'

        Returns:
            dict - {"key0": "value0", "key1": "value1", ...}
        
        """
        pairs = {}
        for item in data:
            unpack = item.split('=')
            if len(unpack) != 2:
                err = f"Error: item '{item}' is not a key=value pair"
                raise RuntimeError(err)
            pairs[unpack[0]] = unpack[1]
        return pairs

    # actions

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
            msg += "name=antani ronin_id=1234567890..abcdef "
            msg += "[joined_date=2022-01-01T00:00:00+00:00 ...]" 
        elif cmd == 'read_scholar':
            msg += "internal_id=42"

        print(msg)

    def _action_init_db(self, data):
        """Init the new db.
        
        It must not exist. It creates a new empty sqlite db file.
        """
        print("Initing empty database ...", end='', flush=True)
        create_db()
        print("done.")

    def _action_add_scholar(self, data):
        """Manage the args and add the new scholar in the db.
        """
        pairs = self._unpack_data(data)        
        required_fields = ('internal_id', 'ronin_id')
        for field in required_fields:
            if field not in pairs:
                err = f"Missing required field '{field}'"
                raise RuntimeError(err)

        s = Scholar(**pairs)
        s.save()

    def _action_read_scholar(self, data):
        """Read a single scholar
        """
        pairs = self._unpack_data(data)
        if not len(pairs):
            err = 'Missing lookup field. Try with internal_id=...'
            raise RuntimeError(err)
        
        lookup_field = list(pairs)[0]
        lookup_value = pairs[lookup_field]

        if lookup_field not in Scholar.fields:
            err = f"'{lookup_field} is not a valid Scholar field"
            raise RuntimeError(err)
        
        scholars = Scholar.filter_by(**{lookup_field: lookup_value})

        # print to stdout
        headers = ['result #'] + Scholar.fields
        headers_str = " | ".join(headers)
        print(headers_str)
        print('-'*len(headers_str))
        for i, scholar in enumerate(scholars):
            data = [i]
            data += [getattr(scholar, field) for field in headers[1:]]
            data_str = " | ".join([str(item) for item in data])
            print(data_str)

    def _action_del_scholar(self, data):
        pass


if __name__ == "__main__":
    logging
    logger = logging.root
    logger.setLevel(logging.ERROR)
    logger.addHandler(logging.StreamHandler())

    c = Command()
