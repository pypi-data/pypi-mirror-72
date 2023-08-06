import pytest
import requests

from rcs_storage import client
from rcs_storage.tests.fixtures import mock_response, mock_404_response
from rcs_storage.tests.helpers import get_mock_ingest_upload_file, py3only

MOCK_HOST = 'https://dashboard.storage/'
MOCK_TOKEN = 'mock_token'


def get_client():
    return client.Client(MOCK_HOST, MOCK_TOKEN)


# Tests for :py:func:`client.parse_date` decorator


def test_parse_date_returns_validly_formatted_string():
    for date in (
        '5 Jan 2020', '5/1/2020', '05-01-2020', '5th January 2020',
        '2020-01-05'
    ):
        assert client.parse_date(date) == '2020-01-05'


def test_parse_date_can_parse_month_first_formats():
    for date in (
        'Jan 5 2020', '1/5/2020', '01-05-2020', 'January 5th 2020',
        '2020-01-05'
    ):
        assert client.parse_date(date, dayfirst=False) == '2020-01-05'


# Tests for :py:func:`client.request` decorator


def spy_on_requests_call_collections_get(mocker):
    spy = mocker.spy(requests, 'get')
    storage = get_client()
    storage.collections.get('9770_lab_name')
    return spy


@py3only
def test_request_decorator_used_by_collections_get():
    """Test that :py:func:`client.CollectionManager.get` is decorated by
    :py:func:`client.request` since that method is called to test
    decorator behaviour.
    """
    assert 'request.<locals>' in str(client.CollectionManager.get)


def test_request_decorator_includes_token(mock_response, mocker):
    args, kwargs = spy_on_requests_call_collections_get(mocker).call_args
    assert kwargs['headers']['Authorization'] == 'Token %s' % MOCK_TOKEN


def test_request_decorator_makes_json_request(mock_response, mocker):
    args, kwargs = spy_on_requests_call_collections_get(mocker).call_args
    assert kwargs['headers']['Content-Type'] == 'application/json'


def test_request_decorator_includes_url_with_host(mock_response, mocker):
    args, kwargs = spy_on_requests_call_collections_get(mocker).call_args
    assert kwargs['url'].startswith(MOCK_HOST)


def test_request_decorator_includes_data_as_string(mock_response, mocker):
    args, kwargs = spy_on_requests_call_collections_get(mocker).call_args
    assert isinstance(kwargs['data'], str)


# Tests for :py:class:`client.CollectionManager`


def test_collections_get_returns_dict(mock_response):
    result = get_client().collections.get('9770_lab_name')
    assert isinstance(result, dict)


def test_collections_get_returns_a_collection(mock_response):
    result = get_client().collections.get('9770_lab_name')
    assert result['code'] == '9770_lab_name'


def test_collections_get_raises_DoesNotExist_for_nonexistent_code(
    mock_404_response
):
    with pytest.raises(client.DoesNotExist):
        result = get_client().collections.get('wrong_code')


def test_collections_list_returns_list_of_dicts(mock_response):
    result = get_client().collections.list()
    assert isinstance(result, list)
    assert isinstance(result[0], dict)


def test_collections_list_results_list_of_collections(mock_response):
    result = get_client().collections.list()
    expected_codes = ['9770_lab_name', '2013R9.9', '2019UOM999']
    for collection in result:
        assert collection['code'] in expected_codes


def test_collections_options_returns_dict(mock_response):
    result = get_client().collections.options()
    assert isinstance(result, dict)


def test_collections_options_returns_options(mock_response):
    storage = get_client()
    result = storage.collections.options()
    assert 'application/json' in result['renders']


def test_collections_storage_products_is_list_of_dicts(mock_response):
    result = get_client().collections.storage_products
    assert isinstance(result, list)
    assert isinstance(result[0], dict)


