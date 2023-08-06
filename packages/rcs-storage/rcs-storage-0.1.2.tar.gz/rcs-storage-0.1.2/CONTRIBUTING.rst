Setup
-----

Git clone this repository::

  git clone git@gitlab.unimelb.edu.au:resplat-data/rcs-storage.git

Install in editable mode (run from repo base directory)::

  python3 -m pip install --editable .

Create a feature branch for your new change::

  git checkout -b my-new-feature

Run a subset of the tests during development::

  tox -e py36,flake8

Merge request
-------------

Run all tests before submitting any merge requests::

  tox

Submit a `merge request`_.


Releasing a new version
-----------------------

1. Ensure tests pass by running ``tox``.
2. Increase the version number in ``setup.py``.
3. Update ``CHANGELOG.rst``.
4. Push changes.
5. Git tag the version.
6. Build dist and upload to PyPi

::

  # Install or update build deps
  python3 -m pip install --user --upgrade setuptools wheel twine
  # Build dist
  python3 setup.py sdist bdist_wheel
  # Upload to PyPi
  python3 -m twine upload --repository pypi dist/*


.. _merge request: https://gitlab.unimelb.edu.au/resplat-data/rcs-storage/-/merge_requests
