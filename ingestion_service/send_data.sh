#!/bin/bash

curl $1 -H "authorization: Bearer $2" --data-binary payload-example.json
