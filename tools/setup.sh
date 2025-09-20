#!/bin/bash
# Setup script for game development tools

echo "Setting up game development tools..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "tools_env" ]; then
    echo "Creating tools virtual environment..."
    python3 -m venv tools_env
fi

# Activate virtual environment
echo "Activating tools environment..."
source tools_env/bin/activate

# Install dependencies
echo "Installing tool dependencies..."
pip install -r requirements.txt

echo "Setup complete!"
echo ""
echo "To use the tools:"
echo "  1. Activate the environment: source tools_env/bin/activate"
echo "  2. Use tools:"
echo "     cd image_processing"
echo "     python3 bit_depth_converter.py --help"
echo ""
echo "To deactivate when done: deactivate"