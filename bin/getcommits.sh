#!/bin/bash

# Become user 'hass'
sudo su -s /bin/bash hass <<'EOF'
# Activate the virtualenv
source /srv/hass/hass_venv/bin/activate
cd "/home/hass/.homeassistant"
git fetch
echo $(git rev-list --count master..origin/master)
exit
EOF
