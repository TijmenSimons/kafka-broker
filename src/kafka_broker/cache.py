import configparser
from uuid import UUID
from .classes import EventObject
from pymemcache.client import base

class Cache:
    def __init__(self, config) -> None:
        self.client = self.innitialize_connection(config)

    def innitialize_connection(self, config):
        client = base.Client(
            (
            config["kafka.cache"]["cache_location"], 
            config["kafka.cache"]["cache_port"]
            )
        )
        if client is not None:
            return client
        else:
            raise Exception("connection could not be innitialized with the cache")

    def add(self, event_object: EventObject):
        return self.client.add(str(event_object.correlation_id), event_object.encode()[1])

    def get(self, correlation_id: UUID):
        raw = self.get_raw(correlation_id)
        return EventObject.decode(raw.decode('utf-8'))
        
    def get_raw(self, correlation_id: UUID):
        return self.client.get(str(correlation_id))

    def delete(self, correlation_id: UUID):
        return self.client.delete(str(correlation_id))
    
    def update(self, event_object: EventObject):
        return self.client.set(str(event_object.correlation_id), event_object.encode())
