#!/bin/bash

# Run the command 20 times concurrently
for ((i=1; i<=10; i++)); do
    echo "Running command iteration $i"
    python azure.py $i &
done

# Wait for all background jobs to finish
wait
