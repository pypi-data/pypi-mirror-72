#!/usr/bin/env bash

cd ..

docker build .  -f docker/rpc.Dockerfile -t cbaxter1988/vse:rpc