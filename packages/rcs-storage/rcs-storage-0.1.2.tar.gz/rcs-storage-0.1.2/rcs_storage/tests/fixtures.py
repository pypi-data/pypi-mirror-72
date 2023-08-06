import re

import pytest
import requests

from rcs_storage.tests.mock_api_responses import (
    collections_get,
    collections_list,
    collections_options,
    ingests_list,
    ingests_post,
    reports_usage_by_department,
    storage_products
)


def get_error_message(method, url):
    return (
        "Unknown API endpoint called: %s %s. If this endpoint "
        "is supposed to exist, please update the "
        "'mock_response' test fixture."
        % (method, url)
    )


def get_url(*args, **kwargs):
    """Determine URL based on args and kwargs passed on a requests method"""
    if args:
        return args[0]
    return kwargs.get('url')


class MockResponse(object):
    status_code = 200

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def json(self):
        return self._json


@pytest.fixture
def mock_response(monkeypatch):
    """Provide mock responses for API requests against a test database
    that contains three collections:
    * 9770_lab_name
    * 2013R9.9
    * 2019UOM999
    """

    def mock_get(*args, **kwargs):
        # URL is either a kwarg or the first arg
        url = get_url(*args, **kwargs)
        # Return response based on URL provided
        if re.search(r'/api/collections/$', url):
            return MockResponse(content=collections_list.content,
                                _json=collections_list.json)
        elif re.search(r'/api/collections/(.*?)/$', url):
            return MockResponse(content=collections_get.content,
                                _json=collections_get.json)
        elif re.search(r'/ingest/upload/$', url):
            return MockResponse(content=ingests_list.content,
                                _json=ingests_list.json)
        elif re.search(
            r'/api/reports/usage-by-department/(.*?)$', url
        ):
            return MockResponse(content=reports_usage_by_department.content,
                                _json=reports_usage_by_department.json)
        elif re.search(r'/api/storage_products/$', url):
            return MockResponse(content=storage_products.content,
                                _json=storage_products.json)
        else:
            raise AssertionError(get_error_message('GET', url))

    def mock_options(*args, **kwargs):
        # URL is either a kwarg or the first arg
        url = get_url(*args, **kwargs)
        # Return response based on URL provided
        if re.search(r'/api/collections/$', url):
            return MockResponse(content=collections_options.content,
                                _json=collections_options.json)
        else:
            raise AssertionError(get_error_message('OPTIONS', url))

    def mock_post(*args, **kwargs):
        # URL is either a kwarg or the first arg
        url = get_url(*args, **kwargs)
        # Return response based on URL provided
        if re.search(r'/ingest/upload/$', url):
            return MockResponse(content=ingests_post.content,
                                _json=ingests_post.json)
        else:
            raise AssertionError(get_error_message('POST', url))

    monkeypatch.setattr(requests, "get", mock_get)
    monkeypatch.setattr(requests, "options", mock_options)
    monkeypatch.setattr(requests, "post", mock_post)


@pytest.fixture
def mock_404_response(monkeypatch):

    def mock_get(*args, **kwargs):
        return MockResponse(status_code=404)

    monkeypatch.setattr(requests, "get", mock_get)
