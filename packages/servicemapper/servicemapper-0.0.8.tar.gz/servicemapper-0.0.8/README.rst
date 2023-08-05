**************
servicemapper
**************
PIPSC Service Mapper is a framework for connecting external services
and sharing data using the PIPSC Data Steward service.

Prerequisites
-------------
* Python 3
* Virtualenv
* npm

Environment Setup
-----------------
Note:  If using zsh, you'll need to use 'noglob' to prevent zsh from using the square brackets for pattern matching.  
A useful alias is
.. code-block:: bash

    $ alias pip='noglob pip3'

Setup the virutalenv and install the dev dependencies:
.. code-block:: bash

    $ npm run venv
    $ source .venv/bin/activate
    $ pip install -e .[dev]

Creating a Manifest
-------------------
.. code-block:: bash

    $ check-manifest --create
    $ git add MANIFEST.ini


Package Testing with tox
------------------------
.. code-block:: bash

    $ tox

Build the Package
-----------------
.. code-block:: bash

    $ python3 setup.py bdist_wheel sdist

Publish the Package
-------------------
.. code-block:: bash

    $ twine upload dist/*


Using the Package
-----------------
To use the servicemapper package in another project you must
configure the package repository, then import servicemapper

.. code-block:: bash

    $ pip install servicemapper

Relevant Info
-------------
https://godatadriven.com/blog/a-practical-guide-to-using-setup-py/
https://www.youtube.com/watch?v=GIF3LaRqgXo

