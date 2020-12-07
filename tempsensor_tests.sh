#!/bin/sh
#Script to run TempSensor node unittests
echo "Running TempSensor node unittests..."
python3 tests/test_tempsensor.py -v
python3 tests/test_tempsensorclient.py -v
python3 tests/test_tempsensordb.py -v
python3 tests/test_tempthingspeak.py -v
