"""
Game State Management for Quorum of Suns

Handles save/load functionality, game settings, and persistent data.
"""

import json
import os
from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional

@dataclass
class GameSettings:
    """User settings and preferences"""
    master_volume: float = 0.7
    sfx_volume: float = 0.8
    music_volume: float = 0.6
    fullscreen: bool = False
    auto_save: bool = True
    difficulty: str = "normal"  # easy, normal, hard, impossible

@dataclass
class GameSave:
    """Saved game data structure"""
    save_name: str = "New Game"
    player_species: str = "human"
    game_turn: int = 1
    galaxy_size: str = "medium"
    difficulty: str = "normal"
    playtime_hours: float = 0.0
    galaxy_seed: int = 42
    # TODO: Add actual game data as we build systems
    # explored_stars: List[str] = field(default_factory=list)
    # player_fleets: List[Dict] = field(default_factory=list)
    # diplomatic_status: Dict[str, str] = field(default_factory=dict)

class GameStateManager:
    """Manages game state, saves, and settings"""
    
    def __init__(self):
        self.settings_file = "data/config/settings.json"
        self.saves_dir = "data/saves"
        
        # Ensure directories exist
        os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
        os.makedirs(self.saves_dir, exist_ok=True)
        
        # Load settings
        self.settings = self.load_settings()
        
        # Current game state
        self.current_save: Optional[GameSave] = None
        
    def load_settings(self) -> GameSettings:
        """Load user settings from file"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    data = json.load(f)
                    return GameSettings(**data)
        except Exception as e:
            print(f"Could not load settings: {e}")
        
        # Return default settings
        return GameSettings()
    
    def save_settings(self):
        """Save current settings to file"""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(asdict(self.settings), f, indent=2)
        except Exception as e:
            print(f"Could not save settings: {e}")
    
    def get_save_files(self) -> list[str]:
        """Get list of available save files"""
        try:
            saves = []
            for filename in os.listdir(self.saves_dir):
                if filename.endswith('.json'):
                    saves.append(filename[:-5])  # Remove .json extension
            return sorted(saves)
        except Exception:
            return []
    
    def load_game(self, save_name: str) -> Optional[GameSave]:
        """Load a game save"""
        try:
            save_path = os.path.join(self.saves_dir, f"{save_name}.json")
            if os.path.exists(save_path):
                with open(save_path, 'r') as f:
                    data = json.load(f)
                    return GameSave(**data)
        except Exception as e:
            print(f"Could not load save '{save_name}': {e}")
        return None
    
    def save_game(self, save_data: GameSave):
        """Save current game state"""
        try:
            save_path = os.path.join(self.saves_dir, f"{save_data.save_name}.json")
            with open(save_path, 'w') as f:
                json.dump(asdict(save_data), f, indent=2)
            self.current_save = save_data
        except Exception as e:
            print(f"Could not save game: {e}")
    
    def has_continue_save(self) -> bool:
        """Check if there's a recent save to continue"""
        saves = self.get_save_files()
        return len(saves) > 0
    
    def start_new_game(self, save_name: str = "New Game") -> GameSave:
        """Start a new game with default settings"""
        import random
        
        new_save = GameSave(
            save_name=save_name,
            player_species="human",
            game_turn=1,
            galaxy_size="medium", 
            difficulty=self.settings.difficulty,
            playtime_hours=0.0,
            galaxy_seed=random.randint(1, 1000000)
        )
        
        self.current_save = new_save
        return new_save