"""
Car Driving Game using Pygame
A simple game where you can drive a car with arrow keys to control direction and speed.
"""

import pygame
pygame.init()  # Initialize pygame immediately after import

import sys
import math
from enum import Enum


class Direction(Enum):
    """Enum for car direction."""
    UP = 0
    RIGHT = 90
    DOWN = 180
    LEFT = 270


class Car:
    """Represents the car in the game."""
    
    def __init__(self, x, y, width=50, height=30):
        """Initialize the car with position and dimensions."""
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.angle = 0  # 0 degrees is up
        self.speed = 0
        self.max_speed = 15
        self.max_reverse_speed = -5
        self.acceleration = 0.5
        self.rotation_speed = 5
    
    def increase_speed(self):
        """Increase the car's speed."""
        if self.speed < self.max_speed:
            self.speed += self.acceleration
    
    def decrease_speed(self):
        """Decrease the car's speed."""
        if self.speed > self.max_reverse_speed:
            self.speed -= self.acceleration
    
    def turn_left(self):
        """Turn the car left."""
        self.angle += self.rotation_speed
        if self.angle >= 360:
            self.angle -= 360
    
    def turn_right(self):
        """Turn the car right."""
        self.angle -= self.rotation_speed
        if self.angle < 0:
            self.angle += 360
    
    def update(self, screen_width, screen_height):
        """Update car position based on speed and angle."""
        # Convert angle to radians and calculate new position
        angle_rad = math.radians(self.angle)
        self.x += self.speed * math.sin(angle_rad)
        self.y -= self.speed * math.cos(angle_rad)
        
        # Keep car within screen boundaries
        self.x = max(0, min(self.x, screen_width - self.width))
        self.y = max(0, min(self.y, screen_height - self.height))
    
    def draw(self, surface):
        """Draw the car on the screen."""
        # Create a surface for the car
        car_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Draw car body (red rectangle)
        pygame.draw.rect(car_surface, (220, 20, 60), (0, 0, self.width, self.height))
        
        # Draw car window (light blue)
        window_height = self.height // 3
        pygame.draw.rect(car_surface, (100, 149, 237), 
                        (self.width // 4, window_height, self.width // 2, window_height))
        
        # Draw car headlights (yellow circles)
        pygame.draw.circle(car_surface, (255, 255, 0), (10, 5), 3)
        pygame.draw.circle(car_surface, (255, 255, 0), (10, self.height - 5), 3)
        
        # Rotate the car surface
        rotated_surface = pygame.transform.rotate(car_surface, self.angle)
        rotated_rect = rotated_surface.get_rect(center=(self.x + self.width // 2, 
                                                        self.y + self.height // 2))
        
        surface.blit(rotated_surface, rotated_rect.topleft)


class CarDrivingGame:
    """Main game class for the car driving game."""
    
    def __init__(self, width=1000, height=700):
        """Initialize the game."""
        try:
            self.width = width
            self.height = height
            self.screen = pygame.display.set_mode((width, height))
            pygame.display.set_caption("Car Driving Game")
            
            self.clock = pygame.time.Clock()
            self.running = True
            self.fps = 60
            
            # Initialize car
            self.car = Car(width // 2, height // 2)
            
            # Colors
            self.bg_color = (34, 139, 34)  # Forest green
            self.text_color = (255, 255, 255)  # White
            
            # Lazy load fonts to avoid circular import issues
            self.font = None
            self.title_font = None
            
        except Exception as e:
            print(f"Error initializing game: {e}")
            pygame.quit()
            sys.exit()
    
    def get_font(self, size=24):
        """Get or create a font with lazy loading."""
        try:
            return pygame.font.SysFont('arial', size)
        except:
            # Fallback to default font if SysFont fails
            try:
                return pygame.font.Font(None, size)
            except:
                # Last resort: use a basic rendering approach
                return None
    
    def draw_background(self):
        """Draw the game background."""
        self.screen.fill(self.bg_color)
        
        # Draw road markings (dashed lines)
        line_color = (255, 255, 100)
        dash_size = 20
        gap_size = 20
        
        # Horizontal lines
        for y in range(0, self.height, dash_size + gap_size):
            pygame.draw.line(self.screen, line_color, (0, y), 
                           (self.width, y), 2)
        
        # Vertical lines
        for x in range(0, self.width, dash_size + gap_size):
            pygame.draw.line(self.screen, line_color, (x, 0), 
                           (x, self.height), 2)
    
    def draw_hud(self):
        """Draw heads-up display (HUD) with game info."""
        font = self.get_font(20)
        
        if font is None:
            return  # Skip HUD if font creation fails
        
        # Speed display
        speed_text = font.render(f"Speed: {self.car.speed:.1f}", True, self.text_color)
        self.screen.blit(speed_text, (10, 10))
        
        # Angle display
        angle_text = font.render(f"Angle: {self.car.angle:.0f}°", True, self.text_color)
        self.screen.blit(angle_text, (10, 40))
        
        # Position display
        pos_text = font.render(f"Position: ({self.car.x:.0f}, {self.car.y:.0f})", True, self.text_color)
        self.screen.blit(pos_text, (10, 70))
        
        # Controls display
        controls_text = [
            "Controls:",
            "↑ Arrow: Increase Speed",
            "↓ Arrow: Decrease Speed",
            "← Arrow: Turn Left",
            "→ Arrow: Turn Right",
            "ESC: Exit Game"
        ]
        
        y_offset = self.height - len(controls_text) * 25 - 10
        for i, text in enumerate(controls_text):
            control_text = font.render(text, True, self.text_color)
            self.screen.blit(control_text, (self.width - 250, y_offset + i * 25))
    
    def handle_events(self):
        """Handle game events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def handle_input(self):
        """Handle continuous key input."""
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_UP]:
            self.car.increase_speed()
        elif keys[pygame.K_DOWN]:
            self.car.decrease_speed()
        
        if keys[pygame.K_LEFT]:
            self.car.turn_left()
        if keys[pygame.K_RIGHT]:
            self.car.turn_right()
    
    def update(self):
        """Update game logic."""
        self.car.update(self.width, self.height)
    
    def draw(self):
        """Draw all game elements."""
        self.draw_background()
        self.car.draw(self.screen)
        self.draw_hud()
        pygame.display.flip()
    
    def run(self):
        """Main game loop."""
        try:
            while self.running:
                self.handle_events()
                self.handle_input()
                self.update()
                self.draw()
                self.clock.tick(self.fps)
        
        except Exception as e:
            print(f"Error during game loop: {e}")
        
        finally:
            pygame.quit()
            sys.exit()


if __name__ == "__main__":
    game = CarDrivingGame()
    game.run()
