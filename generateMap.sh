#!/bin/bash

echo "This script DOES NOT END AUTOMATICALLY. Please close SUMO manually after generating the map files and then CTRL+C the terminal and then run generateParkingAreas."

# Generating map files
read -p "Enter the name of the output folder: " folder

# Run osmWebWizard.py (this will block the script)
python3 /usr/share/sumo/tools/osmWebWizard.py -o "$folder"