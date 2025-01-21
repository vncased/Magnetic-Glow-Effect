import pygame
import random
import math
import platform
import os
import sys


pygame.init()


WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive Glowing Network")


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


GRADIENT_COLORS = [
    (255, 255, 255),  
    (0, 255, 255),    
    (0, 0, 255),      
    (128, 0, 255),    
]


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        self.size = random.uniform(0.12, 0.13)  
        self.color = (255, 255, 255)  
        self.glow_surface = self.create_glow_surface()

    def create_glow_surface(self):
        
        glow_surface = pygame.Surface((60, 60), pygame.SRCALPHA)
        center = 30
        for i, color in enumerate(GRADIENT_COLORS[::-1]):
            alpha = int(180 * ((len(GRADIENT_COLORS) - i) / len(GRADIENT_COLORS)))
            pygame.draw.circle(glow_surface, (*color, alpha), (center, center), center - i * 8)
        return glow_surface

    def move(self, mouse_pos):
        self.x += self.vx
        self.y += self.vy

        
        if self.x <= 0 or self.x >= WIDTH:
            self.vx *= -1
        if self.y <= 0 or self.y >= HEIGHT:
            self.vy *= -1

        
        if mouse_pos:
            mx, my = mouse_pos
            distance = math.hypot(self.x - mx, self.y - my)
            if distance < 150:
                force = (150 - distance) / 150
                angle = math.atan2(self.y - my, self.x - mx)
                self.vx += math.cos(angle) * force * 0.5
                self.vy += math.sin(angle) * force * 0.5

    def draw(self):
        
        center_x = int(self.x - 30)
        center_y = int(self.y - 30)
        screen.blit(self.glow_surface, (center_x, center_y))

        
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))


nodes = [Node(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(50)]


def add_nodes(num_nodes):
    return [Node(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(num_nodes)]


def draw_lines():
    grid_size = 150
    grid = {}
    for i, node in enumerate(nodes):
        cell_x = int(node.x // grid_size)
        cell_y = int(node.y // grid_size)
        grid.setdefault((cell_x, cell_y), []).append(i)

    for i, node1 in enumerate(nodes):
        cell_x = int(node1.x // grid_size)
        cell_y = int(node1.y // grid_size)
        nearby_cells = [
            (cell_x + dx, cell_y + dy)
            for dx in (-1, 0, 1)
            for dy in (-1, 0, 1)
        ]
        for cell in nearby_cells:
            for j in grid.get(cell, []):
                if i < j:  
                    node2 = nodes[j]
                    distance = math.hypot(node1.x - node2.x, node1.y - node2.y)
                    if distance < 150:
                        alpha = max(0, 255 - int(distance * 1.5))
                        color = (
                            (node1.color[0] + node2.color[0]) // 2,
                            (node1.color[1] + node2.color[1]) // 2,
                            (node1.color[2] + node2.color[2]) // 2,
                        )
                        pygame.draw.aaline(screen, color, (node1.x, node1.y), (node2.x, node2.y))


running = True
clock = pygame.time.Clock()
mouse_pos = None


input_active = False
text = ""
input_box = pygame.Rect(50, HEIGHT - 100, 300, 40)  
font = pygame.font.Font(None, 36)

while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  
                nodes.append(Node(*event.pos))

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:  
                input_active = True
            elif event.key == pygame.K_RETURN and input_active:  
                if text.lower() == "exit":
                    pygame.quit()
                    sys.exit()  
                elif text.lower() == "tll":
                    input_active = False
                    text = ""  
                    
                    if platform.system() == "Linux":
                        os.system('python3 tll.py')
                    elif platform.system() == "Windows":
                        os.system("python tll.py")
                    pygame.quit()
                    sys.exit()    
                elif text.lower() == "cll":
                    input_active = False
                    text = ""  
                    
                    if platform.system() == "Linux":
                        os.system('python3 cll.py')
                    elif platform.system() == "Windows":
                        os.system("python cll.py")
                    pygame.quit()
                    sys.exit()    
                try:
                    
                    num_nodes = int(text)
                    
                    nodes.extend(add_nodes(num_nodes))  
                except ValueError:
                    pass
                input_active = False  
                text = ""  
            elif event.key == pygame.K_BACKSPACE:
                text = text[:-1]
            elif input_active:
                text += event.unicode

    
    if input_active:
        
        pygame.draw.rect(screen, WHITE, input_box, 2)
        txt_surface = font.render(text, True, WHITE)
        screen.blit(txt_surface, (input_box.x + 10, input_box.y + 5))

    
    for node in nodes:
        node.move(mouse_pos)
        node.draw()

    draw_lines()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
