#!/bin/bash
sh -c "mkdir -p /altcoin/data/altcoin${1}"
sh -c "/altcoin/src/altcoind -conf=/altcoin/virtual_world/conf/altcoin${1}.conf"
