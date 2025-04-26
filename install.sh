#!/bin/bash

# Script to download and run the Lil' Chatty setup wizard

set -e # Exit immediately if a command exits with a non-zero status.

REPO_URL="https://github.com/bensig/lilchatty.git"
TMP_DIR="lilchatty_setup_temp"

echo "🚀 Starting Lil' Chatty Setup..."

# --- Prerequisite Check ---
echo "Checking prerequisites..."

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed. Please install Python 3 and try again."
    echo "Visit: https://www.python.org/downloads/"
    exit 1
fi

# Check for pip
if ! python3 -m pip --version &> /dev/null; then
    echo "❌ Error: pip for Python 3 is not available. Please ensure pip is installed for your Python 3 environment."
    echo "See: https://pip.pypa.io/en/stable/installation/"
    exit 1
fi

# Check for Git
if ! command -v git &> /dev/null; then
    echo "❌ Error: Git is not installed. Please install Git and try again."
    echo "(On macOS, try running 'xcode-select --install' in the Terminal)"
    exit 1
fi

echo "✅ Prerequisites met (Python 3, pip, Git found)."

# --- Clone Repository --- 
echo "Cloning setup repository into temporary directory (${TMP_DIR})..."
# Remove temporary directory if it already exists
if [ -d "${TMP_DIR}" ]; then
    echo "Removing existing temporary directory..."
    rm -rf "${TMP_DIR}"
fi
git clone --depth 1 "${REPO_URL}" "${TMP_DIR}"

# Navigate into the temporary directory
cd "${TMP_DIR}"

# --- Install Dependencies ---
echo "Installing dependencies (Flask)..."
python3 -m pip install -r requirements.txt

# --- Run App ---
echo "Running setup wizard (app.py)..."
echo "(You can close the wizard by stopping this script with Ctrl+C)"
python3 app.py # app.py can now find ./static/

# --- Cleanup --- 
# Navigate back out of the temporary directory
cd ..
echo "Cleaning up temporary setup directory (${TMP_DIR})..."
rm -rf "${TMP_DIR}"

echo "✨ Lil' Chatty setup wizard finished or was closed." 