def test_collections_storage_products_is_list_of_storage_products(
    mock_response
):
    result = get_client().collections.storage_products
    expected_storage_products = [
        'Market.Melbourne.Mediaflux', 'Ceph.S3', 'DaRIS', 'NetApp.NFS',
        'NetApp.CIFS'
    ]
    for s_p in result:
        assert s_p['name'] in expected_storage_products


def test_get_request_sources_map_returns_dict_of_lists(mock_response):
    result = get_client().collections.get_request_sources_map()
    assert isinstance(result, dict)
    result_values = [v for v in result.values()]
    assert isinstance(result_values[0], list)


def test_get_request_sources_map_maps_to_collection_codes(mock_response):
    result = get_client().collections.get_request_sources_map()
    assert '9770_lab_name' in result['RITM0000000']


# Tests for :py:class:`client.IngestManager`


def spy_on_requests_call_ingests_upload(mocker):
    spy = mocker.spy(requests, 'post')
    path_to_file = get_mock_ingest_upload_file(
        'Market.Melbourne.Mediaflux_12-Jun-2020.csv'
    )
    storage = get_client()
    storage.ingests.upload(path_to_file)
    return spy


def test_ingests_list_returns_list_of_dicts(mock_response):
    result = get_client().ingests.list()
    assert isinstance(result, list)
    assert isinstance(result[0], dict)


def test_ingests_list_returns_list_of_files(mock_response):
    result = get_client().ingests.list()
    assert 'data' in result[0]
    assert result[0]['data'].startswith('http')


def test_ingests_upload_returns_dict(mock_response):
    path_to_file = get_mock_ingest_upload_file(
        'Market.Melbourne.Mediaflux_12-Jun-2020.csv'
    )
    result = get_client().ingests.upload(path_to_file)
    assert isinstance(result, dict)


def test_ingests_upload_returns_a_file(mock_response):
    path_to_file = get_mock_ingest_upload_file(
        'Market.Melbourne.Mediaflux_12-Jun-2020.csv'
    )
    result = get_client().ingests.upload(path_to_file)
    assert result['data'].startswith('http')


def test_ingests_deprecated_upload_storage_report_returns_a_file(
    mock_response
):
    path_to_file = get_mock_ingest_upload_file(
        'Market.Melbourne.Mediaflux_12-Jun-2020.csv'
    )
    result = get_client().ingests.upload_storage_report(path_to_file)
    assert result['data'].startswith('http')


def test_ingests_upload_includes_file_in_request(mock_response, mocker):
    args, kwargs = spy_on_requests_call_ingests_upload(mocker).call_args
    assert 'files' in kwargs
    assert 'data' in kwargs['files']
    assert kwargs['files']['data'].name.endswith(
        'Market.Melbourne.Mediaflux_12-Jun-2020.csv'
    )


def test_ingests_upload_does_NOT_include_content_type_in_request(
    mock_response, mocker
):
    args, kwargs = spy_on_requests_call_ingests_upload(mocker).call_args
    assert 'Content-Type' not in kwargs['headers']


def test_ingests_upload_makes_request_with_no_verify(mock_response, mocker):
    args, kwargs = spy_on_requests_call_ingests_upload(mocker).call_args
    assert kwargs['verify'] == False


# Tests for :py:class:`client.ReportManager`


def test_reports_usage_by_department_returns_list_of_dicts(mock_response):
    result = get_client().reports.usage_by_department()
    assert isinstance(result, list)
    assert isinstance(result[0], dict)


def test_reports_usage_by_department_returns_list_of_department_codes(
    mock_response
):
    result = get_client().reports.usage_by_department()
    assert 'department' in result[0]


def test_reports_usage_by_department_can_include_date_query(
    mock_response, mocker
):
    spy = mocker.spy(requests, 'get')
    result = get_client().reports.usage_by_department(date='2020-06-12')
    args, kwargs = spy.call_args
    assert ('/?date=2020-06-12' in kwargs['url']
            or '&date=2020-06-12' in kwargs['url'])
