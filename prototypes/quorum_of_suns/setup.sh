#!/bin/bash
# Setup script for Quorum of Suns

echo "🌟 Setting up Quorum of Suns development environment..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "quorum_env" ]; then
    echo "Creating virtual environment..."
    python3 -m venv quorum_env
fi

# Activate virtual environment
echo "Activating virtual environment..."
source quorum_env/bin/activate

# Install dependencies
echo "Installing game dependencies..."
pip install -r requirements.txt

echo "✅ Setup complete!"
echo ""
echo "🚀 To run Quorum of Suns:"
echo "  1. Activate the environment: source quorum_env/bin/activate"
echo "  2. Run the game: python3 main.py"
echo ""
echo "🎮 Controls:"
echo "  - Arrow Keys/WASD: Navigate menu"
echo "  - Enter/Space: Select"
echo "  - Escape: Return to main menu"
echo ""
echo "To deactivate when done: deactivate"