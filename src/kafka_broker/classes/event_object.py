import json
from datetime import datetime
import uuid


class EventObject:
    def __init__(
        self,
        correlation_id: int = None,
        event: str = None,
        data: dict[any] = None,
        audit_log: list[dict[str, int, int]] = None,
    ) -> None:
        """Initialize the EventObject:

        Parameters
        ----------
        correlation_id : int
            Event intentifier

        event : str
            Event action

        data : any
            payload

        audit_log : list[dict[str, int, int]]
            Places this object has been
        """
        if not correlation_id:
            correlation_id = uuid.uuid4()
        self.correlation_id = correlation_id

        if not event:
            event = "base.event"
        self.event = event

        if not data:
            data = {}
        self.data = data

        if not audit_log:
            audit_log = []
        self.audit_log = audit_log

    def encode(self):
        result = {
            "correlation_id": self.correlation_id,
            "event": self.event,
            "data": self.data,
            "audit_log": self.audit_log,
        }
        
        result = json.dumps(result)
        return self.correlation_id, result

    def decode(value):
        data = json.loads(value)

        self = EventObject()

        self.correlation_id = data.get("correlation_id")
        self.event = data.get("event")
        self.data = data.get("data")
        self.audit_log = data.get("audit_log")

        return self

    def add_audit_log(self, location):
        self.audit_log.append(
            {
                "data": self.data.copy(),
                "event": self.event,
                "location": location,
                "time_sent": int(datetime.now().timestamp()),
                "time_received": None,
            }
        )

    def update_audit_log(self):
        cur_location = self.audit_log[-1]
        cur_location["time_received"] = int(datetime.now().timestamp())
