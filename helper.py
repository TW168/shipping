from sqlalchemy import create_engine
import configparser

def connect_to_database(section='DEFAULT', dbms='mysql'):
    """
    Connect to a database using connection information from a config file.

    Parameters:
        section (str): The name of the section in the config file that contains the connection information.
        dbms (str): The name of the database management system (DBMS) to use (default is 'mysql').

    Returns:
        sqlalchemy.engine.Connection: A connection object that can be used to execute SQL queries.

    Raises:
        ValueError: If the specified section is not found in the config file.
    """
    config = configparser.ConfigParser()
    config.read('config.py')
    if section not in config.sections():
        raise ValueError(f'Section {section} not found in config.py')

    # Get the connection information from the specified section
    user = config[section]['user']
    password = config[section]['password']
    host = config[section]['host']
    port = int(config[section]['port'])
    database = config[section]['database']

    # Create a connection string using sqlalchemy and the specified DBMS
    connection_string = f'{dbms}+pymysql://{user}:{password}@{host}:{port}/{database}'
    # Create an engine object with the connection string
    engine = create_engine(connection_string)
    # Test the connection by executing a simple query
    conn = engine.connect()
    print(f'Successfully connected to {dbms.upper()} database: {database}')
    return conn
