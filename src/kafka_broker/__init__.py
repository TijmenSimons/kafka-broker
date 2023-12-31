import logging

from typing import Any, Callable
from confluent_kafka import Consumer

from .cache import Cache
from .classes import ConsumerStorage, EventObject, EventRouter
from .consumer import init_consumer, initialize, consume
from .producer import default_callback, produce
from .config import get_config


class BrokerManager:
    consumer_storage: ConsumerStorage
    cache: Cache

    def __init__(self) -> None:
        """Produce to and consume from a kafka message queue."""
        
        filename = "broker_config.ini"

        self.consumer = None
        self.config = get_config(filename)

        log_level = self.config["logging"]["log_level"]
        logging.basicConfig(format="%(levelname)s:\t%(message)s", level=int(log_level))

        self.logger = logging.getLogger("kafka_broker_logger")

        self.consumer_storage = ConsumerStorage()
        self.cache = Cache(self.config, self.logger)

    def produce(
        self,
        topic: str,
        event_object: EventObject | Any,
        callback: Callable = default_callback,
    ):
        """Send a message to the broker.

        Parameters
        ----------
        topic : str
            Defines the topic the message will be sent to.

        event_object : EventObject | any
            The object/message to be sent.

        callback : Callable, default=`default_callback`
            Function to call when having sent the message.

        Returns
        -------
        None

        Description
        -----------

        ## EventObject
        When the producer sends a message to the broker, it tries to
        encode it. If provided in the config, the custom encode function
        must return a key and value pair in the form of a tuple.
        """
        produce(self.config, self.cache, self.logger, topic, event_object, callback)

    def consume(self):
        if not self.consumer:
            kafka_config = self.config["kafka.default"]
            kafka_config.update(self.config["kafka.consumer"])
            self.consumer = Consumer(kafka_config)
            self.consumer.subscribe([self.config["general"]["current_location"]])
        return consume(self.consumer, self.logger)

    def init_consumer_app(self, app):
        """Setup the consumer on a FastAPI instance.

        Parameters
        ----------
        app : FastAPI
            The FastAPI app.

        Returns
        -------
        app : FastAPI
            The edited FastAPI app.

        Description
        -----------

        ### Consuming
        This sets up 2 listeners on the FastAPI app:
        One on startup, and one on shutdown.
        Both of these respectively start and shutdown the consumer.

        The consumer runs in a seperate process, because of this we
        set up a pipe between this main process and the new sub-process.
        Whenever the consumer receives data, it will send this date
        through this pipe to be received in this process.

        Now we can't directly use this pipe to access the data as
        we'd have to wait for data to be receive and we can't be
        doing as such constantly.
        For this we have ConsumerStorage setup.

        ### ConsumerStorage
        In the ConsumerStorage we store all consumed messages in
        a dictionary, with the correlation_id as key.
        So when wanting to pick up data from the ConsumerStorage
        you can call `.consume(key)` as an all in one function.
        This will wait until a message appears with the key provided.

        Additionally you can call `.poll()` to check for new messages
        or `.get(key)` to retrieve messages.
        TIP: when manually retrieving
        messages from the ConsumerStorage, make sure to call `.remove(key)`
        to not have persisting data which takes up memory.

        ### EventObject
        In the config you can define a custome decode function.
        When the consumer receives a message from the broker it tries
        to decode the message before sending it to the ConsumerStorage.
        """
        app, consumer_storage = init_consumer(self.config, self.logger, self.consumer_storage, app)
        self.consumer_storage = consumer_storage
        return app

    def init_consumer(self):
        consuming, consumer_storage = initialize(self.config, self.logger, self.consumer_storage)
        self.consumer_storage = consumer_storage
        return consuming


broker_manager = BrokerManager()

__all__ = [
    "broker_manager",
    "BrokerManager",
    "ConsumerStorage",
    "EventObject",
    "EventRouter",
    "Cache"
]
