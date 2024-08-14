import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import sys
import numpy as np

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
pygame.display.set_caption("3D Maze Explorer")

# Cube vertices
vertices = [
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1),
]

# Cube edges
edges = [
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),
    (4, 5),
    (5, 6),
    (6, 7),
    (7, 4),
    (0, 4),
    (1, 5),
    (2, 6),
    (3, 7),
]

# Draw a cube
def draw_cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

# Render the maze
def render_maze():
    glPushMatrix()
    for x in range(-5, 6):
        for z in range(-5, 6):
            if (x % 2 == 0 or z % 2 == 0):
                glTranslatef(x * 2, 0, z * 2)
                draw_cube()
                glTranslatef(-x * 2, 0, -z * 2)
    glPopMatrix()

# Set up the camera
def setup_camera():
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (WIDTH / HEIGHT), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 1, -10, 0, 1, 0, 0, 1, 0)

# Collision detection
def check_collision(pos):
    x, y, z = pos
    if x < -10 or x > 10 or z < -10 or z > 10:
        return True
    return False

# Main game loop
def game_loop():
    setup_camera()

    pos = np.array([0.0, 1.0, -5.0])

    running = True
    while running:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            pos[0] -= 0.1
        if keys[pygame.K_RIGHT]:
            pos[0] += 0.1
        if keys[pygame.K_UP]:
            pos[2] += 0.1
        if keys[pygame.K_DOWN]:
            pos[2] -= 0.1

        if check_collision(pos):
            pos[0], pos[2] = 0, -5  # Reset to start if collision occurs

        # Update camera position
        glLoadIdentity()
        gluLookAt(pos[0], pos[1], pos[2], pos[0], pos[1], pos[2] + 1, 0, 1, 0)

        # Render maze
        render_maze()

        # Update the display
        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    game_loop()