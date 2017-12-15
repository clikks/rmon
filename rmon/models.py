"""rmon.model
implemented all model class
and serialize class
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from rmon.common.rest import RestException
from redis import StrictRedis, RedisError

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




