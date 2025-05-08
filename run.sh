#!/bin/bash

# Change to script directory
cd "$(dirname "$0")"

# Check if Python virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install requirements
    echo "Installing dependencies..."
    pip install -r requirements.txt
else
    # Activate virtual environment
    source venv/bin/activate
fi

# Run the application
echo "Starting HyprText..."
nohup python src/main.py 
echo "Program started! You can safely close this terminal if you don't want to debug."
