import pygame

def generate_planet_images():
    planet_colors = {
        'jupiter': (200, 150, 100),  # Orange-brown
        'saturn': (220, 200, 150),   # Yellow-light brown
        'mars': (200, 80, 50),      # Red
        'earth': (50, 150, 200),    # Blue-green
        'venus': (230, 230, 180),   # Pale yellow
        'mercury': (150, 150, 150), # Gray
        'uranus': (150, 200, 200),  # Light blue
        'neptune': (50, 100, 200),  # Darker blue
        'pluto': (180, 150, 150)    # Light gray-pink
    }

    image_size = 100 # Diameter of the planet image
    radius = image_size // 2

    for planet_name, base_color in planet_colors.items():
        surface = pygame.Surface((image_size, image_size), pygame.SRCALPHA)
        
        # Add subtle gradient for spherical look
        for i in range(radius):
            alpha = int(255 * (1 - (i / radius)**2)) # Quadratic falloff for smoother gradient
            color = (min(255, base_color[0] + i), min(255, base_color[1] + i), min(255, base_color[2] + i), alpha)
            pygame.draw.circle(surface, color, (radius, radius), radius - i)

        # Draw the base color circle (this will be mostly covered by gradient, but ensures base color)
        pygame.draw.circle(surface, base_color, (radius, radius), radius)

        if planet_name == 'saturn':
            # Add a simple ring for Saturn
            ring_color = (180, 160, 120)
            pygame.draw.ellipse(surface, ring_color, (radius - radius * 1.2, radius - radius * 0.3, radius * 2.4, radius * 0.6), 5)
            pygame.draw.ellipse(surface, ring_color, (radius - radius * 1.1, radius - radius * 0.25, radius * 2.2, radius * 0.5), 2)
        elif planet_name == 'jupiter':
            # Add a simple Great Red Spot for Jupiter
            spot_color = (150, 50, 30)
            pygame.draw.ellipse(surface, spot_color, (radius + radius * 0.2, radius - radius * 0.3, radius * 0.4, radius * 0.2), 0)

        pygame.image.save(surface, f"assets/{planet_name}.png")
        print(f"Generated assets/{planet_name}.png")

if __name__ == '__main__':
    pygame.init()
    generate_planet_images()
    pygame.quit()