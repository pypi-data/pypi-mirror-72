"""
This library allows you to quickly and easily use the SoWeMail Rest API via Python.

For more information on this library, see the README on GitHub.
    https://github.com/sowemail/sowemail-python
For more information on the SoWeMail API, see the v1 docs:
    https://sowemail.com/docs/API_Reference/v1.html

Available subpackages
---------------------
helpers
    Modules to help with common tasks.
"""

import os
from .helpers.mail import *  # noqa
from .sowemail import SoWeMailAPIClient  # noqa

dir_path = os.path.dirname(os.path.realpath(__file__))
if os.path.isfile(os.path.join(dir_path, 'VERSION.txt')):
    with open(os.path.join(dir_path, 'VERSION.txt')) as version_file:
        __version__ = version_file.read().strip()

__sowemail_api_version__ = 1
