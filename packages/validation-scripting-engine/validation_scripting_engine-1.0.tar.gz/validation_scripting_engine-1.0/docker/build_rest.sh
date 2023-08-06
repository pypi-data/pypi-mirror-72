#!/usr/bin/env bash

cd ..

docker build .  -f docker/rest.Dockerfile -t cbaxter1988/vse:rest