#!/bin/bash

year="2015"
wget -l2 -nc -rkp -T 5 -e robots=off -np --reject last100 "https://lkml.org/lkml/$year"

find lkml.org -type f -print0 | xargs -0 sed -i 's/redirect.js//g'
