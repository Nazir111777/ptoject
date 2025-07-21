import pygame
import random

# Инициализация
pygame.init()

# Размеры окна
WIDTH, HEIGHT = 300, 600
CELL_SIZE = 30
cols, rows = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE

# Цвета
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
COLORS = [(0, 255, 255), (0, 0, 255), (255, 127, 0),
          (255, 255, 0), (0, 255, 0), (128, 0, 128), (255, 0, 0)]

# Фигуры
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]]
]

# Окно и поле
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()
grid = [[0 for _ in range(cols)] for _ in range(rows)]

# Класс фигуры
class Piece:
    def _init_(self):
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS)
        self.x = cols // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = list(zip(*self.shape[::-1]))

    def valid(self, dx=0, dy=0, rotated_shape=None):
        shape = rotated_shape if rotated_shape else self.shape
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    nx = self.x + x + dx
                    ny = self.y + y + dy
                    if nx < 0 or nx >= cols or ny >= rows or (ny >= 0 and grid[ny][nx]):
                        return False
        return True

    def freeze(self):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell and self.y + y >= 0:
                    grid[self.y + y][self.x + x] = self.color

def draw_grid():
    for y in range(rows):
        for x in range(cols):
            color = grid[y][x] if grid[y][x] else GRAY
            pygame.draw.rect(win, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 0)
            pygame.draw.rect(win, BLACK, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

def clear_rows():
    global grid
    grid = [row for row in grid if any(cell == 0 for cell in row)]
    while len(grid) < rows:
        grid.insert(0, [0 for _ in range(cols)])

# Основной цикл
current_piece = Piece()
running = True
fall_time = 0

while running:
    dt = clock.tick(30)
    fall_time += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and current_piece.valid(dx=-1):
                current_piece.x -= 1
            elif event.key == pygame.K_RIGHT and current_piece.valid(dx=1):
                current_piece.x += 1
            elif event.key == pygame.K_DOWN and current_piece.valid(dy=1):
                current_piece.y += 1
            elif event.key == pygame.K_UP:
                rotated = list(zip(*current_piece.shape[::-1]))
                if current_piece.valid(rotated_shape=rotated):
                    current_piece.shape = rotated

    if fall_time > 500:
        if current_piece.valid(dy=1):
            current_piece.y += 1
        else:
            current_piece.freeze()
            clear_rows()
            current_piece = Piece()
            if not current_piece.valid():
                running = False  # Game Over
        fall_time = 0

    win.fill(BLACK)
    draw_grid()
    for y, row in enumerate(current_piece.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(
                    win,
                    current_piece.color,
                    ((current_piece.x + x) * CELL_SIZE, (current_piece.y + y) * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                )

    pygame.display.flip()

pygame.quit()