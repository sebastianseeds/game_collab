#!/usr/bin/env python3
"""
Quorum of Suns - A grand strategy space game with direct ship combat

Combines the depth of Master of Orion with real-time ship combat like FTL.
Features multiple civilizations, tech trees, and story-driven gameplay.
"""

import pygame
import sys
from enum import Enum
from src.game_state import GameStateManager
from src.main_menu import MainMenu
from src.galaxy_view import GalaxyView

class GameStates(Enum):
    MAIN_MENU = "main_menu"
    NEW_GAME_SETUP = "new_game_setup"
    GALAXY_VIEW = "galaxy_view"
    SHIP_COMBAT = "ship_combat"
    SETTINGS = "settings"
    QUIT = "quit"

class QuorumOfSuns:
    def __init__(self):
        pygame.init()
        
        # Game constants
        self.SCREEN_WIDTH = 1200
        self.SCREEN_HEIGHT = 800
        self.FPS = 60
        
        # Display state
        self.is_fullscreen = False
        
        # Initialize display
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Quorum of Suns")
        self.clock = pygame.time.Clock()
        
        # Game state management
        self.state_manager = GameStateManager()
        self.current_state = GameStates.MAIN_MENU
        
        # Initialize subsystems
        self.main_menu = MainMenu(self.screen, self.state_manager)
        self.galaxy_view = GalaxyView(self.screen, self.state_manager)
        
        self.running = True
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and self.current_state != GameStates.MAIN_MENU:
                    self.current_state = GameStates.MAIN_MENU
                elif event.key == pygame.K_F11:
                    # Toggle fullscreen
                    self.toggle_fullscreen()
            elif event.type == pygame.VIDEORESIZE:
                # Handle window resize
                self.handle_resize(event.w, event.h)
            
            # Pass events to current state
            if self.current_state == GameStates.MAIN_MENU:
                result = self.main_menu.handle_event(event)
                if result:
                    if result == "QUIT":
                        self.running = False
                    elif result == "NEW_GAME_SETUP":
                        # Skip setup for now, go straight to galaxy view
                        self.current_state = GameStates.GALAXY_VIEW
                        self.state_manager.start_new_game()
                    elif result == "GALAXY_VIEW":
                        self.current_state = GameStates.GALAXY_VIEW
                    elif result == "SETTINGS":
                        self.current_state = GameStates.SETTINGS
            elif self.current_state == GameStates.GALAXY_VIEW:
                result = self.galaxy_view.handle_event(event)
                if result:
                    self.current_state = result
    
    def update(self, dt):
        # Update current state
        if self.current_state == GameStates.MAIN_MENU:
            self.main_menu.update(dt)
        elif self.current_state == GameStates.GALAXY_VIEW:
            self.galaxy_view.update(dt)
        
    def render(self):
        # Clear screen
        self.screen.fill((10, 10, 20))  # Dark space background
        
        # Render current state
        if self.current_state == GameStates.MAIN_MENU:
            self.main_menu.render()
        elif self.current_state == GameStates.GALAXY_VIEW:
            self.galaxy_view.render()
        
        pygame.display.flip()
    
    def run(self):
        print("🌟 Quorum of Suns - Starting...")
        print("Escape key returns to main menu from any screen")
        print("F11 toggles fullscreen mode")
        
        while self.running:
            dt = self.clock.tick(self.FPS) / 1000.0
            
            self.handle_events()
            self.update(dt)
            self.render()
        
        pygame.quit()
        sys.exit()
    
    def toggle_fullscreen(self):
        """Toggle between fullscreen and windowed mode"""
        self.is_fullscreen = not self.is_fullscreen
        
        if self.is_fullscreen:
            # Go fullscreen
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            # Go windowed
            self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.RESIZABLE)
        
        # Update screen reference in subsystems
        self.main_menu.screen = self.screen
        self.galaxy_view.screen = self.screen
        self.galaxy_view.update_screen_size()
    
    def handle_resize(self, width, height):
        """Handle window resize"""
        if not self.is_fullscreen:
            self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
            
            # Update screen reference in subsystems
            self.main_menu.screen = self.screen
            self.galaxy_view.screen = self.screen
            self.galaxy_view.update_screen_size()

if __name__ == "__main__":
    game = QuorumOfSuns()
    game.run()