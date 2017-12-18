import json
from flask import url_for

from rmon.models import Server


class TestServerList:
    #测试 Redis 服务器列表API
    

    endpoint = 'api.server_list'

    def test_get_servers(self, server, client):
        #获取 Redis 服务器列表
        
        resp = client.get(url_for(self.endpoint))
        # RestView 视图基类会设置 HTTP 头部Content-Type 为 json
        assert resp.headers['Content-type'] == 'application/json; charset=utf-8'
        # 访问成功后返回状态码 200 OK
        assert resp.status_code == 200
        servers = resp.json

        # 由于测试环境只有一个 Redis 服务器，所以返回的数量为1
        assert len(servers) == 1

        h = servers[0]
        assert h['name'] == server.name
        assert h['description'] == server.description
        assert h['host'] == server.host
        assert h['port'] == server.port
        assert 'updated_at' in h
        assert 'created_at' in h

    def test_create_server_success(self, db, client):
        #测试创建 Redis 服务器成功
        
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
    # 测试 Rides 服务器详情 API
    endpoint = 'api.server_detail'
   
    def test_get_server_success(self, server, client):
        # 测试获取 Redis 服务器详情
        pass

    def test_get_server_failed(self, db, client):
        # 获取不存在的 Redis 服务器详情失败
        pass

    def test_update_server_success(self, server, client):
        # 更新 Redis 服务器成功

        pass

    def test_update_server_success_with_duplicate_server(self, server, client):
        # 更新服务器名称为其他同名服务器名称时失败

        pass

    def test_delete_success(self, server, client):
        # 删除 Rides 服务器成功
        
        pass

    def test_delete_failed_with_host_not_exist(self, server, db, client):
        # 删除不存在的 Redis 服务器失败

        pass
