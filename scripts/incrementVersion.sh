#!/bin/bash

# Path to the __init__.py file
INIT_FILE="./three/__init__.py"

# Extract the current version
CURRENT_VERSION=$(grep -oP "(?<=__version__ = ')[^']*" "$INIT_FILE")
echo "Current version: $CURRENT_VERSION"

# Split the version into its components
IFS='.' read -r -a VERSION_PARTS <<< "$CURRENT_VERSION"

# Increment the build number
VERSION_PARTS[2]=$((VERSION_PARTS[2] + 1))

# Construct the new version
NEW_VERSION="${VERSION_PARTS[0]}.${VERSION_PARTS[1]}.${VERSION_PARTS[2]}"

# Update the __init__.py file with the new version
sed -i "s/__version__ = '$CURRENT_VERSION'/__version__ = '$NEW_VERSION'/" "$INIT_FILE"

echo "Version updated from $CURRENT_VERSION to $NEW_VERSION"