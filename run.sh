#!/bin/bash

# Run the command 20 times concurrently
for ((i=0; i<12; i++)); do
    echo "Running temperature setting 0.$i"
    python azure.py $i &
done

# Wait for all background jobs to finish
wait
