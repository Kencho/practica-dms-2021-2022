#!/bin/bash

set -xe

cd /tmp/deps/src/common
./install.sh

cd /tmp/src
./install.sh
./start.sh
