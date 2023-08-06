#!/bin/sh

set -e
set -x

# Run pycodestyle
#
python3 -m pycodestyle uosclient

# Run pylint
#
python3 -m pylint uosclient
