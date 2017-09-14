#!/bin/bash

docker run -dit --name test --dns 172.17.0.2 -v $(realpath "$(pwd)/../../../"):/altcoin base
