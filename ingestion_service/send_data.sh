#!/bin/bash

curl $1 -H "authorization: Bearer $3" -H "Content-Type: application/json" -d @$2
