#!/bin/bash

curl $1 -H "authorization: Bearer $3" --data-binary $2
