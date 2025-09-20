# Game Collaboration Hub

Collaborative space for game prototyping with standalone tools that work across any game engine.

## Structure

```
tools/               # Standalone game dev tools
prototypes/          # Independent game prototypes  
shared/assets/       # Common game assets
game_ideas.txt       # Prototype ideas
```

## Tools

- **[Bit Depth Converter](tools/image_processing/)**: Convert images to retro 8-bit/16-bit color palettes

## Prototypes

- **[Space Shooter](prototypes/space_shooter/)**: Classic 2D space shooter (pygame)

## Quick Start

```bash
# Use a tool
cd tools/image_processing
python3 bit_depth_converter.py input.jpg output.png --bits 8

# Run a prototype
cd prototypes/space_shooter
python3 space_shooter.py

# Create your own prototype with any tech
mkdir prototypes/your_game
```