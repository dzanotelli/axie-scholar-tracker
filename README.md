# axie-scholar-tracker
A tool to keep track of Axie Infinity Scholar daily performances

## Requirements
- python>=3.9
- sqlite3

## Install

*For the sake of simplicity in this guide we are using the root user; actually
it's advised to use a specific user and consequently adjust all the paths.* 

1. clone the repository in `/opt` (or in some other path you have write access)
```
~# cd /opt
/opt# git clone git@github.com:dzanotelli/axie-scholar-tracker.git
```

2. create a new virtualenv somewhere (e.g. in `/root`), and activate it
```
~# virtualenv -ppython3 axieST_venv
~# ./axieST_venv/bin/activate
(axieST_venv) ~#
```

3. install the requirements with 
```
(axieST_venv) ~# pip install -r /opt/axie-scholar-tracker/requirements.txt
```

4. init the database
```
(axieST_venv) ~# cd /opt/axie-scholar-tracker/
(axieST_venv) /opt/axie-scholar-tracker/# python axieST.py init_db
Initing empty database ...done.
```

5. copy the crontab file `crontab/axieST` into `/etc/cron.d/`. This will
activate the retrieveing of data of your scholars every day at midnight.

*Adjust paths in this file if you used custom directories (check the file
for more).*

## Usage

Please check
```
(venv) $ python axieST.py --help  
```

to get the list of the available actions and
```
(venv) $ python axieST.py action_help <action>  
```
to get help about a specific action.


## Basic workflow

1. add a new scholar
```
(axieST_venv) ~# python axieST.py add_scholar internal_id='#1' 
ronin_id=fa5ea3...741b name="Bruce Wayne" battle_name=batman
```

2. list scholars
```
(axieST_venv) ~# python axieST.py list_scholars
internal_id | name | battle_name | join_date | is_active | ronin_id
-------------------------------------------------------------------
#1 | Bruce Wayne | batman | 2022-01-01 10:01:00.487522 | True | a5ea3...741b
```
*so you can retrieve the `internal_id` if you forgot it*

3. get scholar data
```
(axieST_venv) ~# python axieST.py get_tracks internal_id=#1
```
which will extract scholar's data of the last N days (default is 14 days).

**IMPORTANT!** It's possibile to use the flag `format` to get data in json
or csv, e.g.:
``` 
(axieST_venv) ~# python axieST.py get_tracks internal_id=#1 format=csv

id,insert_date,mmr,rank,total_slp,raw_total,in_game_slp,ronin_slp,lifetime_slp,last_claim,next_claim,player_name
1,2022-01-03 00:00:00.000001,1372,1482,1517,1517,,0,0,2021-02-30 03:59:50,2021-03-14 03:59:50,[OvumEsports] Mr. Batman
2,2022-01-04 00:00:00.000004,1388,1330,1728,1728,,0,0,2021-02-30 03:59:50,2021-03-14 03:59:50,[OvumEsports] Mr. Batman
```
and of course appending `... format=csv > data.csv` to the command line is
possible to save data to file.

