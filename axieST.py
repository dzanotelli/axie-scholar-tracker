#!/usr/bin/env python3

import argparse
import csv
import io
import json
import sys

from sqlalchemy.engine import base

from datamanager.core import DataManager
from db.models import Scholar, Track
from db.utils import create_db, json_serial


_version = "0.1.0"


class Command:
    actions = ['help_action', 'init_db', 'add_scholar', 'get_scholar',
               'upd_scholar', 'del_scholar', 'list_scholars', 
               'collect_axie_data', 'get_tracks']

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
        
        base_call = f"$ {sys.argv[0]} {cmd} "

        if cmd == 'help_action':
            msg = "Ask help about a specific action\n\n"
            msg += f"E.g.:\n{sys.argv[0]} <cmd> "
        elif cmd == 'add_scholar':
            msg = "Add a new scholar to database\n\n"
            msg += base_call + "name=antani ronin_id=1234567890..abcdef "
            msg += "[joined_date=2022-01-01T00:00:00+00:00 ...]" 
        elif cmd == 'get_scholar':
            msg = "Print info about a scholar\n\n"
            msg += base_call + "internal_id=42\n"
            msg += base_call + "battle_name=batman"
        elif cmd == 'upd_scholar':
            msg = "Update scholar info\n\n"
            msg += base_call + "internal_id=42 name='Clark Kent' "
            msg += "battle_name=superman\n\n"
            msg += "The scholar being updated will be the one which matches "
            msg += "the internal_id"
        elif cmd == 'del_scholar':
            msg = "Delete a scholar from database\n\n"
            msg += base_call + "internal_id=42"
        elif cmd == 'list_scholars':
            msg = "List all the scholars\n\n"
            msg += base_call + '\n\n'
            msg += "If a scholar is marked as not active, the system will "
            msg += "not collect data for her."
        elif cmd == "collect_axie_data":
            msg = "Call the axie API and collect data of active scholars\n\n"
            msg += base_call + '\n\n'
            msg += "This command is meant to be called daily by the cron job."
        elif cmd == 'get_tracks':
            msg = "Get tracks (game info) about a scholar\n\n"
            msg += base_call + "internal_id=42\n"
            msg += base_call + "internal_id=42 days=7\n"
            msg += base_call + "internal_id=42 days=0 format=json\n"
            msg += base_call + "internal_id=42 days=0 format=csv > data.csv\n"
            msg += "\n(days=0 means get all data, defaul is 14)"
        else:
            # here all the actions which does not require further help
            pass

        print(msg)

    def _print_scholar_table(self, scholars):
        """Print a table with all the scholars' data

        Args:
            scholars (list): list of Scholar

        """
        # print headers
        fields = list(Scholar.fields)
        fields.remove('id')        
        headers_str = " | ".join(fields)
        print(headers_str)
        print('-'*len(headers_str))

        # print scholar data
        for scholar in scholars:
            data = [getattr(scholar, field) for field in fields]
            data_str = " | ".join([str(item) for item in data])
            print(data_str)

        if not len(scholars):
            print("Not found.")

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

    def _action_get_scholar(self, data):
        """Read scholar data
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
        
        # there should be just one (or none)
        scholars = list(Scholar.filter_by(**{lookup_field: lookup_value}))
        self._print_scholar_table(scholars)

    def _action_upd_scholar(self, data):
        """Update a scholar using its internal_id as lookup field
        """
        pairs = self._unpack_data(data)
        if not 'internal_id' in pairs:
            err = "Missing 'internal_id': cannot retrieve scholar"
            raise RuntimeError(err)
        
        internal_id = pairs.pop('internal_id')

        scholar = Scholar.get_by(internal_id=internal_id)
        if not scholar:
            print("Not found.")
            return
        
        for key, value in pairs.items():
            if key not in Scholar.fields or key == 'id':
                raise RuntimeError(f'Bad field given: {key}')
            setattr(scholar, key, value)

        scholar.save()
        print('Updated.')

    def _action_del_scholar(self, data):
        pairs = self._unpack_data(data)
        if not 'internal_id' in pairs:
            err = "Missing 'internal_id': cannot retrieve scholar"
            raise RuntimeError(err)
        
        internal_id = pairs.pop('internal_id')

        scholar = Scholar.get_by(internal_id=internal_id)
        if not scholar:
            print("Not found.")
            return

        scholar.delete()
        print("Deleted.")

    def _action_list_scholars(self, data):
        """Print all the scholars
        """
        scholars = Scholar.filter_by().all()
        self._print_scholar_table(scholars)

    def _action_collect_axie_data(self, data):
        """
        Collect data for each scholar 

        """
        print("Collecting new data from axie ...")
        for scholar in Scholar.filter_by(is_active=True):
            print(f'\tScholar: {scholar} ...', end='', flush=True)
            dm = DataManager(scholar)
            if dm.collect_new_data():
                print("done.")
            else:
                print("error.")
    
    def _action_get_tracks(self, data):
        pairs = self._unpack_data(data)        

        internal_id = pairs.get('internal_id', None)
        if internal_id is None:
            raise RuntimeError("Missing arg: internal_id")
        
        scholar = Scholar.get_by(internal_id=internal_id)
        if scholar is None:
            err = f"Scholar(internal_id='{internal_id}') not found"
            raise RuntimeError(err)
        
        days = pairs.get('days', 14)
        try:
            days = int(days)
            if days < 0:
                raise ValueError
        except ValueError:
            raise RuntimeError('days must be a positive integer or 0')

        # get data
        dm =  DataManager(scholar)
        tracks = dm.get_scholar_tracks(days=days)
        
        # return data
        fmt = pairs.get('format', None)
        if fmt is None:
            # we remove the scholar_id (foreign key)
            fields = list(Track.fields)
            fields.remove('scholar_id')

            headers = ' | '.join(fields)
            print(headers)
            print("-" * len(headers))
            for track in tracks:
                data = [getattr(track, field) for field in fields]
                data_str = " | ".join([str(item) for item in data])
                print(data_str)
        elif fmt.lower() == 'json':
            data = [track.to_dict() for track in tracks]
            data = json.dumps(data, default=json_serial)
            print(data)
        elif fmt.lower() == 'csv':
            fields = list(Track.fields)
            fields.remove('scholar_id')

            csvfile = io.StringIO()
            csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
            csvwriter.writerow(fields)
            for track in tracks:
                data = [getattr(track, field) for field in fields]
                csvwriter.writerow(data)

            csvfile.seek(0)
            for line in csvfile:
                print(line, end='')
            

if __name__ == "__main__":
    try:
        c = Command()
    except Exception as e:
        # suppress stacktrace   
        print(e)
