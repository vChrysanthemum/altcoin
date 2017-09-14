#!/bin/bash

docker run -dit --name dev -v $(realpath "$(pwd)/../../../"):/altcoin base
