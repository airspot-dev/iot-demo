from flask import Flask
from flask import request
import logging
import json_logging
import os
import sys
from cloudevents.sdk import converters
from cloudevents.sdk import marshaller
from cloudevents.sdk.converters import binary
from cloudevents.sdk.event import v1
import uuid
from datetime import datetime
import pytz
import requests
import json
import socket

app = Flask("ext-api")

json_logging.ENABLE_JSON_LOGGING = True
json_logging.init_flask()
json_logging.init_request_instrument(app)

logger = logging.getLogger(app.name)
logger.setLevel(int(os.environ.get("LOGGING_LEVEL", logging.DEBUG)))
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.propagate = False

req_logger = logging.getLogger("flask-request-logger")
req_logger.setLevel(logging.ERROR)
req_logger.propagate = False


@app.route("/", methods=['POST'])
def main():
    if request.headers.get("authorization", "") == "Bearer %s" % os.environ.get("API_KEY"):
        _id = str(uuid.uuid4())
        logging.debug("new event id: {}".format(_id))

        if "K_SERVICE" in os.environ:
            source = os.environ["K_SERVICE"]
        elif "SERVICE" in os.environ:
            source = os.environ["SERVICE"]
        else:
            source = socket.gethostname()

        event_time = datetime.utcnow().replace(tzinfo=pytz.UTC).isoformat()
        event = v1.Event()
        event.SetContentType('application/json')
        event.SetEventID(_id)
        event.SetSource(source)
        event.SetSubject(source)
        event.SetEventTime(event_time)
        event.SetEventType("data-received")

        event.Set('Originid', _id)
        event.SetData(
            {
                "receveidAt": event_time,
                "data": request.json,
            }
        )

        m = marshaller.NewHTTPMarshaller([binary.NewBinaryHTTPCloudEventConverter()])

        headers, body = m.ToRequest(event, converters.TypeBinary, json.dumps)

        response = requests.post(os.environ.get("DISPATCH_URL"),
                                 headers=headers,
                                 data=body)

        response.raise_for_status()
        return "OK", 200
    else:
        return "No valid API_KEY provided", 401
