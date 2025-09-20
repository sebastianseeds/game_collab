# Quorum of Suns 🌟

A grand strategy space game combining the depth of Master of Orion with real-time ship combat like FTL and Pixel Starships.

## 🎮 Game Concept

**Grand Strategy Layer:**
- Multiple star systems with unique characteristics
- Various alien civilizations with distinct traits and backstories
- Deep tech trees with branching research paths
- Diplomacy, trade, and warfare on a galactic scale
- Story-driven campaigns based on starting species choice
- Unlockable civilizations and technologies

**Ship Combat Layer:**
- Direct control of your flagship in real-time combat
- FTL-style room management and crew assignment
- Pixel Starships-inspired ship customization
- Strategic combat with energy management and subsystem targeting

## 🚀 Current Status

**✅ Implemented:**
- Main menu with New Game, Continue, Settings options
- Basic game state management
- Save/load system foundation
- Settings persistence

**🔄 In Development:**
- New game setup (species selection, galaxy generation)
- Galaxy view and strategic gameplay
- Ship combat system

**📋 Planned Features:**
- Tech tree system
- Alien civilization AI
- Story campaigns
- Ship design and customization
- Resource management
- Diplomatic system

## 🛠️ Setup and Running

**Requirements:**
- Python 3.9+
- pygame

**Quick Setup:**
```bash
cd prototypes/quorum_of_suns
./setup.sh
```

**Manual Setup:**
```bash
# Create environment
python3 -m venv quorum_env
source quorum_env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Run the game:**
```bash
# Activate environment first
source quorum_env/bin/activate

# Run the game
python3 main.py
```

## 🎯 Controls

**Main Menu:**
- Arrow Keys / WASD: Navigate menu
- Enter / Space: Select option
- Escape: Return to main menu (from any screen)

## 📁 Project Structure

```
quorum_of_suns/
├── main.py              # Game entry point
├── src/                 # Game modules
│   ├── game_state.py    # Save/load and settings management
│   ├── main_menu.py     # Main menu interface
│   └── [more modules]   # Additional game systems
├── assets/              # Game assets
│   ├── sprites/         # Images and animations
│   ├── sounds/          # Audio files
│   └── fonts/           # Custom fonts
├── data/                # Game data
│   ├── saves/           # Saved games
│   └── config/          # Settings and configuration
└── docs/                # Documentation
```

## 🌌 Design Philosophy

**Accessibility:** Easy to learn, deep to master
**Modularity:** Each game system is independent and expandable
**Replayability:** Multiple species, random galaxy generation, branching stories
**Strategy + Action:** Balance between thoughtful planning and exciting real-time combat

## 🔮 Future Expansion Ideas

- Multiplayer support for cooperative or competitive gameplay
- Mod support for custom civilizations and ships
- Procedural story generation
- Advanced AI for dynamic galactic politics
- Mobile companion app for fleet management

## 🤝 Contributing

This is a prototype for testing game mechanics and concepts. Feel free to:
- Suggest new features or improvements
- Report bugs or gameplay issues
- Contribute art, sound, or code
- Playtest and provide feedback

---

*"In the vastness of space, alliances shift like stellar winds, and only the wisest leaders can unite the stars under one banner."*