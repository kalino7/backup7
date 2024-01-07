#!/bin/bash
echo "Running smoke test......"

NODE_VERSION=$(node --version) 

# Check if the last execution command was successful
if [ $? -eq 0 ]; then
    #parsing the app version from package.json
    VERSION=$(perl -ne 'print "$1\n" if /"version": *"(.*?)"/' package.json)

    if [ $? -eq 0 ]; then
        echo "App Version: $VERSION, is running on Node version: $NODE_VERSION"
        echo "..."
        echo "smoke test was successful"
        exit 0
    else
        echo "Failed to get NODE version"
        exit 1
    fi
else
    echo "Failed to run smoke test"
    exit 1
fi