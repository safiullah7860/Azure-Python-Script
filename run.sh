#!/bin/bash

# Run the command 20 times concurrently
for ((i=1; i<=20; i++)); do
    echo "Running command iteration $i"
    python azure.py &
done

# Wait for all background jobs to finish
wait
