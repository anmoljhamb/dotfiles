#!/bin/bash

# Check if the number of arguments is correct
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <profile-directory> <app>"
    exit 1
fi

# Assigning arguments to variables
profile_directory=$1
app=$2

# Execute the command
brave-browser --profile-directory="$profile_directory" --app="$app"
