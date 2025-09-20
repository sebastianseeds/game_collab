"""
Main Menu for Quorum of Suns

Handles the main menu interface with New Game, Continue, and Settings options.
"""

import pygame
from enum import Enum

class MenuOption(Enum):
    NEW_GAME = 0
    CONTINUE = 1
    SETTINGS = 2
    QUIT = 3

class MainMenu:
    def __init__(self, screen, game_state_manager):
        self.screen = screen
        self.game_state = game_state_manager
        
        # Menu state
        self.selected_option = MenuOption.NEW_GAME
        self.menu_options = [
            ("New Game", MenuOption.NEW_GAME),
            ("Continue", MenuOption.CONTINUE),
            ("Settings", MenuOption.SETTINGS),
            ("Quit", MenuOption.QUIT)
        ]
        
        # Visual settings
        self.title_font = pygame.font.Font(None, 72)
        self.menu_font = pygame.font.Font(None, 48)
        self.subtitle_font = pygame.font.Font(None, 32)
        
        # Colors
        self.title_color = (220, 180, 100)  # Golden
        self.normal_color = (180, 180, 200)  # Light gray
        self.selected_color = (255, 220, 120)  # Bright gold
        self.disabled_color = (100, 100, 120)  # Dark gray
        self.background_color = (10, 10, 20)  # Dark space
        
        # Animation
        self.pulse_timer = 0.0
        
    def handle_event(self, event):
        """Handle input events, return new game state if changing"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.move_selection(-1)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.move_selection(1)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                return self.select_option()
        
        return None
    
    def move_selection(self, direction):
        """Move menu selection up or down"""
        options = [opt[1] for opt in self.menu_options]
        current_index = options.index(self.selected_option)
        new_index = (current_index + direction) % len(options)
        self.selected_option = options[new_index]
    
    def select_option(self):
        """Execute the selected menu option"""
        
        if self.selected_option == MenuOption.NEW_GAME:
            return "NEW_GAME_SETUP"  # Return string instead of enum to avoid circular import
        elif self.selected_option == MenuOption.CONTINUE:
            if self.game_state.has_continue_save():
                # TODO: Load most recent save and go to galaxy view
                print("Continue game - TODO: Load most recent save")
                return "GALAXY_VIEW"
            else:
                print("No saved games found!")
                return None
        elif self.selected_option == MenuOption.SETTINGS:
            return "SETTINGS"
        elif self.selected_option == MenuOption.QUIT:
            return "QUIT"
        
        return None
    
    def update(self, dt):
        """Update menu animations"""
        self.pulse_timer += dt * 3.0  # Pulse speed
    
    def render(self):
        """Render the main menu"""
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        # Render starfield background
        self.render_starfield()
        
        # Game title
        title_text = self.title_font.render("QUORUM OF SUNS", True, self.title_color)
        title_rect = title_text.get_rect(center=(screen_width // 2, 150))
        self.screen.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_text = self.subtitle_font.render("A Grand Strategy Space Odyssey", True, self.normal_color)
        subtitle_rect = subtitle_text.get_rect(center=(screen_width // 2, 200))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Menu options
        menu_start_y = 320
        menu_spacing = 60
        
        for i, (text, option) in enumerate(self.menu_options):
            y_pos = menu_start_y + (i * menu_spacing)
            
            # Determine color and effects
            if option == self.selected_option:
                # Pulsing effect for selected option
                pulse = abs(pygame.math.Vector2(1, 0).rotate(self.pulse_timer * 60).x)
                alpha = int(180 + 75 * pulse)
                color = (*self.selected_color[:3], alpha) if len(self.selected_color) == 4 else self.selected_color
                
                # Selection indicator
                indicator = "► "
            else:
                color = self.normal_color
                indicator = "   "
            
            # Check if option should be disabled
            if option == MenuOption.CONTINUE and not self.game_state.has_continue_save():
                color = self.disabled_color
                text += " (No saves found)"
            
            # Render menu text
            menu_text = self.menu_font.render(indicator + text, True, color)
            menu_rect = menu_text.get_rect(center=(screen_width // 2, y_pos))
            self.screen.blit(menu_text, menu_rect)
        
        # Instructions
        instructions = [
            "Use ARROW KEYS or WASD to navigate",
            "Press ENTER or SPACE to select",
            "Press ESCAPE to return to main menu from any screen"
        ]
        
        instruction_y = screen_height - 120
        for instruction in instructions:
            inst_text = self.subtitle_font.render(instruction, True, (120, 120, 140))
            inst_rect = inst_text.get_rect(center=(screen_width // 2, instruction_y))
            self.screen.blit(inst_text, inst_rect)
            instruction_y += 25
    
    def render_starfield(self):
        """Render animated starfield background"""
        # Simple starfield effect
        import random
        random.seed(42)  # Consistent stars
        
        for _ in range(100):
            x = random.randint(0, self.screen.get_width())
            y = random.randint(0, self.screen.get_height())
            brightness = random.randint(100, 255)
            size = random.choice([1, 1, 1, 2])  # Mostly small stars
            
            # Twinkling effect
            twinkle = abs(pygame.math.Vector2(1, 0).rotate(self.pulse_timer * 30 + x + y).x)
            final_brightness = int(brightness * (0.3 + 0.7 * twinkle))
            
            color = (final_brightness, final_brightness, final_brightness)
            pygame.draw.circle(self.screen, color, (x, y), size)