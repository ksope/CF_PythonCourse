Command Line Recipe App

Aim
To build a complete Recipe app that runs on terminal using Python

Description
The Recipe will be built using Python and mySQL and will be able to do the folowing:

1. Create a new recipe
2. View all recipes
3. Search a recipe by ingredients
4. Edit a recipe
5. Delete a recipe

Directions to install and run project:
Clone Repo
Open a terminal, activate it with a virtual environment of your choice, and type the following command:

1. 'pip install sqlalchemy' - to install SQLAlchemy
2. 'pip install mysqlclient' - to install connector

Ensure MySQL Server is Running

Setup
To display installed environments: workon
To load 'cf-python-base' environment: workon cf-python-base
To load 'cf-python-copy' environment: workon cf-python-copy

Open an IPython shell and import the following:
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import sessionmaker

To Use application:
Create a few recipes of your own
Select an option from the Main Menu, to quit the application from the Main Menu, enter 'quit'
