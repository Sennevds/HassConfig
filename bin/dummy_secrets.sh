#!/bin/bash

echo "http_password: dummy" >> $TRAVIS_BUILD_DIR/secrets.yaml
echo "mqtt_user: dummy" >> $TRAVIS_BUILD_DIR/secrets.yaml
echo "mqtt_password: dummy" >> $TRAVIS_BUILD_DIR/secrets.yaml
echo "ifttt_key: dummy" >> $TRAVIS_BUILD_DIR/secrets.yaml
echo "telegram_api_key: dummy" >> $TRAVIS_BUILD_DIR/secrets.yaml
echo "telegram_chat_id: dummy" >> $TRAVIS_BUILD_DIR/secrets.yaml
echo "darksky_api_key: dummy" >> $TRAVIS_BUILD_DIR/secrets.yaml
echo "ssl_certificate: dummy" >> $TRAVIS_BUILD_DIR/secrets.yaml
echo "ssl_key: dummy" >> $TRAVIS_BUILD_DIR/secrets.yaml
echo "google_client_id: dummy" >> $TRAVIS_BUILD_DIR/secrets.yaml
echo "google_client_secret: dummy" >> $TRAVIS_BUILD_DIR/secrets.yaml
echo "file: "+$TRAVIS_BUILD_DIR/+"mysensors.json" >> $TRAVIS_BUILD_DIR/secrets.yaml
