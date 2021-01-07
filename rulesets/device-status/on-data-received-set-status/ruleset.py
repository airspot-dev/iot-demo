from krules_core.base_functions import *
from krules_core import RuleConst as Const
from datetime import datetime, timezone, timedelta

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
                SetSubjectProperty("status", "ACTIVE"),
                Route(
                    event_type="schedule-message",
                    payload=lambda self:
                    {
                        "event_type": "set-device-status",
                        "subject": str(self.subject),
                        "payload": {
                            "value": "INACTIVE"
                        },
                        "origin_id": self.subject.event_info()["originid"],
                        "when": (datetime.now(timezone.utc) + timedelta(
                            seconds=int(self.subject.rate))).isoformat(),
                        "replace": "schedule_status_uid" in self.subject
                                   and self.subject.schedule_status_uid is not None
                    },
                    dispatch_policy=DispatchPolicyConst.DIRECT
                )
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
]
