============================
CloudBees CD/RO Python REST API wrapper
============================

|Build Status| |PyPI version| |PyPI - Downloads| |License| |Codacy Badge| |Docs|

What is it?
___________
This package is used to provide a **simple** python interface for interacting with Cloudbees products
(CloudBees CD/RO).
It is based on the official public Rest API documentation and private methods (+ xml+rpc, raw http request).

Documentation
_____________

`Documentation`_

.. _Documentation: https://cloudbees-python-api.readthedocs.io

How to Install?
_______________

From PyPI

.. code-block:: console

   $ pip install cloudbees-python-api

From Source

- Git clone repository
- Use :code:`pip install -r requirements.txt` to install the required packages
- or :code:`pipenv install && pipenv install --dev`

Examples
________
More **examples** in :code:`examples/` directory.

Here's a short example of how to create a Confluence page:

.. code-block:: python

    from clouebees import CDRO

    cdro = CDRO(
        url='http://localhost:8090',
        username='admin',
        password='admin')

    status = cdro.add_user(
        email='foo@example.com',
        fullname='Foo Bar',
        username='foo',
        password='password')

    print(status)

.. code-block:: python

    from pprint import pprint
    # you code here
    # and then print using pprint(result) instead of print(result)
    pprint(response)

How to contribute?
__________________
First of all, I am happy for any PR requests.
Let's fork and provide your changes :)
See the `Contribution Guidelines for this project`_ for details on how to make changes to this library.

.. _Contribution Guidelines for this project: CONTRIBUTING.rst
.. |Build Status| image:: https://github.com/zhan9san/cloudbees-python-api/workflows/Test/badge.svg?branch=main
   :target: https://github.com/zhan9san/cloudbees-python-api/actions?query=workflow%3ATest+branch%3Amain
   :alt: Build status
.. |PyPI version| image:: https://badge.fury.io/py/cloudbees-python-api.svg
   :target: https://badge.fury.io/py/cloudbees-python-api
   :alt: PyPI version
.. |License| image:: https://img.shields.io/pypi/l/cloudbees-python-api.svg
   :target: https://pypi.python.org/pypi/cloudbees-python-api
   :alt: License
.. |PyPI - Downloads| image:: https://pepy.tech/badge/cloudbees-python-api/month
   :alt: PyPI - Downloads
.. |Docs| image:: https://readthedocs.org/projects/cloudbees-python-api/badge/?version=latest
   :target: https://cloudbees-python-api.readthedocs.io/?badge=latest
   :alt: Documentation Status

Credits
_______
In addition to all the contributors we would like to thank these vendors:

* Cloudbees_ for developing such a powerful ecosystem.
* Microsoft_ for providing us with free licenses of VSCode_
* GitHub_ for hosting our repository and continuous integration

.. _Cloudbees: https://www.cloudbees.com/
.. _GitHub: https://github.com/
.. _Microsoft: https://github.com/Microsoft/vscode/
.. _VSCode: https://code.visualstudio.com/
