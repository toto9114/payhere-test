#!/usr/bin/env bash
PROJECT_NAME=payhere/backend

docker run -it --rm \
  -p 8000:8000 \
 ${PROJECT_NAME} "${@:1}"
