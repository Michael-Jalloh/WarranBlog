# Warran

## Usage

First thing first you need to install the python requirements. Create a virtual environment first

=========================================
``sudo apt-get install python-dev python-pip``

``sudo pip install virtualenv``

``virtualenv app``

``cd app``

``source bin/activate``

``pip install -r requirements.txt``
=======================================

That should get your system up to date. Now u need to create your user so that you will be able to make post on the side.
======================================
``python manage.py config``
======================================

follow the instructions. After creating the user test out the system by 
======================================
``python manage.py runserver``
======================================

Open the atom.py file and in the begin of the on line 9 and 10, change it to

``application.config.from_object(config['production'])``

``config['production'].init_app(application)``


That should get your webapp up and running. But from here on u will need to use a production server like nginx or apache. Look up google on how to use a flask app with one of those servers
