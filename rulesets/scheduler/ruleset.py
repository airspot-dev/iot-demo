from app_functions import DoPostApiCall, DoPutApiCall
from krules_core.base_functions.misc import PyCall
from krules_core.base_functions import *
from krules_core import RuleConst as Const
import requests
from datetime import datetime
from ruleset_functions import DispatchScheduledEvents, call_to_api

#
# try:
#     from ruleset_functions import *
# except ImportError:
#     # for local development
#     from .ruleset_functions import *

rulename = Const.RULENAME
subscribe_to = Const.SUBSCRIBE_TO
ruledata = Const.RULEDATA
filters = Const.FILTERS
processing = Const.PROCESSING

from krules_core.providers import proc_events_rx_factory, subject_factory
from krules_env import publish_proc_events_errors, publish_proc_events_all  # , publish_proc_events_filtered

# proc_events_rx_factory().subscribe(
#     on_next=publish_proc_events_all,
# )
proc_events_rx_factory().subscribe(
    on_next=publish_proc_events_errors,
)

rulesdata = [
    """
    Store schedule info (no replace)
    """,
    {
        rulename: "on-schedule-received-no-replace",
        subscribe_to: "schedule-message",
        ruledata: {
            filters: [
                Filter(lambda payload: not payload.get("replace", False))
            ],
            processing: [
                DoPostApiCall(
                    path="/scheduler/scheduled_event/",
                    json=lambda payload: {
                            "event_type": payload["event_type"],
                            "subject": payload["subject"],
                            "payload": payload["payload"],
                            "origin_id": payload["origin_id"],
                            "when": payload["when"],
                    },
                    on_success=lambda self:
                        lambda ret: self.subject.set("schedule_status_uid", ret.json()["uid"], muted=True)
                ),
            ]
        }
    },
    """
    Update schedule info (replace)
    """,
    {
        rulename: "on-schedule-received-replace",
        subscribe_to: "schedule-message",
        ruledata: {
            filters: [
                Filter(lambda payload: payload.get("replace", True))
            ],
            processing: [
                DoPutApiCall(
                    path=lambda payload: "/scheduler/scheduled_event/%s/" % payload["uid"],
                    json=lambda payload: {
                            "payload": payload["payload"],
                            "when": payload["when"],
                    }
                )
            ]
        }
    },
    """
    On tick route scheduled events
    """,
    {
        rulename: "on-tick-do-schedules",
        subscribe_to: "krules.heartbeat",
        ruledata: {
            processing: [
                DispatchScheduledEvents()
            ]
        }
    },
]
