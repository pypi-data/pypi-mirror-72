|Build Status| |Codecov branch| |Code Climate| |Python Versions| |PyPI Version| |MIT licensed|

**This library allows you to quickly and easily use the SoWeMail Rest API via Python.**

Table of Contents
=================

-  `Installation <#installation>`__
-  `Quick Start <#quick-start>`__
-  `Thanks <#thanks>`__
-  `License <#license>`__

Installation
============

Prerequisites
-------------

-  Python version 3.6+
-  You will need a SoWeMail account, `signup`_

Setup Environment Variables
---------------------------

Mac
~~~

Update the development environment with your `SOWEMAIL_API_KEY`_, for example:

.. code:: bash

    echo "export SOWEMAIL_API_KEY='YOUR_API_KEY'" > sowemail.env
    echo "sowemail.env" >> .gitignore
    source ./sowemail.env

SoWeMail also supports local environment file ``.env``.
Copy or rename ``.env_sample`` into ``.env`` and update `SOWEMAIL_API_KEY`_ with your key.

Windows
~~~~~~~

Temporarily set the environment variable (accessible only during the current CLI session):

.. code:: bash

    set SOWEMAIL_API_KEY=YOUR_API_KEY

Permanently set the environment variable (accessible in all subsequent CLI sessions):

.. code:: bash

    setx SOWEMAIL_API_KEY "YOUR_API_KEY"

Install Package
---------------

.. code:: bash

    pip install sowemail

Dependencies
------------

-  `sowerest`_

Quick Start
===========

Hello Email
-----------

The following is the minimum needed code to send an email with the `/mail/send Helper`_
(`here <https://github.com/sowemail/sowemail-python/blob/master/use_cases/kitchen_sink.md>`__ is a full example):

With Mail Helper Class
~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    import os
    from sowemail import SoWeMailAPIClient
    from sowemail.helpers.mail import Mail

    message = Mail(
        from_email='from_email@example.com',
        to_emails='to@example.com',
        subject='Hello from SoWeMail',
        html_content='<strong>Simple email sending example using python\'s sowerest library</strong>')
    try:
        sow_client = SoWeMailAPIClient(os.environ.get('SOWEMAIL_API_KEY'))
        response = sow_client.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(str(e))

The ``Mail`` constructor creates a personalization object for you.
`Here <https://github.com/sowemail/sowemail-python/blob/master/use_cases/kitchen_sink.md>`__ is an example of how to add it.

Without Mail Helper Class
~~~~~~~~~~~~~~~~~~~~~~~~~

The following is the minimum needed code to send an email without the /mail/send Helper
(`here <https://github.com/sowemail/sowemail-python/blob/master/examples/mail/mail.py#L27>`__ is a full example):

.. code:: python

    import os
    from sowemail import SoWeMailAPIClient

    message = {
        'personalizations': [
            {
                'to': [
                    {
                        'email': 'test@example.com'
                    }
                ],
                'subject': 'Hello from SoWeMail'
            }
        ],
        'from': {
            'email': 'test@example.com'
        },
        'content': [
            {
                'type': 'text/plain',
                'value': 'Simple email sending example using python\'s sowerest library'
            }
        ]
    }
    try:
        sow_client = SoWeMailAPIClient(os.environ.get('SOWEMAIL_API_KEY'))
        response = sow_client.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(str(e))

Thanks
======

This work were inspired and based on the awesome work done on `sendgrid-python`_.

License
=======

`The MIT License (MIT)`_

.. _signup: https://sowemail.com/signup?source=sowemail-python
.. _SOWEMAIL_API_KEY: https://app.sowemail.com/settings/api_keys
.. _sowerest: https://github.com/sowemail/sowerest-python
.. _/mail/send Helper: https://github.com/sowemail/sowemail-python/tree/master/sowemail/helpers/mail
.. _sendgrid-python: https://github.com/sendgrid/sendgrid-python
.. _The MIT License (MIT): https://github.com/sowemail/sowemail-python/blob/master/LICENSE.md

.. |Build Status| image:: https://travis-ci.com/sowemail/sowemail-python.svg?branch=master
   :target: https://travis-ci.com/sowemail/sowemail-python
.. |Codecov branch| image:: https://img.shields.io/codecov/c/github/sowemail/sowemail-python/master.svg?style=flat-square&label=Codecov+Coverage
   :target: https://codecov.io/gh/sowemail/sowemail-python
.. |Code Climate| image:: https://codeclimate.com/github/SoWeMail/sowemail-python/badges/gpa.svg
   :target: https://codeclimate.com/github/SoWeMail/sowemail-python
.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/sowemail.svg
   :target: https://pypi.org/project/sowemail
.. |PyPI Version| image:: https://img.shields.io/pypi/v/sowemail.svg
   :target: https://pypi.org/project/sowemail
.. |MIT licensed| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://github.com/SoWeMail/sowemail-python/blob/master/LICENSE
