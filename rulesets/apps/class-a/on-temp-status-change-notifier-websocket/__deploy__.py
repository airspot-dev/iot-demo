
name = "on-temp-status-change-notifier-websocket"

add_files = (
    "ruleset.py",
)

add_modules = True  # find modules in directory (folders having __init__.py file) and add them to container

extra_commands = (
#    ("RUN", "pip install my-wonderful-lib==1.0")
)

labels = {
    "networking.knative.dev/visibility": "cluster-local",
    "krules.airspot.dev/type": "ruleset",
    "krules.airspot.dev/ruleset": name,
    "configs.krules.airspot.dev/pusher": "inject"
}

template_annotations = {
    "autoscaling.knative.dev/minScale": "1",
}

#service_account = "my-service-account"

triggers = (
   {
       "name": "class-a-%s-tempc-change" % name,
       "filter": {
           "attributes": {
               "type": "subject-property-changed",
               "phase": "running",
               "subjecttype": "device",
               "propertyname": "tempc"
           }
       }
   },
   {
       "name": "class-a-%s-back-to-normal" % name,
       "filter": {
           "attributes": {
               "type": "temp-status-back-to-normal"
           }
       }
   },
   {
       "name": "class-a-%s-status-bad" % name,
       "filter": {
           "attributes": {
               "type": "temp-status-bad"
           }
       }
   },
   {
       "name": "class-a-%s-still-bad" % name,
       "filter": {
           "attributes": {
               "type": "temp-status-still-bad"
           }
       }
   },
)
triggers_default_broker = "class-a"

ksvc_sink = "broker:default"
ksvc_procevents_sink = "broker:procevents"

