#!/usr/bin/env bash
PROJECT_NAME=payhere/backend

docker build --network host -t ${PROJECT_NAME} .
