#       NTBBloodbath | PyBase v0.0.1       #
############################################
# PyBase is distributed under MIT License. #

# dependencies (packages/modules)
import yaml
import json
import sqlite3
import pathlib
import os
from os import path


class PyBase:
    """
    PyBase Main Class

    ...

    Attributes
    ----------

    Methods
    -------
    delete(obj)
        Delete a object from the database established in PyBase init.
    exists(database: str, db_type: str)
        Fetch if the given database exists.
    fetch(obj: str, sub=None)
        Fetch an object and its sub_objects inside the database established in PyBase init.
    insert(content: dict)
        Insert a dictionary content inside the given database file.
    read()
        Read the database file established in PyBase init to to access its objects.
            
    TODO:
        Add SQLite support.
        Add more useful methods.
        Improve existing methods & banner.
    """
    def __init__(self,
                 database: str,
                 db_type: str,
                 db_path: str = pathlib.Path().absolute()):
        """
        Define the database to use and create it if it doesn't exist.

        ...

        Parameters
        ----------
        database : str
            The name of the database without extension.
        db_type : str
            The database type.
            Available types: yaml, json, sqlite
        db_path : str
            The path where the database is located (default is current working directory).
            Example: /home/bloodbath/Desktop/PyBase

        Raises
        ------
        TypeError
            If database or db_type isn't a String.
        ValueError
            If the given db_type isn't a valid type (JSON, YAML, SQLite).
        FileNotFoundError
            If the given path wasn't found.
        """

        self.__path = db_path  # private path variable to clean code.

        if type(database) != str:
            raise TypeError('database must be a String.')
        elif type(db_type) != str:
            raise TypeError('db_type must be a String.')
        elif path.exists(db_path) != True:
            raise FileNotFoundError(
                f'The path ({self.__path}) wasn\'t found. Please check that the path exists.'
            )
        elif type(db_type) == str:
            self.__EXTENSION = '.' + db_type.lower(
            ) if db_type != 'SQLite' else '.db'
            self.__DB = (f'{self.__path}/{database}{self.__EXTENSION}')
            if db_type.lower() == 'json':
                if path.exists(self.__DB) == False:
                    try:
                        with open(self.__DB, mode='w+',
                                  encoding='utf-8') as json_file:
                            json.dump({}, json_file)
                    except Exception as err:
                        print(f'[ERROR]: {err.__class__}')
            elif db_type.lower() == 'yaml':
                if path.exists(self.__DB) == False:
                    try:
                        with open(self.__DB, mode='w+',
                                  encoding='utf-8') as yaml_file:
                            yaml.dump('---\n', yaml_file)
                    except Exception as err:
                        print(f'[ERROR]: {err.__class__}')
            elif db_type.lower() == 'sqlite':
                self.__sql_conn = sqlite3.connect(self.__DB)
            else:
                raise ValueError('db_type must be JSON, YAML or SQLite.')

    def delete(self, obj):
        """
        Delete a object from the database established in PyBase init.

        ...
        
        Parameters
        ----------
        obj
            The object which will be deleted from the database.

        Raises
        ------
        KeyError
            If key isn't found.
        ValueError
            If obj doesn't have a value (is equal to zero or None).
        """

        if len(obj) == 0 or obj is None:
            raise ValueError('obj must have a value (str, int, float, bool).')
        else:
            if self.__EXTENSION == '.json':
                try:
                    with open(self.__DB, encoding='utf-8') as json_file:
                        data = json.load(
                            json_file)  # Pass JSON to Python objects.
                        data.pop(obj)  # Delete the given object.
                    with open(self.__DB, mode='w',
                              encoding='utf-8') as json_file:
                        json.dump(data, json_file, indent=4,
                                  sort_keys=True)  # Save
                except KeyError as err:
                    print(f'[ERROR]: {err.__class_}')
            elif self.__EXTENSION == '.yaml':
                try:
                    with open(self.__DB, encoding='utf-8') as yaml_file:
                        data = yaml.load(yaml_file, Loader=yaml.FullLoader)
                        data.pop(obj)
                    with open(self.__DB, mode='w',
                              encoding='utf-8') as yaml_file:
                        yaml.dump(data, yaml_file, sort_keys=True)
                except KeyError as err:
                    print(f'[ERROR]: {err.__class__}')

    def exists(self, database: str, db_path: str = pathlib.Path().absolute()):
        """
        Fetch if the given database exists.

        ...

        Parameters
        ----------
        database : str
            The name of the database with extension.

        db_path : str
           The path where the database is located (default is current working directory).
           Example: /home/bloodbath/Desktop/PyBase

        Raises
        ------
        TypeError
            If database or db_path isn't a String.

        Returns
        -------
        bool
            Returns True or False depending on if the database given exists in the given path.
        """

        if type(database) != str:
            raise TypeError('database must be a String.')
        elif type(db_path) != str:
            raise TypeError('db_path must be a String.')
        else:
            if path.exists(f'{db_path}/{database}') == True:
                return True
            else:
                return False

    def fetch(self, obj: str, sub: dict = None):
        """
        Fetch an object and its sub_objects inside the database established in PyBase init.

        ...

        Parameters
        ----------
        obj : str
            The object which will be fetched inside the database.
        sub : dict, optional
            The sub_object(s) of the object which will be fetched inside the database.

        Raises
        ------
        TypeError
            If obj isn't a String or if sub isn't a list.
        ValueError
            If sub have more than 5 objects inside.
        KeyError
            If sub doesn't exist in the database.

        Returns
        -------
        str
            If the object or sub_objects are a String.
        int
            If the object or sub_objects are a Integer.
        float
            If the object or sub_objects are a Float.
        bool
            If the object or sub_objects are a Boolean.

        TODO:
            Add support for more objects inside the lists.
        """
        if type(obj) != str:
            raise TypeError('obj must be a String.')
        elif sub != None and type(sub) != dict:
            raise TypeError('sub must be a dict.')
        elif sub != None and len(sub) > 5:
            raise ValueError('sub can\'t have more than 5 objects inside.')
        else:
            obj = dict({obj: sub}) if sub != None and len(sub) >= 1 else {
                obj: ''
            }
            if self.__EXTENSION == '.json':
                with open(self.__DB, mode='r', encoding='utf-8') as json_file:
                    data = json.load(json_file)
                    for key in list(obj):
                        if key in data and sub != None and len(sub) != 0:
                            try:
                                # Establish the maximum deep of the fetch to 5 objects.
                                if len(sub) == 1 and list(
                                        sub)[0] in data[key].keys():
                                    return type(data[key][list(sub)[0]])
                                elif len(sub) == 2 and list(
                                        sub)[1] in data[key].keys():
                                    return type(data[key][list(sub)[1]])
                                elif len(sub) == 3 and list(
                                        sub)[2] in data[key].keys():
                                    return type(data[key][list(sub)[2]])
                                elif len(sub) == 4 and list(
                                        sub)[3] in data[key].keys():
                                    return type(data[key][list(sub)[3]])
                                elif len(sub) == 5 and list(
                                        sub)[4] in data[key].keys():
                                    return type(data[key][list(sub)[4]])
                            except KeyError as err:
                                print(f'[ERROR]: {err.__class__}')
                        else:
                            try:
                                return type(data[key])
                            except KeyError as e:
                                print(f'[ERROR]: {err.__class__}')
            elif self.__EXTENSION == '.yaml':
                with open(self.__DB, mode='r', encoding='utf-8') as yaml_file:
                    data = yaml.load(yaml_file, Loader=yaml.FullLoader)
                    for key in list(obj):
                        if key in data and sub != None and len(sub) != 0:
                            try:
                                # Establish the maximum deep of the fetch to 5 objects.
                                if len(sub) == 1 and list(
                                        sub)[0] in data[key].keys():
                                    return type(data[key][list(sub)[0]])
                                elif len(sub) == 2 and list(
                                        sub)[1] in data[key].keys():
                                    return type(data[key][list(sub)[1]])
                                elif len(sub) == 3 and list(
                                        sub)[2] in data[key].keys():
                                    return type(data[key][list(sub)[2]])
                                elif len(sub) == 4 and list(
                                        sub)[3] in data[key].keys():
                                    return type(data[key][list(sub)[3]])
                                elif len(sub) == 5 and list(
                                        sub)[4] in data[key].keys():
                                    return type(data[key][list(sub)[4]])
                            except KeyError as err:
                                print(f'[ERROR]: {err.__class__}')
                        else:
                            try:
                                return type(data[key])
                            except KeyError as e:
                                print(f'[ERROR]: {err.__class__}')

    def insert(self, content: dict):
        """
        Insert a dictionary content inside the database file established in PyBase init.
        
        ...

        Parameters
        ----------
        content : dict
            The content which will be inserted inside the database.
            
        Raises
        ------
        TypeError
            If content isn't a dictionary.
        """

        if type(content) != dict:
            raise TypeError('content must be a dictionary.')
        else:
            if self.__EXTENSION == '.json':
                try:
                    with open(self.__DB, encoding='utf-8') as json_file:
                        data = json.load(json_file)
                        data.update(content)
                    with open(self.__DB, mode='w',
                              encoding='utf-8') as json_file:
                        json.dump(data, json_file, indent=4, sort_keys=True)
                except Exception as err:
                    print(f'[ERROR]: {err.__class__}')
            elif self.__EXTENSION == '.yaml':
                try:
                    with open(self.__DB, encoding='utf-8') as yaml_file:
                        data = yaml.load(yaml_file, Loader=yaml.FullLoader)
                        data.update(content)
                    with open(self.__DB, mode='w',
                              encoding='utf-8') as yaml_file:
                        yaml.dump(data, yaml_file, sort_keys=True)
                except Exception as err:
                    print(f'[ERROR]: {err.__class__}')

    def read(self):
        """
        Read the database file established in PyBase init to access its objects.

        ...

        Parameters
        ----------

        Raises
        ------

        Returns
        -------
        dict
            A dictionary which contains all the database objects.
        """

        if self.__EXTENSION == '.json':
            try:
                with open(self.__DB, mode='r+', encoding='utf-8') as json_file:
                    data = json.load(json_file)
                    return data
            except Exception as err:
                print(f'[ERROR]: {err.__class__}')
        elif self.__EXTENSION == '.yaml':
            try:
                with open(self.__DB, mode='r+', encoding='utf-8') as yaml_file:
                    data = yaml.load(yaml_file, Loader=yaml.FullLoader)
                    return data
            except Exception as err:
                print(f'[ERROR]: {err.__class__}')
