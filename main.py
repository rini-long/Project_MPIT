import turtle
import numpy as np
import random

# Настройка окна
window = turtle.Screen()
window.bgcolor("black")
window.tracer(0)  # Отключаем автоматическое обновление экрана

# Настройка главной черепашки
spiral_turtle = turtle.Turtle()
spiral_turtle.shape("turtle")
spiral_turtle.color("blue")
spiral_turtle.speed(0)  # Максимальная скорость
spiral_turtle.hideturtle()
spiral_turtle.penup()  # Поднять перо, чтобы не рисовать начальную точку

# Параметры логарифмической спирали
a = 10  # Начальный радиус
b = 0.1  # Коэффициент роста
theta_max = 15 * np.pi  # Максимальный угол (25π для большого количества витков)
num_points = 4000  # Количество точек для построения

# Генерация углов и радиусов
theta = np.linspace(0, theta_max, num_points)
r = a * np.exp(b * theta)

# Цвета для "дочек"
colors = ['yellow', 'LightCyan', 'white','LightYellow','LemonChiffon']

# Функция для рисования одной спирали
def draw_spiral(offset_x, offset_y, start_point=0, s=0, rnd=0.09):
    # Переход из полярных координат в декартовы с учетом смещения
    x = r * np.cos(theta) + offset_x
    y = r * np.sin(theta) + offset_y

    # Перемещение черепашки в начальную точку
    spiral_turtle.goto(x[0], y[0])
    spiral_turtle.penup()

    # Рисование спирали и добавление "дочек"
    for i in range(1, num_points):

        if i>s:
            spiral_turtle.goto(x[i], y[i])
            # Случайное добавление "дочек" вдоль спирали
            if random.random() < rnd and i > start_point:  # Вероятность 9% на каждой точке
                spiral_turtle.dot(random.randint(1, 3), random.choice(colors))

# Рисование нескольких спиралей с разными смещениями
offsets = [
    (0, 0),      # Центральная спираль
    (10, 10),    # Смещение вправо и вверх
    (-10, 10),   # Смещение влево и вверх
    (10, -10),   # Смещение вправо и вниз
    (-10, -10),  # Смещение влево и вниз
    (15, 0),     # Смещение вправо
    (-15, 0),    # Смещение влево
    (0, 15),     # Смещение вверх
    (0, -50),    # Смещение вниз
]

# Рисование всех спиралей
for offset in offsets:
    draw_spiral(offset[0], offset[1], start_point=0, s=0)


# Рисование нескольких спиралей с разными смещениями
offsets = [
    (30, 30),    # Смещение вправо и вверх
    (-30, 30),   # Смещение влево и вверх
    (30, -30),   # Смещение вправо и вниз
    (-30, -30),  # Смещение влево и вниз
    (30, 0),     # Смещение вправо
    (-30, 0),    # Смещение влево
    (0, 30),     # Смещение вверх
    (0, -30),    # Смещение вниз
]

# Рисование всех спиралей
for offset in offsets:
    draw_spiral(offset[0], offset[1], start_point=200, s=200, rnd=0.09)
# Обновление экрана
window.update()

# Завершение работы
window.mainloop()