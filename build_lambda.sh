#!/bin/sh
docker build --platform linux/amd64 --provenance=false -t amanzi-lambda:latest -f lambda/Dockerfile .
