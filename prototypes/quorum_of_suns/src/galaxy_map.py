"""
Galaxy Map System for Quorum of Suns

Handles galactic and star system maps, including star generation and navigation.
"""

import random
import math
from dataclasses import dataclass
from typing import List, Optional, Tuple
from enum import Enum

class StarType(Enum):
    YELLOW_DWARF = "yellow_dwarf"
    RED_GIANT = "red_giant"
    WHITE_DWARF = "white_dwarf"
    BLUE_GIANT = "blue_giant"
    NEUTRON_STAR = "neutron_star"
    BINARY_SYSTEM = "binary_system"

@dataclass
class Star:
    """Represents a star in the galaxy"""
    name: str
    x: float
    y: float
    star_type: StarType
    color: Tuple[int, int, int]
    size: float
    has_planets: bool = True
    is_explored: bool = False
    has_starbase: bool = False
    homeworld_species: str = None  # Species that has their homeworld here
    homeworld_planet: str = None   # Name of the homeworld planet
    
    def distance_to(self, other_star) -> float:
        """Calculate distance to another star"""
        dx = self.x - other_star.x
        dy = self.y - other_star.y
        return math.sqrt(dx * dx + dy * dy)

@dataclass
class GalaxyMap:
    """Represents the entire galaxy"""
    width: int
    height: int
    stars: List[Star]
    name: str = "Unnamed Galaxy"
    
    def get_star_at_position(self, x: float, y: float, tolerance: float = 20.0) -> Optional[Star]:
        """Find a star near the given position"""
        for star in self.stars:
            distance = math.sqrt((star.x - x) ** 2 + (star.y - y) ** 2)
            if distance <= tolerance:
                return star
        return None
    
    def get_stars_in_range(self, center_x: float, center_y: float, range_radius: float) -> List[Star]:
        """Get all stars within a certain range of a position"""
        stars_in_range = []
        for star in self.stars:
            distance = math.sqrt((star.x - center_x) ** 2 + (star.y - center_y) ** 2)
            if distance <= range_radius:
                stars_in_range.append(star)
        return stars_in_range

