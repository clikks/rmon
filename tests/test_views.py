import json
from flask import url_for

from rmon.models import Server


class TestServerList:
    #���� Redis �������б�API
    

    endpoint = 'api.server_list'

    def test_get_servers(self, server, client):
        #��ȡ Redis �������б�
        
        resp = client.get(url_for(self.endpoint))
        # RestView ��ͼ��������� HTTP ͷ��Content-Type Ϊ json
        assert resp.headers['Content-type'] == 'application/json; charset=utf-8'
        # ���ʳɹ��󷵻�״̬�� 200 OK
        assert resp.status_code == 200
        servers = resp.json

        # ���ڲ��Ի���ֻ��һ�� Redis �����������Է��ص�����Ϊ1
        assert len(servers) == 1

        h = servers[0]
        assert h['name'] == server.name
        assert h['description'] == server.description
        assert h['host'] == server.host
        assert h['port'] == server.port
        assert 'updated_at' in h
        assert 'created_at' in h

    def test_create_server_success(self, db, client):
        #���Դ��� Redis �������ɹ�
        
        data = {'name':'test2','description':'redis server','host':'127.0.0.1'}
        resp = client.post(url_for(self.endpoint),data=json.dumps(data),
                           content_type='application/json')
        assert resp.status_code == 201
        assert resp.headers['Content-type'] == 'application/json; charset=utf-8'
        assert resp.json == {'ok': True}

        assert Server.query.count() == 1
        server = Server.query.first()
        assert server is not None
        for key in data:
            assert getattr(server, key) == data[key]

    def test_create_server_failed_with_invalid_host(self, db, client):
        data = {'name':'test3','description':'redis server','host':'127.0.0.2'}
        resp = client.post(url_for(self.endpoint),data=json.dumps(data),
                           content_type='application/json')
        assert resp.status_code == 400
        assert resp.headers['Content-type'] == 'application/json; charset=utf-8'
        assert resp.json == {'ok': False,
                'message': 'redis server %s can not connected' % data['host']}
        assert Server.query.count() == 0
    
    def test_create_server_failed_with_duplciate_server(self, server, client):
        data = {'name':'test3','description':'redis server','host':'127.0.0.1'}
        client.post(url_for(self.endpoint), data=json.dumps(data),
                content_type='application/json')
        resp = client.post(url_for(self.endpoint), data=json.dumps(data),
                content_type='application/json')
        assert resp.status_code == 400
        assert resp.headers['Content-type'] == 'application/json; charset=utf-8'
        assert resp.json == {'ok':False, 
                'message':'Redis server already exist'}
        #assert Server.query.all() == False
        assert Server.query.count() == 2

class TestServerDetail:
    # ���� Rides ���������� API
    endpoint = 'api.server_detail'
   
    def test_get_server_success(self, server, client):
        # ���Ի�ȡ Redis ����������
        pass

    def test_get_server_failed(self, db, client):
        # ��ȡ�����ڵ� Redis ����������ʧ��
        pass

    def test_update_server_success(self, server, client):
        # ���� Redis �������ɹ�

        pass

    def test_update_server_success_with_duplicate_server(self, server, client):
        # ���·���������Ϊ����ͬ������������ʱʧ��

        pass

    def test_delete_success(self, server, client):
        # ɾ�� Rides �������ɹ�
        
        pass

    def test_delete_failed_with_host_not_exist(self, server, db, client):
        # ɾ�������ڵ� Redis ������ʧ��

        pass
