
name = "on-data-received-set-status"

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
    "configs.krules.airspot.dev/django-restapi-consumer": "inject",
    "krules.airspot.dev/ruleset": name
}

template_annotations = {
    #"autoscaling.knative.dev/minScale": "0",
}

#service_account = "my-service-account"

triggers = (
   {
       "name": name,
       "filter": {
           "attributes": {
               "type": "subject-property-changed",
               "phase": "running",
           }
       }
   },
   {
       "name": "%s-inactive" % name,
       "filter": {
           "attributes": {
               "type": "set-device-status",
           }
       },
   }
)
triggers_default_broker = "default"

ksvc_sink = "broker:default"
ksvc_procevents_sink = "broker:procevents"

