"""
Galaxy View Interface for Quorum of Suns

Main strategic interface showing the galactic map with bottom control panel.
"""

import pygame
import math
from typing import Optional
from .galaxy_map import GalaxyMap, GalaxyGenerator, Star

class GalaxyView:
    def __init__(self, screen, game_state_manager):
        self.screen = screen
        self.game_state = game_state_manager
        
        # Display settings
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.control_panel_height = 120
        self.map_area_height = self.screen_height - self.control_panel_height
        
        # Load galaxy background
        self.galaxy_background = None
        try:
            self.galaxy_background = pygame.image.load("assets/maps/spiral_arm_galaxy.png").convert()
            # Scale to fit the galaxy map dimensions (we'll set these to match image size)
            self.galaxy_bg_width = 1200
            self.galaxy_bg_height = 1200
            self.galaxy_background = pygame.transform.scale(self.galaxy_background, 
                                                          (self.galaxy_bg_width, self.galaxy_bg_height))
        except Exception as e:
            print(f"Could not load galaxy background: {e}")
            self.galaxy_background = None
        
        # Map state
        self.galaxy_map: Optional[GalaxyMap] = None
        self.camera_x = 0
        self.camera_y = 0
        self.zoom = 1.0
        self.selected_star: Optional[Star] = None
        
        # UI state
        self.dragging = False
        self.last_mouse_pos = (0, 0)
        
        # Fonts
        self.title_font = pygame.font.Font(None, 36)
        self.info_font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        
        # Colors
        self.panel_color = (30, 30, 40)
        self.panel_border_color = (60, 60, 80)
        self.text_color = (200, 200, 220)
        self.selected_color = (255, 255, 100)
        self.button_color = (50, 50, 70)
        self.button_hover_color = (70, 70, 90)
        
        # Animation
        self.time_pulse = 0.0
        
        # Initialize galaxy if needed
        if not self.galaxy_map:
            self.generate_new_galaxy()
    
    def generate_new_galaxy(self):
        """Generate a new galaxy map"""
        # Use current game time as seed for reproducible galaxies
        seed = hash(self.game_state.current_save.save_name) if self.game_state.current_save else 42
        
        # Scale galaxy to fit in the available screen space with some padding
        available_width = self.screen_width - 40  # Leave 20px padding on each side
        available_height = self.map_area_height - 40  # Leave 20px padding top/bottom
        
        # Use smaller dimension to maintain aspect ratio
        galaxy_size = min(available_width, available_height)
        
        self.galaxy_map = GalaxyGenerator.generate_galaxy(
            width=galaxy_size, 
            height=galaxy_size, 
            num_stars=45,
            seed=seed,
            galaxy_image_path="assets/maps/spiral_arm_galaxy.png" if self.galaxy_background else None
        )
        
        # Update background size to match
        if self.galaxy_background:
            self.galaxy_bg_width = galaxy_size
            self.galaxy_bg_height = galaxy_size
            self.galaxy_background = pygame.transform.scale(
                pygame.image.load("assets/maps/spiral_arm_galaxy.png").convert(),
                (galaxy_size, galaxy_size)
            )
        
        # Center camera to show entire galaxy
        self.camera_x = (self.galaxy_map.width - self.screen_width) // 2
        self.camera_y = (self.galaxy_map.height - self.map_area_height) // 2
        
        # Ensure camera doesn't go negative (galaxy smaller than screen)
        self.camera_x = max(0, self.camera_x)
        self.camera_y = max(0, self.camera_y)
    
    def update_screen_size(self):
        """Update screen dimensions and regenerate galaxy to fit new size"""
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.map_area_height = self.screen_height - self.control_panel_height
        
        # Regenerate galaxy to fit new screen size
        self.generate_new_galaxy()
    
    def handle_event(self, event):
        """Handle input events"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_x, mouse_y = event.pos
                if mouse_y < self.map_area_height:  # Click in map area
                    # Check for star selection
                    world_x, world_y = self.screen_to_world(mouse_x, mouse_y)
                    clicked_star = self.galaxy_map.get_star_at_position(world_x, world_y, 15.0)
                    if clicked_star:
                        self.selected_star = clicked_star
                        print(f"Selected star: {clicked_star.name}")
                    else:
                        self.selected_star = None
                        # Start dragging
                        self.dragging = True
                        self.last_mouse_pos = event.pos
                else:
                    # Click in control panel
                    self.handle_control_panel_click(mouse_x, mouse_y)
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False
        
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                mouse_x, mouse_y = event.pos
                dx = mouse_x - self.last_mouse_pos[0]
                dy = mouse_y - self.last_mouse_pos[1]
                self.camera_x -= dx
                self.camera_y -= dy
                self.last_mouse_pos = event.pos
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Advance time
                self.advance_time()
            elif event.key == pygame.K_TAB:
                # Cycle through stars
                self.cycle_star_selection()
        
        return None
    
    def handle_control_panel_click(self, mouse_x, mouse_y):
        """Handle clicks in the control panel"""
        panel_y = self.map_area_height
        relative_y = mouse_y - panel_y
        
        # Check for button clicks (implement specific buttons later)
        if 50 <= mouse_x <= 150 and 20 <= relative_y <= 50:
            # End Turn button area
            self.advance_time()
        elif 200 <= mouse_x <= 300 and 20 <= relative_y <= 50:
            # Tech button area (placeholder)
            print("Tech button clicked (not implemented)")
    
    def advance_time(self):
        """Advance game time by one turn"""
        if self.game_state.current_save:
            self.game_state.current_save.game_turn += 1
            print(f"Turn advanced to: {self.game_state.current_save.game_turn}")
    
    def cycle_star_selection(self):
        """Cycle through stars for easy navigation"""
        if not self.galaxy_map.stars:
            return
        
        if self.selected_star:
            try:
                current_index = self.galaxy_map.stars.index(self.selected_star)
                next_index = (current_index + 1) % len(self.galaxy_map.stars)
                self.selected_star = self.galaxy_map.stars[next_index]
            except ValueError:
                self.selected_star = self.galaxy_map.stars[0]
        else:
            self.selected_star = self.galaxy_map.stars[0]
        
        # Center camera on selected star
        if self.selected_star:
            self.camera_x = self.selected_star.x - self.screen_width // 2
            self.camera_y = self.selected_star.y - self.map_area_height // 2
    
    def screen_to_world(self, screen_x, screen_y):
        """Convert screen coordinates to world coordinates"""
        world_x = screen_x + self.camera_x
        world_y = screen_y + self.camera_y
        return world_x, world_y
    
    def world_to_screen(self, world_x, world_y):
        """Convert world coordinates to screen coordinates"""
        screen_x = world_x - self.camera_x
        screen_y = world_y - self.camera_y
        return screen_x, screen_y
    
    def update(self, dt):
        """Update galaxy view"""
        self.time_pulse += dt * 2.0
    
    def render(self):
        """Render the galaxy view"""
        # Clear screen
        self.screen.fill((5, 5, 15))  # Very dark space
        
        # Render galaxy map
        self.render_galaxy_map()
        
        # Render control panel
        self.render_control_panel()
        
        # Render UI overlays
        self.render_star_info()
    
    def render_galaxy_map(self):
        """Render the galactic map"""
        if not self.galaxy_map:
            return
        
        # Create map surface (clipped to map area)
        map_surface = pygame.Surface((self.screen_width, self.map_area_height))
        map_surface.fill((5, 5, 15))
        
        # Draw galaxy background image if available
        if self.galaxy_background:
            # Calculate position to center the galaxy image
            bg_screen_x = -self.camera_x
            bg_screen_y = -self.camera_y
            
            # Only draw if any part is visible
            if (bg_screen_x + self.galaxy_bg_width > 0 and bg_screen_x < self.screen_width and
                bg_screen_y + self.galaxy_bg_height > 0 and bg_screen_y < self.map_area_height):
                map_surface.blit(self.galaxy_background, (bg_screen_x, bg_screen_y))
        else:
            # Draw background grid if no galaxy image
            self.draw_background_grid(map_surface)
        
        # Draw stars
        for star in self.galaxy_map.stars:
            screen_x, screen_y = self.world_to_screen(star.x, star.y)
            
            # Only draw if on screen
            if -20 <= screen_x <= self.screen_width + 20 and -20 <= screen_y <= self.map_area_height + 20:
                self.draw_star(map_surface, star, screen_x, screen_y)
        
        # Draw selection indicator
        if self.selected_star:
            screen_x, screen_y = self.world_to_screen(self.selected_star.x, self.selected_star.y)
            if 0 <= screen_x <= self.screen_width and 0 <= screen_y <= self.map_area_height:
                self.draw_selection_indicator(map_surface, screen_x, screen_y)
        
        self.screen.blit(map_surface, (0, 0))
    
    def draw_background_grid(self, surface):
        """Draw subtle background grid"""
        grid_size = 100
        grid_color = (15, 15, 25)
        
        # Vertical lines
        start_x = -(self.camera_x % grid_size)
        for x in range(int(start_x), self.screen_width + grid_size, grid_size):
            pygame.draw.line(surface, grid_color, (x, 0), (x, self.map_area_height))
        
        # Horizontal lines
        start_y = -(self.camera_y % grid_size)
        for y in range(int(start_y), self.map_area_height + grid_size, grid_size):
            pygame.draw.line(surface, grid_color, (0, y), (self.screen_width, y))
    
    def draw_star(self, surface, star, screen_x, screen_y):
        """Draw a star on the map"""
        # Create a proper glow effect using filled circles with decreasing alpha
        glow_layers = 5
        max_glow_radius = int(star.size * 2.5)
        
        # Create temporary surface for glow with alpha
        glow_surface = pygame.Surface((max_glow_radius * 2 + 10, max_glow_radius * 2 + 10), pygame.SRCALPHA)
        
        for i in range(glow_layers):
            # Calculate radius and alpha for this layer
            layer_radius = max_glow_radius * (1 - i / glow_layers)
            alpha = int(30 * (1 - i / glow_layers))  # Fade out towards edges
            
            # Create glow color with alpha
            glow_color = (*star.color, alpha)
            
            # Draw filled circle for glow layer
            if layer_radius > 0:
                pygame.draw.circle(glow_surface, glow_color, 
                                 (max_glow_radius + 5, max_glow_radius + 5), 
                                 int(layer_radius))
        
        # Blit glow to main surface
        surface.blit(glow_surface, (screen_x - max_glow_radius - 5, screen_y - max_glow_radius - 5))
        
        # Main star (solid and bright)
        pygame.draw.circle(surface, star.color, (int(screen_x), int(screen_y)), int(star.size))
        
        # Star name (if not too zoomed out)
        if star.size > 2:
            name_text = self.small_font.render(star.name, True, (180, 180, 200))
            name_rect = name_text.get_rect(center=(screen_x, screen_y + star.size + 12))
            surface.blit(name_text, name_rect)
    
    def draw_selection_indicator(self, surface, screen_x, screen_y):
        """Draw selection indicator around selected star"""
        pulse = abs(math.sin(self.time_pulse))
        radius = 15 + pulse * 5
        alpha = int(150 + pulse * 105)
        
        # Create a surface for the selection ring with alpha
        selection_surface = pygame.Surface((radius * 2 + 10, radius * 2 + 10), pygame.SRCALPHA)
        pygame.draw.circle(selection_surface, (*self.selected_color[:3], alpha), 
                         (radius + 5, radius + 5), int(radius), 2)
        
        surface.blit(selection_surface, (screen_x - radius - 5, screen_y - radius - 5))
    
    def render_control_panel(self):
        """Render the bottom control panel"""
        panel_y = self.map_area_height
        
        # Panel background
        panel_rect = pygame.Rect(0, panel_y, self.screen_width, self.control_panel_height)
        pygame.draw.rect(self.screen, self.panel_color, panel_rect)
        pygame.draw.line(self.screen, self.panel_border_color, 
                        (0, panel_y), (self.screen_width, panel_y), 2)
        
        # Time display
        if self.game_state.current_save:
            turn_text = self.info_font.render(f"Turn: {self.game_state.current_save.game_turn}", 
                                            True, self.text_color)
            self.screen.blit(turn_text, (20, panel_y + 20))
        
        # Control buttons
        self.draw_button("End Turn", 50, panel_y + 50, 100, 30)
        self.draw_button("Tech", 200, panel_y + 50, 100, 30)
        self.draw_button("Diplomacy", 350, panel_y + 50, 100, 30)
        self.draw_button("Fleet", 500, panel_y + 50, 100, 30)
        
        # Quick info
        info_text = "SPACE: Advance Time | TAB: Cycle Stars | Click & Drag: Pan Map | ESC: Main Menu"
        info_surface = self.small_font.render(info_text, True, (120, 120, 140))
        info_rect = info_surface.get_rect(center=(self.screen_width // 2, panel_y + 90))
        self.screen.blit(info_surface, info_rect)
    
    def draw_button(self, text, x, y, width, height):
        """Draw a UI button"""
        button_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, self.button_color, button_rect)
        pygame.draw.rect(self.screen, self.panel_border_color, button_rect, 1)
        
        text_surface = self.small_font.render(text, True, self.text_color)
        text_rect = text_surface.get_rect(center=button_rect.center)
        self.screen.blit(text_surface, text_rect)
    
    def render_star_info(self):
        """Render information about the selected star"""
        if not self.selected_star:
            return
        
        # Determine panel size based on content
        base_height = 120
        extra_height = 40 if self.selected_star.homeworld_species else 0
        info_height = base_height + extra_height
        
        # Info panel in top-right corner
        info_width = 280
        info_x = self.screen_width - info_width - 20
        info_y = 20
        
        # Background
        info_rect = pygame.Rect(info_x, info_y, info_width, info_height)
        pygame.draw.rect(self.screen, self.panel_color, info_rect)
        
        # Special border color for homeworld systems
        border_color = (255, 215, 0) if self.selected_star.homeworld_species else self.panel_border_color
        pygame.draw.rect(self.screen, border_color, info_rect, 2)
        
        # Star info
        y_offset = info_y + 10
        
        # Star name with homeworld indicator
        star_name = self.selected_star.name
        if self.selected_star.homeworld_species:
            star_name += " ⭐"  # Homeworld indicator
        name_text = self.info_font.render(star_name, True, self.selected_color)
        self.screen.blit(name_text, (info_x + 10, y_offset))
        y_offset += 25
        
        type_text = self.small_font.render(f"Type: {self.selected_star.star_type.value.replace('_', ' ').title()}", 
                                         True, self.text_color)
        self.screen.blit(type_text, (info_x + 10, y_offset))
        y_offset += 20
        
        planets_text = self.small_font.render(f"Planets: {'Yes' if self.selected_star.has_planets else 'None'}", 
                                            True, self.text_color)
        self.screen.blit(planets_text, (info_x + 10, y_offset))
        y_offset += 20
        
        explored_text = self.small_font.render(f"Explored: {'Yes' if self.selected_star.is_explored else 'No'}", 
                                             True, self.text_color)
        self.screen.blit(explored_text, (info_x + 10, y_offset))
        y_offset += 20
        
        # Homeworld information
        if self.selected_star.homeworld_species:
            homeworld_text = self.small_font.render(f"Homeworld: {self.selected_star.homeworld_planet}", 
                                                   True, (255, 215, 0))  # Gold color
            self.screen.blit(homeworld_text, (info_x + 10, y_offset))
            y_offset += 20
            
            species_text = self.small_font.render(f"Species: {self.selected_star.homeworld_species}", 
                                                 True, (255, 215, 0))  # Gold color
            self.screen.blit(species_text, (info_x + 10, y_offset))