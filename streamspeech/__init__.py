"""

A web app to interact with Google's PaLM API 

.. author: Nelson Gonzabato

"""



import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from version import __version__
__author__ = "Nelson Gonzabato"
__all__ = ["app_main.py", "app.py"]
assert isinstance(__version__, str)
__version__ = __version__