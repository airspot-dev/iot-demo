#!/bin/bash

curl -H {"api_key": "bearer $API_KEY"} --data-binary payload-example.json
