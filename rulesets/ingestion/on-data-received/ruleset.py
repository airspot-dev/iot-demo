from krules_core.base_functions import *
from krules_core import RuleConst as Const
from datetime import datetime, timezone, timedelta
from app_functions import DoPostApiCall
from uuid import uuid4

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

from krules_core.providers import proc_events_rx_factory
from krules_env import publish_proc_events_errors, publish_proc_events_all  # , publish_proc_events_filtered
from krules_core.event_types import SUBJECT_PROPERTY_CHANGED

# proc_events_rx_factory().subscribe(
#   on_next=publish_proc_events_all,
# )
proc_events_rx_factory().subscribe(
    on_next=publish_proc_events_errors,
)

rulesdata = [

    """
    On data received we just set a "lastSeen" property allowing reacting for changing status
    """,
    {
        rulename: "on-data-received-set-lastseen",
        subscribe_to: "data-received",
        ruledata: {
            processing: [
                SetSubjectProperty("lastSeen", lambda: datetime.now(timezone.utc).isoformat()),
            ]
        }
    },
    """
    When a subject property (except for status) changes, sets status to active
    """,
    {
        rulename: "on-property-update-set-status-active",
        subscribe_to: [SUBJECT_PROPERTY_CHANGED],
        ruledata: {
            filters: [
                Filter(lambda payload: payload["property_name"] != "status")
            ],
            processing: [
                SetSubjectProperty("status", "ACTIVE", use_cache=False),
                DoPostApiCall(
                    path="/scheduler/scheduled_event/",
                    json=lambda subject: {
                        "uid": str(getattr(subject, "schedule_status_uid", uuid4())),
                        "event_type": "set-device-status",
                        "subject": subject.name,
                        "payload": {
                            "value": "INACTIVE"
                        },
                        "origin_id": subject.event_info()["originid"],
                        "when": (datetime.now(timezone.utc) + timedelta(
                            seconds=int(subject.rate))).isoformat(),
                    },
                    on_success=lambda self:
                    lambda ret: self.subject.set("schedule_status_uid", ret.json()["uid"], muted=True),
                    raise_on_error=False
                ),
            ]
        }
    },

    """
    Set device status, used to set INACTIVE by the scheduler
    """,
    {
        rulename: 'on-set-device-status',
        subscribe_to: "set-device-status",
        ruledata: {
            processing: [
                SetSubjectProperty("status", lambda payload: payload["value"])
            ]
        }
    },

    """
    Since we have already intercepted the subject property changed event inside the container we need to send it out 
    explicitly
    """,
    {
        rulename: "device-status-propagate",
        subscribe_to: SUBJECT_PROPERTY_CHANGED,
        ruledata: {
            filters: [
                Filter(lambda payload: payload["property_name"] == "status")
            ],
            processing: [
                Route(dispatch_policy=DispatchPolicyConst.DIRECT)
            ]
        },
    },
]
