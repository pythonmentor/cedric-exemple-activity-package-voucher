import os

from .base import *
from .base import env

# Allow the use of a Jupyter notebook with database
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
