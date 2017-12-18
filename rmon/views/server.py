# -*- coding: utf-8 -*-

from flask import request, g
from rmon.common.rest import RestView
from rmon.models import Server, ServerSchema
from rmon.common.decorators import ObjectMustBeExist

class ServerList(RestView):
    # Redis 服务器列表
    def get(self):
        # 获取 Redis 列表

        servers =Server.query.all()
        return ServerSchema().dump(servers, many=True).data

    def post(self):
        # 创建 Redis 服务器
        
        data = request.get_json()
        server, errors = ServerSchema().load(data)
        if errors:
            return errors, 400
        server.ping()
        server.save()
        return {'ok':True}, 201


class ServerDetail(RestView):
    """ Redis servers list
    """
    
    method_decorators = (ObjectMustBeExist(Server),)
    def get(self, object_id):
        data, _ = ServerSchema().dump(g.instance)
        return data

    def put(self, object_id):
        """update server
        """
        schema = ServerSchema(context={'instance':g.instance})
        data = request.get_json()
        server, errors = schema.load(data, partial=True)

        if errors:
            return errors, 400
        server.save()
        return {'ok': True}

    def delete(self, object_id):
        """delete server
        """
        g.instance.delete()
        return {'ok': True}, 204


