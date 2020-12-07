#!/bin/sh

echo "                              ___ _          _ "
echo "  /\  /\___  _ __ ___   ___  / _ (_)_  _ ___| |"
echo " / /_/ / _ \|  _ ' _ \ / _ \/ /_)/ \ \/ / _ \ |"
echo "/ __  / (_) | | | | | |  __/ ___/| |>  <  __/ |"
echo "\/ /_/ \___/|_| |_| |_|\___\/    |_/_/\_\___|_|"

echo "\nSetting up environment..."
export PYTHONPATH=":$PWD/lightclapper:$PWD/securitysystem:$PWD/tempsensor"
export FLASK_APP="main.py"
export FLASK_ENV="development"
export FLASK_DEBUG="1"
echo "PYTHONPATH =" $PYTHONPATH
echo "FLASK_APP =" $FLASK_APP
echo "FLASK_ENV =" $FLASK_ENV
echo "FLASK_DEBUG =" $FLASK_DEBUG
echo "Environment ready. Have a nice day!"