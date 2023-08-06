import os
import sys

import pytest

from rcs_storage.tests import mock_ingest_upload_files

py3only = pytest.mark.skipif(
    sys.version_info < (3, 0), reason="This test requires Python 3"
)


def get_mock_ingest_upload_file(filename):
    dirname = os.path.dirname(mock_ingest_upload_files.__file__)
    return os.path.join(dirname, filename)
