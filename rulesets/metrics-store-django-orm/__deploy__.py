
name = "metrics-store-django-orm"

add_files = (
    "ruleset.py",
)

add_modules = True  # find modules in directory (folders having __init__.py file) and add them to container

extra_commands = (
#    ("RUN", "pip install my-wonderful-lib==1.0")
)

labels = {
    "serving.knative.dev/visibility": "cluster-local",
    "krules.airspot.dev/type": "ruleset",
    "configs.krules.airspot.dev/django-restapi-consumer": "inject"
}

template_annotations = {
    #"autoscaling.knative.dev/minScale": "0",
}

#service_account = "my-service-account"

triggers = (
#    {
#        "name": "test-trigger",
#        # broker: "my-broker"
#        "filter": {
#            "attributes": {
#                "type": "my-type"
#                # ...
#            }
#        }
#    },
#    ...
)
triggers_default_broker="default"

ksvc_sink = "broker:default"
ksvc_procevents_sink = "broker:procevents"

