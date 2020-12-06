#!/bin/sh
# Script to run LightClapper node unittests
echo "Running LightClapper node unittests..."
python3 tests/test_lightclapper.py -v
python3 tests/test_lightclapperclient.py -v
python3 tests/test_lightclapperdb.py -v
python3 tests/test_lightclapperthingspeak.py -v
