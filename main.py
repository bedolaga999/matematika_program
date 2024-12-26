import tkinter as tk
import random

# Размер поля
SIZE = 7
# Размеры кораблей
SHIP_SIZES = [3, 2, 1, 1]
# Направления для проверки соседей
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

# Функция для генерации случайного положения кораблей
def generate_ships():
    grid = [['.' for _ in range(SIZE)] for _ in range(SIZE)]
    ships = []

    for ship_size in SHIP_SIZES:
        placed = False
        while not placed:
            orientation = random.choice(['horizontal', 'vertical'])
            if orientation == 'horizontal':
                row = random.randint(0, SIZE - 1)
                col = random.randint(0, SIZE - ship_size)
                if all(grid[row][col + i] == '.' for i in range(ship_size)):
                    for i in range(ship_size):
                        grid[row][col + i] = 'S'
                    ships.append((row, col, orientation, ship_size))
                    placed = True
            else:
                row = random.randint(0, SIZE - ship_size)
                col = random.randint(0, SIZE - 1)
                if all(grid[row + i][col] == '.' for i in range(ship_size)):
                    for i in range(ship_size):
                        grid[row + i][col] = 'S'
                    ships.append((row, col, orientation, ship_size))
                    placed = True

    return grid, ships

# Класс для игрового интерфейса
class SeaBattleGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Морской бой")
        self.geometry(f"{SIZE * 60}x{SIZE * 60 + 100}")

        # Разделение экрана на два фрейма
        self.main_frame = tk.Frame(self)
        self.main_frame.pack()

        # Игровое поле (для взаимодействия)
        self.game_frame = tk.Frame(self.main_frame)
        self.game_frame.grid(row=0, column=0)

        # Экран расположения кораблей (для отображения)
        self.ship_frame = tk.Frame(self.main_frame)
        self.ship_frame.grid(row=0, column=1, padx=10)

        # Кнопка для рандомного изменения расположения кораблей
        self.random_button = tk.Button(self, text="Random", width=20, command=self.randomize_ships)
        self.random_button.pack()

        # Инициализация поля
        self.grid = [['.' for _ in range(SIZE)] for _ in range(SIZE)]
        self.ship_grid = [['.' for _ in range(SIZE)] for _ in range(SIZE)]
        self.buttons = {}
        self.ships = []

        self.create_widgets()
        self.generate_ships()

    def create_widgets(self):
        # Игровое поле (для взаимодействия) - левый экран
        for row in range(SIZE):
            for col in range(SIZE):
                button = tk.Button(self.game_frame, text=' ', width=6, height=3, command=lambda r=row, c=col: self.cell_click(r, c))
                button.grid(row=row, column=col)
                self.buttons[(row, col)] = button

        # Экран расположения кораблей (только для отображения) - правый экран
        for row in range(SIZE):
            for col in range(SIZE):
                button = tk.Button(self.ship_frame, text=' ', width=6, height=3, state='disabled')
                button.grid(row=row, column=col)

    def generate_ships(self):
        self.grid, self.ships = generate_ships()

        # Отображение кораблей на экране расположения (правый экран)
        for row in range(SIZE):
            for col in range(SIZE):
                if self.grid[row][col] == 'S':
                    # Подсвечиваем клетки с кораблями сиреневым цветом на правом экране
                    self.ship_frame.grid_slaves(row=row, column=col)[0].config(bg='purple')

    def randomize_ships(self):
        # Пересоздание расположения кораблей
        self.grid = [['.' for _ in range(SIZE)] for _ in range(SIZE)]
        self.ship_grid = [['.' for _ in range(SIZE)] for _ in range(SIZE)]

        for button in self.ship_frame.grid_slaves():
            button.config(bg='white')  # Очищаем экран расположения кораблей

        for button in self.game_frame.grid_slaves():
            button.config(bg='white')  # Очищаем игровое поле

        self.generate_ships()

    def cell_click(self, row, col):
        if self.grid[row][col] == 'S':
            self.buttons[(row, col)].config(bg='red')  # Клетка с кораблем становится красной
            self.grid[row][col] = 'X'  # Мечаем клетку как пораженную
        else:
            self.buttons[(row, col)].config(bg='gray')  # Клетка без корабля становится серой

if __name__ == "__main__":
    game = SeaBattleGame()
    game.mainloop()
