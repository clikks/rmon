from rmon.models import Server
from rmon.common.rest import RestException

class TestServer:
    """test Server function
    """

    def test_save(self, db):
        """test Server.save func
        """
        assert Server.query.count() == 0
        server = Server(name='test', host='127.0.0.1')

        server.save()
        assert Server.query.count() == 1

    def test_delete(self, db, server):
        """test Server.delete func
        """

        assert Server.query.count() == 1
        server.delete()
        assert Server.query.count() == 0

    def test_ping_success(self, db, server):
        """test Server.ping func success
         need Redis server listening in 127.0.0.1:6379
        """
        assert server.ping() is True

    def test_ping_failed(self, db):
        """test Server.ping func failed
          when Server.ping func failed, raise RestException ERROR
        """
        server  = Server(name='test', host='127.0.0.1', port=6399)
        try:
            server.ping()
        except RestException as e:
            assert e.code == 400
            assert e.message == 'redis server %s can not connected' % server.host

    def test_get_metrics_success(self, db, server):
        """test Server.get_metrics func success
        need Redis server listening in 127.0.0.1:6379
        """
        assert type(server.get_metrics()) is dict

    def test_get_metrics_failed(self, db):
        server = Server(name='test', host='127.0.0.1', port=6399)
        try:
            server.get_metrics()
        except RestException as e:
            assert e.code == 400
            assert e.message == 'redis server %s can not connected' % server.host

