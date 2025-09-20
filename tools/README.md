# Game Development Tools

Collection of standalone tools that can be used with any game engine or framework. These tools help with common game development tasks like asset processing, level generation, and content creation.

## 🎨 Image Processing

Tools for converting and processing game graphics:

- **[Bit Depth Converter](image_processing/bit_depth_converter.py)**: Convert images to retro-style low bit depths (8-bit, 16-bit)
- *More coming soon...*

## 🔊 Audio Processing

Tools for game audio (planned):

- Audio format converter
- Bit rate reducer for retro audio
- Sound effect generator

## 🗺️ Level Generation

Procedural content generation tools (planned):

- Dungeon generator
- Terrain height map generator
- Maze generator

## 📦 Asset Conversion

Tools for converting between formats (planned):

- 3D model format converter
- Texture atlas generator
- Animation frame extractor

## Usage Philosophy

These tools are designed to be:

- **Framework-agnostic**: Work with Unity, Godot, pygame, custom engines, etc.
- **Standalone**: No dependencies on shared game code
- **Command-line friendly**: Easy to integrate into build pipelines
- **Single-purpose**: Each tool does one thing well
- **Reusable**: Useful across different game genres and styles

## Setup

```bash
# One-time setup (creates tools_env virtual environment)
./setup.sh

# Then activate before using tools
source tools_env/bin/activate

# Use tools...
cd image_processing
python3 bit_depth_converter.py --help

# Deactivate when done
deactivate
```

## Adding New Tools

1. Add your tool to the appropriate directory
2. Update `requirements.txt` if you need new dependencies  
3. Update `setup.sh` to mention your tool
4. Add documentation with usage examples