class GalaxyGenerator:
    """Generates procedural galaxies"""
    
    STAR_NAMES = [
        "Atheon", "Brixis", "Crylos", "Drenith", "Evandor", "Fyrmere", "Galdris", "Hexara",
        "Ithrys", "Jelvon", "Kethara", "Lyraxis", "Morthak", "Nexilon", "Oshimar", "Pytheris", "Qeltion",
        "Rythen", "Sylkara", "Thyrnos", "Ulveron", "Vaxon", "Wyldris", "Xelthar", "Ythiron", "Zelkane",
        "Aelkris", "Byrneth", "Corvix", "Dythara", "Elenthis", "Falduros", "Gytheon", "Helkaar",
        "Ivaxis", "Jorthis", "Kyrinon", "Malthen", "Norvith", "Oxalar", "Pelthen", "Qorthak",
        "Ravex", "Sythion", "Telvaris", "Ukthara", "Valdris", "Wenthis", "Xytheon", "Yvaleth"
    ]
    
    STAR_TYPE_WEIGHTS = {
        StarType.YELLOW_DWARF: 0.4,   # Most common, like our sun
        StarType.RED_GIANT: 0.25,    # Common
        StarType.WHITE_DWARF: 0.15,  # Fairly common
        StarType.BLUE_GIANT: 0.1,    # Rare but impressive
        StarType.NEUTRON_STAR: 0.05, # Very rare
        StarType.BINARY_SYSTEM: 0.05 # Very rare
    }
    
    STAR_COLORS = {
        StarType.YELLOW_DWARF: (255, 255, 180),
        StarType.RED_GIANT: (255, 100, 100),
        StarType.WHITE_DWARF: (255, 255, 255),
        StarType.BLUE_GIANT: (150, 200, 255),
        StarType.NEUTRON_STAR: (200, 150, 255),
        StarType.BINARY_SYSTEM: (255, 200, 150)
    }
    
    @classmethod
    def generate_galaxy(cls, width: int, height: int, num_stars: int = 50, seed: int = None, galaxy_image_path: str = None) -> GalaxyMap:
        """Generate a new galaxy with procedurally placed stars"""
        if seed is not None:
            random.seed(seed)
        
        stars = []
        used_names = set()
        
        # Try to load galaxy image for star positioning
        star_positions = []
        if galaxy_image_path:
            try:
                import pygame
                galaxy_img = pygame.image.load(galaxy_image_path)
                galaxy_img = pygame.transform.scale(galaxy_img, (width, height))
                star_positions = cls._extract_bright_spots(galaxy_img, num_stars)
            except Exception as e:
                print(f"Could not analyze galaxy image: {e}")
        
        # Fallback to procedural generation if no image positions
        if not star_positions:
            center_x, center_y = width // 2, height // 2
        
        # First, create the human homeworld system (Ra)
        ra_star = Star(
            name="Ra",
            x=0, y=0,  # Will be positioned below
            star_type=StarType.YELLOW_DWARF,
            color=cls.STAR_COLORS[StarType.YELLOW_DWARF],
            size=cls._get_star_size(StarType.YELLOW_DWARF),
            has_planets=True,
            is_explored=True,
            homeworld_species="Human",
            homeworld_planet="Eden"
        )
        
        # Position Ra near galactic core but not in it (about 20% from center)
        center_x, center_y = width // 2, height // 2
        core_radius = min(width, height) * 0.2  # 20% from center
        ra_angle = random.uniform(0, 2 * math.pi)
        ra_star.x = center_x + core_radius * math.cos(ra_angle)
        ra_star.y = center_y + core_radius * math.sin(ra_angle)
        
        stars.append(ra_star)
        used_names.add("Ra")

        for i in range(num_stars - 1):  # -1 because we already added Ra
            # Choose star name
            available_names = [name for name in cls.STAR_NAMES if name not in used_names]
            if not available_names:
                # Generate numbered names if we run out
                name = f"Star-{i + 2:03d}"  # +2 because Ra is star 1
            else:
                name = random.choice(available_names)
                used_names.add(name)
            
            # Choose star type based on weights
            star_type = cls._weighted_choice(cls.STAR_TYPE_WEIGHTS)
            
            # Use image-based position if available, otherwise use procedural generation
            if star_positions and i < len(star_positions):
                x, y = star_positions[i]
                # Add small random offset to avoid perfect alignment
                x += random.uniform(-5, 5)
                y += random.uniform(-5, 5)
            else:
                # Fallback to procedural generation
                center_x, center_y = width // 2, height // 2
                if i < 5:
                    # First few stars closer to center (home systems)
                    angle = random.uniform(0, 2 * math.pi)
                    radius = random.uniform(50, 150)
                    x = center_x + radius * math.cos(angle)
                    y = center_y + radius * math.sin(angle)
                else:
                    # Distribute others more broadly with some spiral structure
                    spiral_arm = random.randint(0, 2)  # 3 spiral arms
                    arm_angle = (spiral_arm * 2 * math.pi / 3) + random.uniform(-0.5, 0.5)
                    radius = random.uniform(100, min(width, height) * 0.4)
                    spiral_factor = radius / (min(width, height) * 0.4)
                    final_angle = arm_angle + spiral_factor * math.pi
                    
                    x = center_x + radius * math.cos(final_angle) + random.uniform(-50, 50)
                    y = center_y + radius * math.sin(final_angle) + random.uniform(-50, 50)
            
            # Keep stars within bounds
            x = max(30, min(width - 30, x))
            y = max(30, min(height - 30, y))
            
            # Determine star properties
            color = cls.STAR_COLORS[star_type]
            size = cls._get_star_size(star_type)
            has_planets = random.random() > 0.1  # 90% have planets
            
            star = Star(
                name=name,
                x=x,
                y=y,
                star_type=star_type,
                color=color,
                size=size,
                has_planets=has_planets
            )
            
            stars.append(star)
        
        return GalaxyMap(
            width=width,
            height=height,
            stars=stars,
            name="Quorum Galaxy"
        )
    
    @classmethod
    def _weighted_choice(cls, weights_dict):
        """Choose item based on weights"""
        items = list(weights_dict.keys())
        weights = list(weights_dict.values())
        return random.choices(items, weights=weights)[0]
    
    @classmethod
    def _get_star_size(cls, star_type: StarType) -> float:
        """Get display size for star type"""
        size_map = {
            StarType.YELLOW_DWARF: 3.0,
            StarType.RED_GIANT: 5.0,
            StarType.WHITE_DWARF: 2.0,
            StarType.BLUE_GIANT: 6.0,
            StarType.NEUTRON_STAR: 1.5,
            StarType.BINARY_SYSTEM: 4.0
        }
        return size_map.get(star_type, 3.0)
    
    @classmethod
    def _extract_bright_spots(cls, galaxy_surface, num_stars: int):
        """Extract bright spots from galaxy image to use as star positions"""
        import pygame
        
        width, height = galaxy_surface.get_size()
        brightness_map = []
        
        # Sample brightness at regular intervals to find bright spots
        sample_step = 5  # Sample every 5 pixels for performance
        
        for y in range(0, height, sample_step):
            for x in range(0, width, sample_step):
                try:
                    # Get pixel color
                    r, g, b = galaxy_surface.get_at((x, y))[:3]
                    
                    # Calculate brightness (weighted for visual perception)
                    brightness = 0.299 * r + 0.587 * g + 0.114 * b
                    
                    # Store position and brightness
                    brightness_map.append((brightness, x, y))
                except:
                    continue
        
        # Sort by brightness (brightest first) and take top positions
        brightness_map.sort(reverse=True, key=lambda x: x[0])
        
        # Extract positions of brightest spots
        star_positions = []
        min_distance = 40  # Minimum distance between stars
        
        for brightness, x, y in brightness_map:
            # Only consider reasonably bright spots
            if brightness < 50:  # Threshold for minimum brightness
                break
                
            # Check if this position is far enough from existing stars
            too_close = False
            for existing_x, existing_y in star_positions:
                distance = math.sqrt((x - existing_x)**2 + (y - existing_y)**2)
                if distance < min_distance:
                    too_close = True
                    break
            
            if not too_close:
                star_positions.append((x, y))
                
                # Stop when we have enough stars
                if len(star_positions) >= num_stars:
                    break
        
        return star_positions