from app_functions import WebsocketDevicePublishMessage, WebsocketNotificationEventClass
from krules_core.base_functions import *
from krules_core import RuleConst as Const
from krules_core.event_types import SUBJECT_PROPERTY_CHANGED

from krules_core.providers import proc_events_rx_factory
from krules_env import publish_proc_events_errors, publish_proc_events_all  #, publish_proc_events_filtered


rulename = Const.RULENAME
subscribe_to = Const.SUBSCRIBE_TO
ruledata = Const.RULEDATA
filters = Const.FILTERS
processing = Const.PROCESSING

DEVICE_DATA = "device-data"


# proc_events_rx_factory().subscribe(
#   on_next=publish_proc_events_all,
# )
proc_events_rx_factory().subscribe(
 on_next=publish_proc_events_errors,
)

rulesdata = [
    """
    Notify ACTIVE
    """,
    {
        rulename: "on-device-active-notify-websocket",
        subscribe_to: [SUBJECT_PROPERTY_CHANGED],
        ruledata: {
            filters: [
                Filter(lambda payload: payload.get("value") == "ACTIVE")
            ],
            processing: [
                WebsocketDevicePublishMessage(
                    channel=lambda subject: subject.get_ext("fleet"),
                    event=DEVICE_DATA,
                    data=lambda self:{
                        # "device_class": self.subject.get_ext("deviceclass"),
                        "status": self.payload["value"],
                        "event": "Receiving data",
                        "event_class": WebsocketNotificationEventClass.NORMAL,
                    }
                )
            ]
        }
    },
    """
    Notify INACTIVE
    """,
    {
        rulename: "on-device-inactive-notify-websocket",
        subscribe_to: [SUBJECT_PROPERTY_CHANGED],
        ruledata: {
            filters: [
                Filter(lambda payload: payload.get("value") == "INACTIVE")
            ],
            processing: [
                WebsocketDevicePublishMessage(
                    channel=lambda subject: subject.get_ext("fleet"),
                    event=DEVICE_DATA,
                    data=lambda self:{
                        # "device_class": self.subject.get_ext("deviceclass"),
                        "status": self.payload["value"],
                        "event": "No more data receiving",
                        "event_class": WebsocketNotificationEventClass.WARNING,
                    }
                )
            ]
        }
    },
]

