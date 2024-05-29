#!/bin/bash

# Use absolute paths for safety
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/clean"
DIST_FILE="$SCRIPT_DIR/dist/inter_doc-0.0.1-py3-none-any.whl"
TEST_SCRIPT="$SCRIPT_DIR/test.py"

if [ "$1" = "build" ]; then
    python3 setup.py sdist bdist_wheel
    if [ $? -ne 0 ]; then
        echo "Build failed."
        exit 1
    fi
elif [ "$1" = "reset" ]; then
    pip install "$DIST_FILE" --force-reinstall
    
    if [ $? -ne 0 ]; then
        echo "Installation of the wheel failed."
        exit 1
    fi
    clear
    echo "Install inter-doc successfully"

elif [ "$1" = "test" ]; then
    clear
    python3 -m unittest tests.py
    if [ $? -ne 0 ]; then
        echo "Tests failed."
        exit 1
    fi

else
    echo "Invalid command. Usage: ./run.sh [build|reset|test]"
    exit 1
fi
