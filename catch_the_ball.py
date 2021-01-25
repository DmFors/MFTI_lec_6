import pygame
from pygame.draw import *
from random import randint, choice

pygame.init()

FPS = 30
A, B = 1200, 650  # screen width and height
sc = pygame.display.set_mode((A, B))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


def generate_new_ball() -> list:
    """
    генерирует псевдослучайные параметры круга
    :return: цвет, координаты, радиус, вектор скорости круга
    """
    x = randint(100, A - 100)
    y = randint(100, B - 100)
    r = choice(range(10, 101, 10))
    color = choice(COLORS)
    speed = [-1, 1]
    Vx, Vy = speed[randint(0, 1)], speed[randint(0, 1)]
    return [color, x, y, r, [Vx, Vy]]


def draw_ball(screen, params) -> None:
    """
    рисует круг в заданном месте холста с заданными параметрами
    :param screen: холст, на котором рисуются круг
    :param params: параметры круга (color, x, y, r)
    :return: None
    """
    color, x, y, r, *needless = params
    circle(screen, color, (x, y), r)


def move_ball(params) -> list:
    """
    пересчитывает координаты круга, в соответствии с заданным вектором скорости
    :param params: параметры круга и его скорости (color, x, y, r, velocity)
    :return параметры круга с пересчитанными координатами (color, x, y, r, velocity)
    """
    color, x, y, r, [Vx, Vy] = params
    x = x + Vx
    y = y + Vy
    params = [color, x, y, r, [Vx, Vy]]
    return params


def check_collision(params, a, b) -> list:
    """
    проверяет столкновение круга с границами холста
    :param params: параметры круга (color, x, y, r, velocity)
    :param a: ширина холста
    :param b: высота холста
    :return: параметры круга с пересчитанным вектором скорости
    """
    color, x, y, r, [Vx, Vy] = params
    if x - r == 0 or x + r == a:
        Vx = -Vx
    if y - r == 0 or y + r == b:
        Vy = -Vy
    params = [color, x, y, r, [Vx, Vy]]
    return params


def check_hit(params, event) -> bool:
    """
    проверяет попадание клика мыши в круг
    :param params: пармаметры круга (color, x, y, r)
    :param event: событие = клик мыши по холсту
    :return: есть попадание: True; нет попадания: False
    """
    x_ball, y_ball, r = params[1:4]
    x_clk, y_clk = event.pos
    distance = ((x_clk - x_ball) ** 2 + (y_clk - y_ball) ** 2) ** 0.5
    if distance <= r:
        return True
    else:
        return False


def calc_score(params, score) -> tuple:
    """
    добавляет к общему счёту число очков,
    количество которых зависит от параметров полученного круга
    :param params: пармаметры круга (color, x, y, r, velocity)
    :param score: счёт
    :returns: новое значение счёта, разницу между предыд и тек счётом
    """
    r = params[3]
    diff = 110 - r
    score += diff
    return score, diff


def print_the_score(screen, score, diff) -> None:
    """
    печатает текущее количество очков (счёт) на холст
    :param screen: холст, на который будет напечатан счёт
    :param score: текущий счёт
    :param diff:  разница между пред и тек счётом
    :return:
    """
    color = (255, 255, 255)
    background = (100, 50, 100)
    fontObj = pygame.font.Font(None, 50)
    textSurfaceObj = fontObj.render(f'Your score: {score} (+{diff})', True, color, background)
    screen.blit(textSurfaceObj, [10, 10])


def mouse_button_down(balls, game_score, game_diff) -> tuple:
    """
    обрабатывает нажатия кнопок мышки
    :return:
    """
    for i, ball_params in enumerate(balls):
        if check_hit(ball_params, event):
            game_score, game_diff = calc_score(ball_params, game_score)
            del balls[i]
    return balls, game_score, game_diff


pygame.display.update()
clock = pygame.time.Clock()
finished = False
ball_params = None
game_score = game_diff = spawn_time = 0
balls = []

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
            break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            balls, game_score, game_diff = mouse_button_down(balls, game_score, game_diff)

    sc.fill(BLACK)
    if len(balls) < 10:
        spawn_time += 1
        if spawn_time > 99:
            balls.append(generate_new_ball())
            spawn_time = 0

    for i, ball_params in enumerate(balls):
        draw_ball(sc, ball_params)
        balls[i] = move_ball(ball_params)
        balls[i] = check_collision(balls[i], A, B)

    print_the_score(sc, game_score, game_diff)
    pygame.display.flip()

pygame.quit()
