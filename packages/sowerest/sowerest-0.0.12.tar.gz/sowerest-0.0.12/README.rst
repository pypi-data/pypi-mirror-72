|Build Status| |Codecov branch| |Code Climate| |Python Versions| |PyPI Version| |MIT licensed|

**Quickly and easily access any RESTful or RESTful-like API.**

If you are looking for the sowemail API client library, please see `this repo`_.

Table of Contents
=================

-  `Installation <#installation>`__
-  `Quick Start <#quick-start>`__
-  `Usage <#usage>`__
-  `Roadmap <#roadmap>`__
-  `Local Setup of the Project <#local-setup-of-the-project>`__
-  `Troubleshooting <#troubleshooting>`__
-  `Announcements <#announcements>`__
-  `Thanks <#thanks>`__
-  `About <#about>`__
-  `License <#license>`__

Installation
============

Prerequisites
-------------

-  Python version 3.4+

Install Package
---------------

.. code:: bash

    pip install sowerest

or

.. code:: bash

    easy_install sowerest

API Key
-------

Store your sowemail API key in a ``.env`` file.

.. code:: bash

    cp .env_sample .env

Edit the ``.env`` file and add your API key.

Quick Start
===========

Here is a quick example:

``GET /your/api/{param}/call``

.. code:: python

    import sowerest

    global_headers = {"Authorization": "Bearer XXXXXXX"}
    client = Client(host='base_url', request_headers=global_headers)
    client.your.api._(param).call.get()
    print(response.status_code)
    print(response.headers)
    print(response.body)

``POST /your/api/{param}/call`` with headers, query parameters and a request body with versioning.

.. code:: python

    import sowerest

    global_headers = {"Authorization": "Bearer XXXXXXX"}
    client = Client(host='base_url', request_headers=global_headers)
    query_params = {"hello":0, "world":1}
    request_headers = {"X-Test": "test"}
    data = {"some": 1, "awesome": 2, "data": 3}
    response = client.your.api._(param).call.post(request_body=data,
                                                  query_params=query_params,
                                                  request_headers=request_headers)
    print(response.status_code)
    print(response.headers)
    print(response.body)

Usage
=====

-  `Example Code`_

Thanks
======

We were mainly inspired by the work done on `python-http-client`_, `birdy`_ and `universalclient`_.

License
=======

`The MIT License (MIT)`_

.. _this repo: https://github.com/sowemail/sowerest-python
.. _Example Code: https://github.com/sowemail/sowerest-python/tree/master/examples
.. _birdy: https://github.com/inueni/birdy
.. _universalclient: https://github.com/dgreisen/universalclient
.. _python-http-client: https://github.com/sendgrid/python-http-client
.. _The MIT License (MIT): https://github.com/sowemail/sowerest-python/blob/master/LICENSE

.. |Build Status| image:: https://travis-ci.com/sowemail/sowerest-python.svg?branch=master
   :target: https://travis-ci.com/sowemail/sowerest-python
.. |Codecov branch| image:: https://img.shields.io/codecov/c/github/sowemail/sowerest-python/master.svg?style=flat-square&label=Codecov+Coverage
   :target: https://codecov.io/gh/sowemail/sowerest-python
.. |Code Climate| image:: https://codeclimate.com/github/SoWeMail/sowerest-python/badges/gpa.svg
   :target: https://codeclimate.com/github/SoWeMail/sowerest-python
.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/sowerest.svg
   :target: https://pypi.org/project/sowerest
.. |PyPI Version| image:: https://img.shields.io/pypi/v/sowerest.svg
   :target: https://pypi.org/project/sowerest
.. |MIT licensed| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://github.com/SoWeMail/sowerest-python/blob/master/LICENSE
