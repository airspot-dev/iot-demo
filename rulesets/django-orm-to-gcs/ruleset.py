
from krules_core.base_functions import *
from krules_core import RuleConst as Const
import os

rulename = Const.RULENAME
subscribe_to = Const.SUBSCRIBE_TO
ruledata = Const.RULEDATA
filters = Const.FILTERS
processing = Const.PROCESSING

from krules_core.providers import proc_events_rx_factory, configs_factory
from krules_env import publish_proc_events_all

from ruleset_functions import CreateFleetGCSFolder

proc_events_rx_factory().subscribe(
  on_next=publish_proc_events_all,
)

with open("google-cloud-key.json", "w") as f:
    f.write(configs_factory()["google-cloud"]["credentials"]["key.json"])
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.abspath(f.name)

rulesdata = [
    """
    Rule description here..
    """,
    {
        rulename: "on-fleet-model-creation-create-gcs-folders",
        subscribe_to: ["django.orm.post_save"],
        ruledata: {
            filters: [
                Filter(
                    lambda payload:
                        payload["signal_kwargs"]["created"]
                )
            ],
            processing: [
                CreateFleetGCSFolders(
                    bucket="iot-demo-01",
                    fleet=lambda payload: payload["data"]["name"]
                )
            ]
        }
    },
]

