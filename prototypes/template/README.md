# Game Prototype Template

This is ONE possible starting point for game prototypes. It's a simple pygame example, but you're encouraged to use whatever technology works best for your game idea.

## What This Template Provides

- **Basic pygame setup**: Simple game loop with input and rendering
- **Example movement**: WASD/Arrow key controls
- **Minimal code**: Easy to understand and modify
- **No forced dependencies**: Use it as-is or completely replace it

## Getting Started

1. **Copy this template**:
   ```bash
   cp -r prototypes/template prototypes/your_game_name
   cd prototypes/your_game_name
   ```

2. **Customize the game**:
   - Edit `main.py` to implement your game logic
   - Modify the `GamePrototype` class name to something more specific
   - Update this README with your game's details

3. **Run your prototype**:
   ```bash
   python3 main.py
   ```

## Template Structure

- `main.py` - Main game file with example implementation
- `README.md` - This documentation file

## Alternative Approaches

Feel free to ignore this template entirely and use:

- **Unity or Godot**: For full-featured game engines
- **Other Python libraries**: pygame-ce, arcade, pyglet
- **JavaScript**: HTML5 Canvas, Phaser, Three.js  
- **Native code**: C++ with SDL/SFML, Rust with ggez
- **Any other technology** that fits your project

## Customization Tips

1. **Add Game Objects**: Create classes for players, enemies, projectiles, etc.
2. **Use Shared Assets**: Place common assets in `shared/assets/` for reuse
3. **Implement Game States**: Add menus, pause screens, game over states
4. **Add Sound**: Use pygame's sound capabilities for audio
5. **Create Levels**: Implement level loading and progression

## Example Extensions

- Add sprites and animations
- Implement collision detection
- Create particle systems
- Add sound effects and music
- Implement save/load functionality
- Add multiple game states (menu, playing, paused)

## Dependencies

This template only uses:
- pygame (for graphics and input)

Install with:
```bash
pip install pygame
# or run the project setup: ../../setup.sh
```

## Using Project Tools

Check out the standalone tools in `../../tools/` that work with any game:
- **Image processing**: Convert images to retro bit depths
- **Audio tools**: (coming soon)
- **Level generation**: (coming soon)