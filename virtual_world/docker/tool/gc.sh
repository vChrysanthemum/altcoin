#!/bin/bash
docker images -a|grep -v IMAGE|awk '{print $3}'|xargs docker rmi -f
