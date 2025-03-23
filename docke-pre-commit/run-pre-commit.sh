#!/bin/bash

# Run Docker Compose and wait for completion
PRE_COMMIT_OUTPUT=$(docker-compose -f compose-precommit.yml up --build --abort-on-container-exit --exit-code-from fastapi-pre-commit 2>&1)
if [ $? -eq 0 ]; then
    echo "pre-commit completed successfully."
else
    echo "pre-commit failed."
    echo "Error details:"
    echo "$PRE_COMMIT_OUTPUT"
    exit 1
fi