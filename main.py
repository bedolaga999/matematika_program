import pygame
import random
import heapq

# Константы
WINDOW_SIZE = 500  # Размер окна
GRID_SIZE = 20  # Размер одной клетки
ROWS = WINDOW_SIZE // GRID_SIZE  # Количество строк
COLS = WINDOW_SIZE // GRID_SIZE  # Количество столбцов

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
LAVENDER = (230, 230, 250)  # Сиреневый цвет для игрока
PALE_GREEN = (152, 251, 152)  # Бледно-зеленый цвет для лабиринта

# Инициализация pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Maze Game")
font = pygame.font.Font(None, 36)  # Шрифт для уведомления о прохождении

# Создание лабиринта с начальной и конечной точками
maze = [[1 for _ in range(COLS)] for _ in range(ROWS)]  # 1 — стена, 0 — свободное пространство
start_pos = (1, 1)
end_pos = (COLS - 2, ROWS - 2)
game_won = False  # Флаг, указывающий на прохождение лабиринта


# Функция генерации лабиринта с помощью DFS
def generate_maze(x, y):
    directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]  # Направления для прорубания путей
    random.shuffle(directions)  # Перемешиваем направления для случайности
    maze[y][x] = 0  # Сделать текущую позицию проходом
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < COLS and 0 <= ny < ROWS and maze[ny][nx] == 1:
            # Прорубаем путь между ячейками
            maze[ny][nx] = 0
            maze[y + dy // 2][x + dx // 2] = 0
            generate_maze(nx, ny)


# Генерация лабиринта с использованием DFS
generate_maze(start_pos[0], start_pos[1])

# Убедимся, что начальная и конечная позиции свободны
maze[start_pos[1]][start_pos[0]] = 0
maze[end_pos[1]][end_pos[0]] = 0


# Алгоритм A*
def heuristic(a, b):
    """Эвристика: Манхэттенское расстояние"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star(start, end):
    """Алгоритм A* для поиска кратчайшего пути"""
    open_set = []
    heapq.heappush(open_set, (0 + heuristic(start, end), 0, start))  # f, g, позиция
    came_from = {}  # Словарь для восстановления пути
    g_score = {start: 0}  # Стоимость пути от начальной точки
    f_score = {start: heuristic(start, end)}  # Эвристическая оценка пути

    while open_set:
        _, current_g, current = heapq.heappop(open_set)

        # Если достигли конца, восстанавливаем путь
        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        # Проверяем соседей
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)

            if 0 <= neighbor[0] < COLS and 0 <= neighbor[1] < ROWS and maze[neighbor[1]][neighbor[0]] == 0:
                tentative_g_score = current_g + 1  # Стоимость перехода на соседнюю клетку

                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                    heapq.heappush(open_set, (f_score[neighbor], tentative_g_score, neighbor))

    return []  # Если пути нет


# Игровой цикл
player_pos = list(start_pos)  # Начальная позиция игрока
path = a_star(start_pos, end_pos)  # Находим путь с помощью A*

running = True
clock = pygame.time.Clock()


# Функция для движения игрока
def move_player(dx, dy):
    global player_pos
    new_x = player_pos[0] + dx
    new_y = player_pos[1] + dy

    if 0 <= new_x < COLS and 0 <= new_y < ROWS and maze[new_y][new_x] == 0:
        player_pos = [new_x, new_y]

    # Если игрок достиг конечной точки
    if player_pos == list(end_pos):
        return True
    return False


while running:
    screen.fill(WHITE)

    # Отрисовываем лабиринт
    for y in range(ROWS):
        for x in range(COLS):
            color = PALE_GREEN if maze[y][x] == 0 else BLACK
            pygame.draw.rect(screen, color, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

            # Отметим начальную точку
            if (x, y) == start_pos:
                pygame.draw.rect(screen, BLUE, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

            # Отметим конечную точку
            if (x, y) == end_pos:
                pygame.draw.rect(screen, GREEN, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Отметим путь
    for p in path:
        pygame.draw.rect(screen, (255, 255, 0), (p[0] * GRID_SIZE, p[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Отметим игрока
    pygame.draw.rect(screen, LAVENDER, (player_pos[0] * GRID_SIZE, player_pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Проверка на управление игроком
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move_player(0, -1)
            elif event.key == pygame.K_DOWN:
                move_player(0, 1)
            elif event.key == pygame.K_LEFT:
                move_player(-1, 0)
            elif event.key == pygame.K_RIGHT:
                move_player(1, 0)

    # Если игрок достиг цели
    if player_pos == list(end_pos):
        message = font.render("Поздравляем! Вы прошли лабиринт!", True, (255, 0, 0))
        screen.blit(message,
                    (WINDOW_SIZE // 2 - message.get_width() // 2, WINDOW_SIZE // 2 - message.get_height() // 2))

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
