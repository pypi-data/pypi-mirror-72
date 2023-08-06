import socket
from unittest.mock import patch, Mock

try:
    import cPickle as pickle
except ImportError:
    import pickle


from django.core.cache import InvalidCacheBackendError
from nose.tools import (
    eq_,
    raises,
)


@raises(InvalidCacheBackendError)
def test_multiple_servers():
    from django_elastipymemcache.memcached import (
        ElastiPyMemCache,
    )
    ElastiPyMemCache('h1:0,h2:0', {})


@raises(InvalidCacheBackendError)
def test_wrong_server_format():
    from django_elastipymemcache.memcached import (
        ElastiPyMemCache,
    )
    ElastiPyMemCache('h', {})


@patch('django_elastipymemcache.memcached.get_cluster_info')
def test_split_servers(get_cluster_info):
    from django_elastipymemcache.memcached import (
        ElastiPyMemCache,
        deserialize_pickle,
        serialize_pickle,
    )
    backend = ElastiPyMemCache('h:0', {})
    servers = [('h1', 0), ('h2', 0)]
    get_cluster_info.return_value = {
        'nodes': servers
    }
    backend._lib.Client = Mock()
    assert backend._cache
    get_cluster_info.assert_called_once_with(
            'h', '0', False, socket._GLOBAL_DEFAULT_TIMEOUT)
    backend._lib.Client.assert_called_once_with(
        servers,
        deserializer=deserialize_pickle,
        ignore_exc=True,
        serializer=serialize_pickle
    )


@patch('django_elastipymemcache.memcached.get_cluster_info')
def test_node_info_cache(get_cluster_info):
    from django_elastipymemcache.memcached import (
        ElastiPyMemCache,
        deserialize_pickle,
        serialize_pickle,
    )
    servers = [('h1', 0), ('h2', 0)]
    get_cluster_info.return_value = {
        'nodes': servers
    }

    backend = ElastiPyMemCache('h:0', {})
    backend._lib.Client = Mock()
    backend.set('key1', 'val')
    backend.get('key1')
    backend.set('key2', 'val')
    backend.get('key2')
    backend._lib.Client.assert_called_once_with(
        servers,
        deserializer=deserialize_pickle,
        ignore_exc=True,
        serializer=serialize_pickle
    )
    eq_(backend._cache.get.call_count, 2)
    eq_(backend._cache.set.call_count, 2)

    get_cluster_info.assert_called_once_with(
            'h', '0', False, socket._GLOBAL_DEFAULT_TIMEOUT)


@patch('django_elastipymemcache.memcached.get_cluster_info')
def test_failed_to_connect_servers(get_cluster_info):
    from django_elastipymemcache.memcached import ElastiPyMemCache
    backend = ElastiPyMemCache('h:0', {})
    get_cluster_info.side_effect = OSError()
    eq_(backend.get_cluster_nodes(), [])


@patch('django_elastipymemcache.memcached.get_cluster_info')
def test_invalidate_cache(get_cluster_info):
    from django_elastipymemcache.memcached import ElastiPyMemCache
    servers = [('h1', 0), ('h2', 0)]
    get_cluster_info.return_value = {
        'nodes': servers
    }

    backend = ElastiPyMemCache('h:0', {})
    backend._lib.Client = Mock()
    assert backend._cache
    backend._cache.get = Mock()
    backend._cache.get.side_effect = Exception()
    try:
        backend.get('key1', 'val')
    except Exception:
        pass
    #  invalidate cached client
    container = getattr(backend, '_local', backend)
    container._client = None
    try:
        backend.get('key1', 'val')
    except Exception:
        pass
    eq_(backend._cache.get.call_count, 2)
    eq_(get_cluster_info.call_count, 3)


@patch('django_elastipymemcache.memcached.get_cluster_info')
def test_client_get_many(get_cluster_info):
    from django_elastipymemcache.memcached import ElastiPyMemCache

    servers = [('h1', 0), ('h2', 0)]
    get_cluster_info.return_value = {
        'nodes': servers
    }

    backend = ElastiPyMemCache('h:0', {})
    ret = backend.get_many(['key1'])
    eq_(ret, {})

    # When server does not found...
    with patch('pymemcache.client.hash.HashClient._get_client') as p:
        p.return_value = None
        ret = backend.get_many(['key2'])
        eq_(ret, {})

    with patch('pymemcache.client.hash.HashClient._safely_run_func') as p2:
        p2.return_value = {
            ':1:key3': 1509111630.048594
        }

        ret = backend.get_many(['key3'])
        eq_(ret, {'key3': 1509111630.048594})

    # If False value is included, ignore it.
    with patch('pymemcache.client.hash.HashClient.get_many') as p:
        p.return_value = {
            ':1:key1': 1509111630.048594,
            ':1:key2': False,
            ':1:key3': 1509111630.058594,
        }
        ret = backend.get_many(['key1', 'key2', 'key3'])
        eq_(
            ret,
            {
                'key1': 1509111630.048594,
                'key3': 1509111630.058594
            },
        )

    with patch('pymemcache.client.hash.HashClient.get_many') as p:
        p.return_value = {
            ':1:key1': None,
            ':1:key2': 1509111630.048594,
            ':1:key3': False,
        }
        ret = backend.get_many(['key1', 'key2', 'key3'])
        eq_(
            ret,
            {
                'key2': 1509111630.048594,
            },
        )


@patch('django_elastipymemcache.memcached.get_cluster_info')
def test_client_set_many(get_cluster_info):
    from django_elastipymemcache.memcached import ElastiPyMemCache

    servers = [('h1', 0), ('h2', 0)]
    get_cluster_info.return_value = {
        'nodes': servers
    }

    backend = ElastiPyMemCache('h:0', {})
    ret = backend.set_many({'key1': 'value1', 'key2': 'value2'})
    eq_(ret, ['key1', 'key2'])


@patch('django_elastipymemcache.memcached.get_cluster_info')
def test_client_delete(get_cluster_info):
    from django_elastipymemcache.memcached import ElastiPyMemCache

    servers = [('h1', 0), ('h2', 0)]
    get_cluster_info.return_value = {
        'nodes': servers
    }

    backend = ElastiPyMemCache('h:0', {})
    ret = backend.delete('key1')
    eq_(ret, None)


@patch('django_elastipymemcache.memcached.get_cluster_info')
def test_client_delete_many(get_cluster_info):
    from django_elastipymemcache.memcached import ElastiPyMemCache

    servers = [('h1', 0), ('h2', 0)]
    get_cluster_info.return_value = {
        'nodes': servers
    }

    backend = ElastiPyMemCache('h:0', {})
    ret = backend.delete_many(['key1', 'key2'])
    eq_(ret, None)


def test_serialize_pickle():
    from django_elastipymemcache.memcached import serialize_pickle
    eq_(serialize_pickle('key', 'str'), ('str', 1))
    eq_(serialize_pickle('key', 0), (pickle.dumps(0), 2))


def test_deserialize_pickle():
    from django_elastipymemcache.memcached import deserialize_pickle
    eq_(deserialize_pickle('key', 'str', 1), 'str')
    eq_(deserialize_pickle('key', pickle.dumps(0), 2), 0)
