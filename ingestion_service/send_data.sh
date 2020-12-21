#!/bin/bash

curl $1 -H "authorization: Bearer $2" -H "Content-Type: application/json" -d @$3
