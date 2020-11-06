#!/bin/sh

echo "                              ___ _          _ "
echo "  /\  /\___  _ __ ___   ___  / _ (_)_  _ ___| |"
echo " / /_/ / _ \|  _ ' _ \ / _ \/ /_)/ \ \/ / _ \ |"
echo "/ __  / (_) | | | | | |  __/ ___/| |>  <  __/ |"
echo "\/ /_/ \___/|_| |_| |_|\___\/    |_/_/\_\___|_|"

# TODO: Fix imports so this step is not needed
echo "\nSetting up environment..."
export PYTHONPATH=":$PWD/lightclapper:$PWD/securitysystem:$PWD/tempsensor"
echo "PYTHONPATH =" $PYTHONPATH
echo "Environment ready. Have a nice day!"
