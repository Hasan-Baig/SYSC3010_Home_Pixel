#!/bin/sh
# Script to run SecuritySystem node unittests
echo "Running SecuritySystem node unittests..."
python3 tests/test_securitysystem.py -v
python3 tests/test_securitysystemclient.py -v
python3 tests/test_securitysystemdb.py -v
python3 tests/test_securitythingspeak.py -v