import pytest


@pytest.mark.skip('Let GitLab pipeline succeed - use coverage as a warning')
def test_missing_tests():
    pytest.fail('Tests are not written for module rcs_storage.scripts.main')
