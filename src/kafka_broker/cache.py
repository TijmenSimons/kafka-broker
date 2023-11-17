import configparser
from .classes import EventObject
from pymemcache.client import base

class Cache:
    def __init__(self, config) -> None:
        self.client = self.innitialize_connection(config)

    def innitialize_connection(self, config):
        print(config)
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

    def cache_item(self, event_object: EventObject):
        self.client.add(event_object.correlation_id, event_object.data)
        return event_object.correlation_id

    def get_cache_item(self, event_object: EventObject):
        self.client.get(event_object.correlation_id)
        return event_object.correlation_id

    def delete_cache_item(self, event_object: EventObject):
        self.client.delete(event_object.correlation_id)
        return event_object.correlation_id
