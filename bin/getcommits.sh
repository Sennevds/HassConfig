#!/bin/bash

cd "/home/homeassistant/.homeassistant"
git fetch
echo $(git rev-list --count master..origin/master)
exit
