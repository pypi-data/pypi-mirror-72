"""
This library allows you to quickly and easily use the SoWeMail Rest API via Python.

For more information on this library, see the README on GitHub.
    https://github.com/sowemail/sowemail-python
For more information on the SoWeMail API, see the v1 docs:
    https://sowemail.com/docs/API_Reference/v1.html

This file provides the SoWeMail API Client.
"""

import os

from .base_interface import BaseInterface


class SoWeMailAPIClient(BaseInterface):
    """The SoWeMail API Client.

    Use this object to interact with the API. For example:
        mail_client = sowemail.SoWeMailAPIClient(os.environ.get('SOWEMAIL_API_KEY'))
        ...
        mail = Mail(from_email, subject, to_email, content)
        response = mail_client.send(mail)

    For examples and detailed use instructions, see
        https://github.com/sowemail/sowemail-python
    """

    def __init__(
            self,
            api_key=None,
            host='https://api.sowemail.com'):
        """
        Construct the SoWeMail API object.
        Note that the underlying client is being set up during initialization,
        therefore changing attributes in runtime will not affect HTTP client
        behaviour.

        :param api_key: SoWeMail API key to use. If not provided, value
                        will be read from environment variable "SOWEMAIL_API_KEY"
        :type api_key: string
        :param host: base URL for API calls
        :type host: string
        """
        self.api_key = api_key or os.environ.get('SOWEMAIL_API_KEY')
        auth = 'Bearer {}'.format(self.api_key)

        super(SoWeMailAPIClient, self).__init__(auth, host)
