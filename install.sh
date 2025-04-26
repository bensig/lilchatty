#!/bin/bash

# Simple script to download and run the Lil' Chatty setup wizard

set -e # Exit immediately if a command exits with a non-zero status.

REPO_RAW_URL="https://raw.githubusercontent.com/bensig/lilchatty/main"

echo "🚀 Starting Lil' Chatty Setup..."

# --- Prerequisite Check ---
echo "Checking prerequisites..."

if ! command -v python3 &> /dev/null
then
    echo "❌ Error: Python 3 is not installed. Please install Python 3 and try again."
    echo "Visit: https://www.python.org/downloads/"
    exit 1
fi

if ! python3 -m pip --version &> /dev/null
then
    echo "❌ Error: pip for Python 3 is not available. Please ensure pip is installed for your Python 3 environment."
    echo "See: https://pip.pypa.io/en/stable/installation/"
    exit 1
fi

echo "✅ Prerequisites met (Python 3 and pip found)."

# --- Download and Install Dependencies ---
echo "Downloading requirements..."
curl -fsSL "${REPO_RAW_URL}/requirements.txt" -o lilchatty_requirements.txt

echo "Installing dependencies (Flask)..."
python3 -m pip install -r lilchatty_requirements.txt

# --- Download and Run App ---
echo "Downloading setup wizard (app.py)..."
curl -fsSL "${REPO_RAW_URL}/app.py" -o lilchatty_app.py

echo "Running setup wizard..."
python3 lilchatty_app.py

# --- Cleanup (optional) ---
echo "Cleaning up temporary files..."
rm lilchatty_requirements.txt
rm lilchatty_app.py

echo "✨ Lil' Chatty setup wizard finished or was closed." 