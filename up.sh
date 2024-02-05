#!/usr/bin/env bash

set -ex

docker-compose -f docker-compose.dev.yml up --build --exit-code-from app
BUILD_EXIT_CODE=$?
docker-compose -f docker-compose.dev.yml down

if [ $BUILD_EXIT_CODE -eq 0 ];
then
  docker-compose up --build
fi
