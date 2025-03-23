#!/bin/sh

# Navigate to the working directory
cd /linter

# Initialize a Git repository if it doesn't exist
if [ ! -d ".git" ]; then
    echo "Initializing Git repository..."
    git init
fi

# Check if there are any Python files
if ls *.py 1> /dev/null 2>&1; then
    # Add Python files to git
    git add *.py
    git status
else
    echo "No Python files found to add."
fi

# Check if uv.lock exists and add it to git
if [ -f "uv.lock" ]; then
    echo "Adding uv.lock to Git..."
    git add uv.lock pyproject.toml
    git status
else
    echo "uv.lock file not found."
fi

# Run the pre-commit checks (optional, uncomment if needed)
PRE_COMMIT_OUTPUT=$(pre-commit run --all-files --verbose 2>&1)
if [ $? -eq 0 ]; then
    echo "pre-commit completed successfully."
else
    echo "pre-commit failed."
    echo "Error details:"
    echo "$PRE_COMMIT_OUTPUT"
    exit 1
fi

# Copy all Python files to the /main folder, forcefully replacing any existing files
if ls *.py 1> /dev/null 2>&1; then
    echo "Copying Python files to /main..."
    cp -f *.py /main/
    echo "Copy completed."
else
    echo "No Python files found to copy."
fi

# # Keep the container running
# tail -f /dev/null