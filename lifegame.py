import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import numpy as np
import csv
import sys

# 初始化参数
N = 50
CELL_SIZE = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 初始化Pygame
pygame.init()
screen = pygame.display.set_mode((N * CELL_SIZE, N * CELL_SIZE))
clock = pygame.time.Clock()

def load_pattern(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        rows, cols = next(reader)
        pattern = np.zeros((int(rows), int(cols)))
        for i, row in enumerate(reader):
            pattern[i] = [int(cell) for cell in row]
    return pattern

# 从命令行读取CSV文件
if len(sys.argv) != 2:
    print("Usage: python lifegame.py <pattern.csv>")
    sys.exit(1)

pattern_file = sys.argv[1]

# 初始化网格，加载模式
grid = np.zeros((N, N))
pattern = load_pattern(pattern_file)
grid[1:1+pattern.shape[0], 1:1+pattern.shape[1]] = pattern

def draw_grid():
    for i in range(N):
        for j in range(N):
            color = WHITE if grid[i, j] == 1 else BLACK
            pygame.draw.rect(screen, color, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def update_grid():
    global grid
    new_grid = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            live_neighbors = np.sum(grid[max(0, i-1):min(N, i+2), max(0, j-1):min(N, j+2)]) - grid[i, j]
            if grid[i, j] == 1 and (live_neighbors == 2 or live_neighbors == 3):
                new_grid[i, j] = 1
            elif grid[i, j] == 0 and live_neighbors == 3:
                new_grid[i, j] = 1
    grid = new_grid

# 检测迭代周期
def detect_period():
    states = []
    period = 0
    while True:
        state = grid.tobytes()
        if state in states:
            period = len(states) - states.index(state)
            break
        states.append(state)
        update_grid()
    return period

# 主循环
running = True
paused = True
period_detected = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_RIGHT and paused:
                update_grid()
            elif event.key == pygame.K_p and paused and not period_detected:
                period = detect_period()
                print(f"Detected period: {period}")
                period_detected = True

    screen.fill(BLACK)
    draw_grid()
    pygame.display.flip()
    clock.tick(10)

    if not paused:
        update_grid()

pygame.quit()
