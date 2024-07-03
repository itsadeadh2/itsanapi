from .config import add_configs
from .cors import add_cors
from .resources import add_resources
from .injector import AppModule

__all__ = ['add_configs', 'add_cors', 'add_resources', 'AppModule']
