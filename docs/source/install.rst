Installation
============

Create a dedicated Python 3.9 environment, for instance, using conda:

.. code-block:: bash

    $ conda create -n connect4 python=3.9
    $ conda activate connect4

For users
---------

install the connect4 package

.. code-block:: bash

    $ cd /path/to/package
    $ pip install .

For developers
--------------

install the test framework and the pre-commit hooks

.. code-block:: bash

    $ pip install -e ".[dev]"
    $ pre-commit install
