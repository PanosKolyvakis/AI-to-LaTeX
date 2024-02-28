#!/bin/bash

# Path to your latex_requirements.txt file
REQUIREMENTS_FILE="latex_requirements.txt"

# Check if tlmgr is available
if ! command -v tlmgr &> /dev/null
then
    echo "tlmgr could not be found. Please ensure TeX Live is correctly installed."
    exit
fi

# Install packages listed in the requirements file
while IFS= read -r package
do
    echo "Installing LaTeX package: $package"
    tlmgr install "$package"
done < "$REQUIREMENTS_FILE"
