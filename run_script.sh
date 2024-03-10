#!/bin/bash

# Get the directory of the script
script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change directory to the script's directory
cd "$script_dir"

python3 app.py 2> error.log
