import base64

from krules_core.base_functions import *
from krules_core import RuleConst as Const

rulename = Const.RULENAME
subscribe_to = Const.SUBSCRIBE_TO
ruledata = Const.RULEDATA
filters = Const.FILTERS
processing = Const.PROCESSING

from krules_core.providers import proc_events_rx_factory
from krules_env import publish_proc_events_errors, publish_proc_events_all  #, publish_proc_events_filtered

proc_events_rx_factory().subscribe(
  on_next=publish_proc_events_all,
)
# proc_events_rx_factory().subscribe(
#  on_next=publish_proc_events_errors,
# )
from app_functions import hashed
from k8s_functions import K8sObjectCreate, K8sObjectsQuery

from ruleset_functions import SetSecretName

IMAGE_DIGEST = 'lorenzocampo/device_endpoint@sha256:99212a0673ee9913d9c9e8f82c5dbb994f2bd54869ae0c1f3b3866ae93af52f0'

rulesdata = [
    """
    On new fleet create secret
    """,
    {
        rulename: "on-new-fleet-create-service",
        subscribe_to: ["django.orm.post_save"],
        ruledata: {
            filters: [
                Filter(
                    lambda payload:
                        payload.get("signal_kwargs", {}).get("created", False)
                )
            ],
            processing: [
                SetSecretName("secret_name"),
                SetPayloadProperty("labels", lambda payload: (
                    eval(payload.get("data").get("cluster_local")) and {
                        "serving.knative.dev/visibility": "cluster-local"
                    } or {}
                )),
                K8sObjectsQuery(
                    apiversion="eventing.knative.dev/v1",
                    kind="Broker",
                    returns=lambda payload: lambda objs: (
                        payload.setdefault("k_sink", objs.get(name="data-received").obj["status"]["address"]["url"])
                    )
                ),
                K8sObjectCreate(lambda payload: {
                    "apiVersion": "v1",
                    "kind": "Secret",
                    "type": "Opaque",
                    "metadata": {
                        "name": payload["secret_name"],
                        "labels": {
                            "app.krules.airspot.dev/owned-by": payload["data"]["name"]
                        }
                    },
                    "data": {
                        "api_key": base64.b64encode(payload["data"]["api_key"].encode("utf-8")).decode("utf-8")
                    }
                }),
                K8sObjectCreate(lambda payload: {
                    "apiVersion": "serving.knative.dev/v1",
                    "kind": "Service",
                    "metadata": {
                        "labels": {**{"demo.krules.airspot.dev/app": "fleet-endpoint"}, **payload.get("labels")},
                        "name": payload["data"]["name"],
                    },
                    "spec": {
                        "template": {
                            "metadata": {
                                "name": payload["secret_name"]
                            },
                            "spec": {
                                "containers": [{
                                    "image": IMAGE_DIGEST,
                                    "env": [
                                        {
                                            "name": "K_SINK",
                                            "value": payload["k_sink"],
                                        },
                                        {
                                            "name": "API_KEY",
                                            "valueFrom": {
                                                "secretKeyRef": {
                                                    "name": payload["secret_name"],
                                                    "key": "api_key"
                                                }
                                            }
                                        }
                                    ]
                                }]
                            }
                        }
                    }

                })
            ]
        }
    },
    """
    On fleet update (manage api_key and cluster-local)
    """,
    {
        rulename: "on-update-fleet-update-service",
        subscribe_to: ["django.orm.post_save"],
        ruledata: {
            filters: [
                Filter(
                    lambda payload:
                    not payload.get("signal_kwargs", {}).get("created", False)
                )
            ],
            processing: [
                # set the expected secret name
                SetSecretName("secret_name"),
            ],
        }
    },
]

