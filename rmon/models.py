"""rmon.model
implemented all model class
and serialize class
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from rmon.common.rest import RestException
from redis import StrictRedis, RedisError
from marshmallow import (Schema, fields, validate, post_load, validates_schema, ValidationError)

db = SQLAlchemy()


class Server(db.Model):
    """Redis Server model
    """

    __tablename__ = 'redis_server'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(512))
    host = db.Column(db.String(15))
    port = db.Column(db.Integer, default=6379)
    password = db.Column(db.String())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Server(name=%s)>' % self.name

    def save(self):
        """ Save to database
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete from database
        """
        db.session.delete(self)
        db.session.commit()

    @property
    def redis(self):
        return StrictRedis(host=self.host, port=self.port, password=self.password)
    
    def ping(self):
        """check whether Redis server can be accessed
        """
        try:
            return self.redis.ping()
        except RedisError:
            raise RestException(400, 'redis server %s can not connected' % self.host)

    def get_metrics(self):
        """get Redis server monitor info
        from Redis server command 'INFO',return monitor info.
        reference https://redis.io/commands/INFO
        """
        try:
            return self.redis.info()
        except RedisError:
            raise RestException(400, 'redis server %s can not connected' % self.host)


class ServerSchema(Schema):
    """Redis server record serialize class
    """

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(2, 64))
    description = fields.String(validate=validate.Length(0,512))
    # host must ipv4 format, use regular verification
    host = fields.String(required=True, validate=validate.Regexp(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'))
    port = fields.Integer(validate=validate.Range(1024,65536))
    password = fields.String()
    updated_at = fields.DateTime(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

    @validates_schema
    def validate_schema(self, data):
        """verification if there is a same name of Redis server
        """
        if 'port' not in data:
            data['port'] = 6379

        instance = self.context.get('instance', None)
        #print(instance)
        #print(self.context)
        server = Server.query.filter_by(name=data['name']).first()
        
        if server is None:
            return

        # update server time
        if instance is not None and server != instance:
            raise ValidationError('Redis server already exist', 'name')

        # create server time
        if instance is None and server :
            raise ValidationError('Redis server already exist', 'name')

    @post_load
    def create_or_update(self, data):
        """after data load success, create Server object
        """
        instance = self.context.get('instance', None)
        #print(instance) 
        # create Redis server
        if instance is None:
            return Server(**data)

        # update server
        for key in data:
            setattr(instance, key, data[key])
        return instance

