===========
rcs-storage
===========

.. image:: https://gitlab.unimelb.edu.au/resplat-data/rcs-storage/badges/master/pipeline.svg
.. image:: https://gitlab.unimelb.edu.au/resplat-data/rcs-storage/badges/master/coverage.svg

Copyright © 2020 - The University of Melbourne.

BETA only - use in production environments at your own risk.

Installation
============

::

  pip install rcs-storage

Usage
=====

Command Line
------------

For example::

  rcs-storage collection list

For help::

  rcs-storage collection list -h

You may set the following environment variables so you don't have to pass
``--token`` and/or ``--host`` to the command every time you run it::

  export RCS_STORAGE_HOST=https://<hostname>/
  export RCS_STORAGE_TOKEN=<your token>

Python
------

For example::

  from rcs_storage.client import Client

  storage = Client(host=<host>, token=<token>)
  storage.collections.list()

Issues
======

Please submit issues using the `GitLab Issue Tracker`_.

Contributing
============

See `CONTRIBUTING.rst`_.

Changelog
=========

See the `change log`_.


.. _GitLab Issue Tracker: https://gitlab.unimelb.edu.au/resplat-data/rcs-storage/-/issues
.. _CONTRIBUTING.rst: CONTRIBUTING.rst
.. _change log: CHANGELOG.rst
