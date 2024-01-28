#!/bin/bash
echo "Running smoke test..."

NODE_VERSION=$(node --version)

# Check if the last execution command was successful
if [ $? -eq 0 ]; then
    # Parsing the app version from package.json
    VERSION=$(perl -ne 'print "$1\n" if /"version": *"(.*?)"/' package.json)

    if [ $? -eq 0 ]; then
        echo "App Version: $VERSION, is running on Node version: $NODE_VERSION"
        echo "......................................"

        # Empty database previous records if any
        python3 script/delete_db.py

        echo "Loading datasets into the database, this might take a while..."

        # Run Python script to add records
        python3 script/add_record.py

        # Check the exit status
        if [ $? -eq 0 ]; then
            echo "............................................."
            echo "All dataset has been successfully loaded into the database, now beginning extraction of schema...."

            # Run Python script to evaluate
            python3 script/evaluate.py

            # Check the exit status
            if [ $? -eq 0 ]; then
                # update the main.tex file to reflect the generated schema values            
                python3 script/generate_pdf_values.py
                if [ $? -eq 0 ]; then
                    echo "............................................."
                    echo "Smoke test was successful, Schemas extracted!!!"
                    exit 0
                else 
                    echo "............................................."
                    echo "Could not replace the generated values in the latex file"
                    exit 1
                fi
            else
                echo "............................................."
                echo "Failed to extract Schema."
                exit 1
            fi

        else
            echo "............................................."
            echo "Failed to load datasets into the database."
            exit 1
        fi
    else
        echo "............................................."
        echo "Failed to get NODE version"
        exit 1
    fi
else
    echo "............................................."
    echo "Failed to run smoke test"
    exit 1
fi
