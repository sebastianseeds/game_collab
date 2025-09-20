#!/usr/bin/env python3
"""
Game Prototype Template

A basic pygame template for rapid prototyping. This template doesn't force
any framework - just provides a simple starting point that you can modify
or completely replace with your preferred approach.

Feel free to:
- Use a different game engine (Unity, Godot, etc.)
- Use different libraries (arcade, pyglet, etc.) 
- Build from scratch with just SDL/OpenGL
- Use web technologies (JavaScript/Canvas)

This is just ONE possible starting point.
"""

import pygame
import sys

# Initialize pygame
pygame.init()

# Constants (modify as needed)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
BACKGROUND_COLOR = (20, 20, 30)
PLAYER_COLOR = (100, 200, 255)

class GamePrototype:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Game Prototype Template")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Example game state
        self.player_x = SCREEN_WIDTH // 2
        self.player_y = SCREEN_HEIGHT // 2
        self.player_speed = 200  # pixels per second
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def update(self, dt):
        # Handle input
        keys = pygame.key.get_pressed()
        
        # Example movement (WASD or arrow keys)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.player_y -= self.player_speed * dt
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.player_y += self.player_speed * dt
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.player_x -= self.player_speed * dt
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.player_x += self.player_speed * dt
        
        # Keep player on screen
        self.player_x = max(25, min(SCREEN_WIDTH - 25, self.player_x))
        self.player_y = max(25, min(SCREEN_HEIGHT - 25, self.player_y))
        
        # Add your game logic here
        
    def render(self):
        # Clear screen
        self.screen.fill(BACKGROUND_COLOR)
        
        # Draw player
        pygame.draw.circle(
            self.screen, 
            PLAYER_COLOR,
            (int(self.player_x), int(self.player_y)), 
            25
        )
        
        # Draw instructions
        font = pygame.font.Font(None, 36)
        text = font.render("Use WASD or Arrow Keys to Move", True, (255, 255, 255))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(text, text_rect)
        
        # Add your rendering code here
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # Delta time in seconds
            
            self.handle_events()
            self.update(dt)
            self.render()
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = GamePrototype()
    game.run()