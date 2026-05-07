#!/bin/bash
# Setup script for DAR-Cyber Backend

set -e

echo "=== DAR-Cyber Backend Setup ==="

# Check Python version
echo "Checking Python version..."
python3 --version || { echo "Python 3 is required"; exit 1; }

# Create virtual environment if not exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv || { echo "Failed to create venv. Install python3-venv"; exit 1; }
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Create .env from example if not exists
if [ ! -f ".env" ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env and set your configuration!"
fi

echo ""
echo "=== Setup Complete ==="
echo "To activate the environment: source venv/bin/activate"
echo "To run the server: uvicorn app.main:app --reload"
echo "To run tests: pytest tests/"
