import configparser
from os import path
from getpass import getpass, getuser
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.ext import declarative

from ezreal.utils import base_folder

config_location = path.join(base_folder, 'db_config.ini')
db_config = configparser.ConfigParser()

Base = declarative.declarative_base()

# Opening the database
try:
    with open(config_location) as configfile:
        db_config.read_file(configfile)
except FileNotFoundError:
    print(f'Database config file not found. No database configured.\n'
          f'This program is able to setup a database starting kit in SQLite.\n'
          f'You can also choose to use a postgresql databse and configure its access by following.\n'
          f'It will be saved in clear text at {path.join(base_folder, "db_config.ini")}\n'
          f'Please input your db choice: [postgresql/sqlite]')
    db_choice = input()
    db_config['general'] = {}
    if db_choice == 'sqlite':
        db_config['general']['db_type'] = db_choice
        print(f'SQLite database setup complete.')
    elif db_choice == 'postgresql':
        db_config['general']['db_type'] = db_choice
        db_config['connection_info'] = {}
        print(f'username:')
        db_config['connection_info']['username'] = getuser()
        print(f'password:')
        db_config['connection_info']['password'] = getpass()
        print(f'host:')
        db_config['connection_info']['host'] = input()
        print(f'port:')
        db_config['connection_info']['port'] = input()
        print(f'database:')
        db_config['connection_info']['database'] = input()
        print(f'PostgreSQL database setup complete.')
    else:
        raise ReferenceError("Unrecognize string or database type not allowed.")
    with open(config_location, 'w+') as configfile:
        db_config.write(configfile)


if db_config.get('general', 'db_type') == 'sqlite':
    database_location = path.join(base_folder, 'ezreal_core_schema.db')
    db_url = db_config.get('general', 'db_type') + ':///{}'.format(database_location)
elif db_config.get('general', 'db_type') == 'postgresql':
    db_url = db_config.get('general', 'db_type') + '://' + db_config.get('connection_info', 'username') + ':' \
             + db_config.get('connection_info', 'password') + '@' + db_config.get('connection_info', 'host') \
             + ':' + db_config.get('connection_info', 'port') + '/' + db_config.get('connection_info', 'database')

engine = sqlalchemy.create_engine(db_url)

# Creating an easy access function
get_session = orm.sessionmaker(bind=engine)

# Defining the function to call at the end of the sqlite initialization
def initialize_sql():
    Base.metadata.create_all(engine)