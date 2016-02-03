#!/bin/bash

export CONCORDION_HOME=/Users/gweaver/Documents/ARPA-E/pyconcordion-read-only
export PYTHONPATH=$CONCORDION_HOME/src
python -t $CONCORDION_HOME/src/scripts/concordion_folder_runner src/tests
