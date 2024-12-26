import matplotlib.pyplot as plt
import numpy as np

# Настройки спирали
num_points = 1000  # Количество точек на спирали
angle_increment = 0.1  # Увеличение угла в радианах
step_increment = 0.01  # Увеличение шага для каждой точки

# Создание массивов для хранения координат x и y
x_values = []
y_values = []

# Генерация спирали
current_angle = 0
current_radius = 0
for i in range(num_points):
    # Вычисление координат x и y на основе текущего радиуса и угла
    x = current_radius * np.cos(current_angle)
    y = current_radius * np.sin(current_angle)

    # Сохранение координат
    x_values.append(x)
    y_values.append(y)

    # Увеличение угла и радиуса для следующей точки
    current_angle += angle_increment
    current_radius += step_increment

# Построение графика спирали
plt.figure(figsize=(6, 6))
plt.plot(x_values, y_values, color='blue')
plt.title("Спираль с увеличивающимся шагом")
plt.axis('equal')  # Сохранение одинакового масштаба для осей
plt.grid(True)
plt.show()
