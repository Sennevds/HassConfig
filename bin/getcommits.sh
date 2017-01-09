#!/bin/bash

cd "/home/hass/.homeassistant"
sudo git fetch
echo $(git rev-list --count master..origin/master)
exit
