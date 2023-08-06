0.1.2 (2020-06-13)
------------------

* Removed ``client.CollectionManager`` methods which were removed from the
  `storage-registry`_ API (``create()`` and ``update()``).
* Renamed ``client.IngestManager`` method to ``upload_storage_report()`` to
  ``upload()`` and deprecated the old method name.
* ``client.ReportManager.usage_by_department`` can now take a date with any
  date format.
* Added new CLI command ``rcs-storage report usage-by-department``.

0.1.1 (2020-06-13)
------------------

* Fixed bug where passing a hostname via the CLI argument ``-h`` did not
  change the actual hostname being used.

0.1.0
-----

First release.


.. _storage-registry: https://gitlab.unimelb.edu.au/resplat-data/storage-registry
