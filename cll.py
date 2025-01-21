import pygame
import random
import math
import sys  
import os
import platform


pygame.init()


WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive Glowing Network")


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        self.size = random.uniform(2, 3)  
        self.color = [random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)]
        self.color_change = [random.uniform(-0.3, 0.3) for _ in range(3)]

        
        self.glow_surface = pygame.Surface((int(self.size * 10), int(self.size * 10)), pygame.SRCALPHA)
        center = self.size * 5
        for i in range(8, 0, -1):
            alpha = int(180 * (i / 8))
            glow_color = (*self.color, alpha)
            pygame.draw.circle(self.glow_surface, glow_color, (int(center), int(center)), int(self.size * i))

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

        
        for i in range(3):
            self.color[i] += self.color_change[i]
            if self.color[i] > 255 or self.color[i] < 100:
                self.color_change[i] *= -1

    def draw(self):
        
        center_x, center_y = int(self.x - self.size * 5), int(self.y - self.size * 5)
        screen.blit(self.glow_surface, (center_x, center_y))

        
        pygame.draw.circle(screen, tuple(map(int, self.color)), (int(self.x), int(self.y)), int(self.size))


nodes = [Node(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(50)]  


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

def add_nodes(num_nodes):
    return [Node(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(num_nodes)]


def update_background():
    t = pygame.time.get_ticks() / 2000
    r = int(20 + 10 * math.sin(t))
    g = int(20 + 10 * math.sin(t + 2))
    b = int(20 + 10 * math.sin(t + 4))
    screen.fill((r, g, b))


running = True
clock = pygame.time.Clock()
mouse_pos = None


input_active = False
text = ""
input_box = pygame.Rect(50, HEIGHT - 100, 300, 40)  
font = pygame.font.Font(None, 36)

while running:
    update_background()

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
                elif text.lower() == "bll":
                    print("Старт другой эффект")
                    input_active = False
                    text = ""  
                    
                    if platform.system() == "Linux":
                        os.system('python3 bll.py')
                    elif platform.system() == "Windows":
                        os.system("python bll.py")
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
