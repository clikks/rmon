"""
rmon.config
rmon config file
"""

import os


class DevConfig:
    """
    Development Envrioment Config
    """

    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    TEMPLATES_AUTO_RELOAD = True


class ProductConfig(DevConfig):
    """
    Production Enviroment Config
    """

    DEBUG = False


    path = os.path.join(os.getcwd(), 'rmon.db').replace('\\','/')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' %path

