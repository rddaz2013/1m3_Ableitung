__author__ = 'rened'

import inspect, importlib as implib

if __name__ == "__main__":
    mod = implib.import_module( "read_labview_rev2" )
    print mod
    for i in inspect.getmembers(mod, inspect.ismodule ):
        print i[0],i[1]

import pip
for package in pip.get_installed_distributions():
    name = package.project_name # SQLAlchemy, Django, Flask-OAuthlib
    key = package.key # sqlalchemy, django, flask-oauthlib
    module_name = package._get_metadata("top_level.txt") # sqlalchemy, django, flask_oauthlib
    location = package.location # virtualenv lib directory etc.
    version = package.version # version number

    print key,version